from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from driver import driver as d
import config
from helpers.page_log import log_method_call


class BaseMobilePage:
    __COOKIES_BANNER_LOC = By.CSS_SELECTOR, "div .consent-banner"
    __SEARCH_BUTTON_LOC = By.CSS_SELECTOR, "a[aria-label='Search']"
    __SEARCH_INPUT_LOC = By.CSS_SELECTOR, "input[data-a-target='tw-input']"

    def __init__(self, driver: d.SportyWebDriver):
        self._driver = driver

    @log_method_call
    def open(self, url: str = None):
        self._driver.get(url or config.BASE_UI_URL)

    # next actions are available on every page

    @log_method_call
    def search_for(self, text: str):
        self._driver.find_element(*self.__SEARCH_BUTTON_LOC).click()
        search_input = self._driver.find_element(*self.__SEARCH_INPUT_LOC)
        search_input.send_keys(text)
        search_input.send_keys(Keys.RETURN)

    @log_method_call
    def accept_cookies(self):
        """
        Accept cookies banner
        Note: we implement hiding (not accept) since twitch a detection of automated tools.
            We can either use stealth library or undetected_chromedriver to bypass this.
            However, I would suggest this is beyond the scope of this task.
        """
        accept_cookies_button = self._driver.find_element(*self.__COOKIES_BANNER_LOC)
        self._driver.execute_script('arguments[0].setAttribute("style", "display: none;")', accept_cookies_button)

    @log_method_call
    def scroll(self, times=1):
        for _ in range(times):
            self._driver.scroll()

    @log_method_call
    def wait_until_page_is_fully_loaded(self):
        self._driver.wait_until_page_is_loaded()
        self._driver.wait_until_images_loaded()
