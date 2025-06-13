from Subject.Subject import Subject
from Website.IWebsite import IWebsite
from Menu.IMenu import IMenu
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from Book.IBook import IBook
from Chapter.IChapter import IChapter
from CookieHandler.ICookieHandler import ICookieHandler
import time, random

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
        except Exception:
            pass

    def scrape(self) -> None:
        self._menu.open() # Open the menu
        books = self._menu.getAllBookElements()
        print(f"Found {len(books)} book/s.")

        for book in (books[::-1]):
            self._scrape_book(book)

    def _go_to_element(self, element):
        self._driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        

    def _scrape_book(self, book_element):
        # scroll view/ center to the book
        self._go_to_element(book_element)
        book_scraper = self._book(book_element)
        book_name = book_scraper.getName()
        print("Scraping", book_name)
        book_scraper.expand()

        chapters = book_scraper.getAllChapterElements()
        print(f"Found {len(chapters)} chapter/s.")

        for i, chapter in enumerate(chapters):
            self._scrape_chapter(chapter, i + 1)

    def _scrape_chapter(self, chapter_element, chapter_number):
        self._go_to_element(chapter_element)
        chapter_scraper = self._chapter(chapter_element)
        verses = chapter_scraper.getAllVerses()
        chap_abv = chapter_scraper.getChapterAbbreviation()
        print(f"Found {len(verses)} verse/s.")

        for verse_number, verse in enumerate(verses, start=1):
            self.current_data = {
                "chap abv": chap_abv,
                "chapter number": chapter_number,
                "verse number": verse_number,
                "verse content": verse
            }
        time.sleep(random.randint(2, 5))
