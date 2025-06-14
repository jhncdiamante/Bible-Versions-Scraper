from Subject.Subject import Subject
from Website.IWebsite import IWebsite
from Menu.IMenu import IMenu
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from Book.IBook import IBook
from Chapter.IChapter import IChapter
from CookieHandler.ICookieHandler import ICookieHandler
import time, random
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BibleWebsite(Subject, IWebsite):
    def __init__(self,
                 url: str,
                 driver: WebDriver,
                 menu: IMenu,
                 book: IBook,
                 chapter: IChapter,
                 cookie_handler: ICookieHandler
                 ):
        
        super().__init__()
        self.url = url
        self._driver = driver
        self._menu = menu
        self._book = book
        self._chapter = chapter
        self._cookie_handler = cookie_handler
        self._current_data = None  ## represents current node data (e.g. "2PE 1:1	Συμεὼν Πέτρος δοῦλος καὶ ἀπ")
        self._driver.maximize_window()
        self._last_highlighted = None

    @property
    def current_data(self):
        return self._current_data


    @current_data.setter
    def current_data(self, current_data):
        # Updates a new row for the text file database with the current data node
        self._current_data = current_data
        self.notify()
        

    def open(self):
        # opens the base page and waits to be fully loaded
        self._driver.get(self.url)
        WebDriverWait(self._driver, 30).until(
            lambda _: self._driver.execute_script('return document.readyState') == 'complete'
        )
        try:
            self._cookie_handler.clickAllowCookiesButton()
        except TimeoutException:
            pass
        time.sleep(3)

    def scrape(self) -> None:
        self._menu.open() # Open the menu
        books = self._menu.getAllBookElements()
        print(f"Found {len(books)} book/s.")

        for book in books:
            self._scrape_book(book)

    def _go_to_element(self, element):
        self._driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", element)
        time.sleep(0.3)

    def _dehighlight_chapter(self):
        self._driver.execute_script("arguments[0].style.outline = '';", self._last_highlighted)


    def _highlight_chapter(self, chapter_element):
        if self._last_highlighted: # removes highlight from previous chapter and highlight the new one
            self._dehighlight_chapter()
        self._driver.execute_script("arguments[0].style.outline = '3px solid red';", chapter_element) # highlights the chapter element
        self._last_highlighted = chapter_element
        time.sleep(0.5)
        

    def _scrape_book(self, book_element):
        book_scraper = self._book(book_element)
        book_name = book_scraper.getName()
        print("Scraping", book_name)
        # scroll view/ center to the book
        self._go_to_element(book_element) 

        book_scraper.expand()

        # When menu panel is opened, there is a specific book that is expanded in default.
        # Therefore, when line "book_scraper.expand()" runs and the default one is the first book
        # the book will be closed, resulting in an error when we locate the chapters table
        # simply expand it again in that case
        try:
            chapters = book_scraper.getAllChapterElements()
        except (TimeoutException, NoSuchElementException,):
            book_scraper.expand()
            chapters = book_scraper.getAllChapterElements()
        except Exception as e:
            print(f"Error in scraping {book_name}: {str(e)}")
            raise Exception
        
        print(f"Found {len(chapters)} chapter/s.")
        for chapter_number, chapter_element in enumerate(chapters, start=1): 
            self._scrape_chapter(chapter_element=chapter_element, chapter_number=chapter_number)

        self._dehighlight_chapter() # OPTIONAL: removes highlighted chapter (the last one) before closing the book
        self._last_highlighted = None # reset highlighter for new book (will throw StaleElementException) if not reset per book

    def _scrape_chapter(self, chapter_element, chapter_number):
        self._go_to_element(chapter_element)
        self._highlight_chapter(chapter_element)    

        chapter_scraper = self._chapter(chapter_element, chapter_number)
        verses = chapter_scraper.getAllVerses()
        chap_abv = chapter_scraper.getChapterAbbreviation()
        print(f"Found {len(verses)} verse/s.")

        for verse_number, verse_content in verses.items():
            self.current_data = {
                "chap abv": chap_abv,
                "chapter number": chapter_number,
                "verse number": verse_number,
                "verse content": verse_content
            }
        time.sleep(random.randint(2, 5))
