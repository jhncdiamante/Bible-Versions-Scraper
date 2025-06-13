from CookieHandler.ICookieHandler import ICookieHandler

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Helpers.retryable import retryable
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException, InvalidCoordinatesException
from selenium.webdriver.remote.webdriver import WebDriver

ALLOW_BUTTON_ID = "onetrust-accept-btn-handler"

class CookieHandler(ICookieHandler):
    def __init__(self, driver: WebDriver):
        self._driver = driver

    @retryable(max_retries=3, delay=5, exceptions=(TimeoutException, ))
    def clickAllowCookiesButton(self) -> None:
        allow_all_button = WebDriverWait(self._driver, 30).until(
            EC.element_to_be_clickable((By.ID, ALLOW_BUTTON_ID))
        )
        allow_all_button.click()