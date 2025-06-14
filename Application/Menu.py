from Menu.IMenu import IMenu
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Helpers.retryable import retryable
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

MENU_BUTTON_CONTAINER = "ibep-bible-reader-container"
MENU_BUTTON = "button"
MENU_PANE = "ibep-chapter-picker"
BOOKS_C_NAME = 'div[class="border-grayExtraLight border-b"]'
FIRST_CHILD = "./div[1]"

class Menu(IMenu):
    def __init__(self, driver: WebDriver):
        self._driver = driver

    @retryable(max_retries=3, delay=2, exceptions=(TimeoutException,))
    def open(self) -> None:
        # Locate container where the menu button lies
        container = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.TAG_NAME, MENU_BUTTON_CONTAINER))
        )
        print("Found container.")
        # get menu button
        menu_button = WebDriverWait(container, 60).until(
            EC.element_to_be_clickable((By.TAG_NAME, MENU_BUTTON))
        )

        menu_button.click()
        print("Menu Button clicked.")

        # wait for menu panel to appear after the menu button is clicked
        WebDriverWait(self._driver, 30).until(
            EC.visibility_of_element_located((By.TAG_NAME, MENU_PANE))
        )
        print("Menu panel found.")
        
    
    @retryable(max_retries=3, delay=2, exceptions=(TimeoutException, NoSuchElementException,))
    def getAllBookElements(self) -> list[WebElement]:
        # get the menu panel where books are located
        menu_pane = self._driver.find_element(By.TAG_NAME, MENU_PANE)

        books = WebDriverWait(menu_pane, 90).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, BOOKS_C_NAME))
        ) 
        # returns all book elements
        return [book.find_element(By.XPATH, FIRST_CHILD) for book in books]
        

