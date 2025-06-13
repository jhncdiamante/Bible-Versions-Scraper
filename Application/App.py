from .Website import BibleWebsite
from Driver.NormalDriver import NormalDriver
from .Menu import Menu
from .Book import Book
from .Chapter import Chapter
from .CookieHandler import CookieHandler
from Data.TextDatabase import TextDatabase

BASE_URL = "https://www.die-bibel.de/en/bible/"
VERSIONS = ["BHS", "LXX", "VUL", "UBS5"]

VERSION = VERSIONS[0] # replace index [0] = BHS, [1] = LXX, ...


driver = NormalDriver()
driver.set_up_driver()
driver_handle = driver.driver 

menu_handler = Menu(driver_handle)
cookie_handler = CookieHandler(driver_handle)


website = BibleWebsite(
    f"{BASE_URL}{VERSION}",
    driver=driver_handle,
    menu=menu_handler,
    book=Book,       
    chapter=Chapter,
    cookie_handler=cookie_handler
)
print("Scraping", VERSION)
text_db = TextDatabase(VERSION)
website.attach(text_db)
website.open()
website.scrape()
