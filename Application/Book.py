from Book.IBook import IBook

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

CHAPTERS_TABLE = "following-sibling::*[1]"

class Book(IBook):
    def __init__(self, book: WebElement):
        self._book_element = book

    def expand(self) -> None:
        self._book_element.click()

    def getName(self) -> str:
        return self._book_element.text.strip().title()

    
    def getAllChapterElements(self) -> list[WebElement]:
        chapters_table = self._book_element.find_element(By.XPATH, CHAPTERS_TABLE)
        chapters_ref = WebDriverWait(chapters_table, 60).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, "a"))
        )
        return chapters_ref
    
    def getChapterCount(self) -> int:
        return len(self.getAllChapterElements())

