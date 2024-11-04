from selenium.webdriver.common.by import By

from helpers.page_log import log_method_call
from pages.base_mobile_page import BaseMobilePage


class SearchMobilePage(BaseMobilePage):
    __CHANNELS_TAB_LOC = By.CSS_SELECTOR, "li [role='tab'][href*='channels']"
    __CATEGORIES_TAB_LOC = By.CSS_SELECTOR, "li [role='tab'][href*='categories']"
    __VIDEOS_TAB_LOC = By.CSS_SELECTOR, "li [role='tab'][href*='categories']"
    __ALL_CHANNELS_LOC = By.CSS_SELECTOR, 'a.tw-link'

    @log_method_call
    def open_channels_tab(self):
        self._driver.find_element(*self.__CHANNELS_TAB_LOC).click()
        self._driver.wait_until_element_is_visible((By.CSS_SELECTOR, ".tw-image"))

    @log_method_call
    def open_categories_tab(self):
        self._driver.find_element(*self.__CATEGORIES_TAB_LOC).click()

    @log_method_call
    def open_videos_tab(self):
        self._driver.find_element(*self.__VIDEOS_TAB_LOC).click()

    @log_method_call
    def select_any_channel(self):
        # I suggest to not use random data and find a specific streamer every time.
        # However, in this case - list of streamers is dynamic (based on views and so on).
        # So we can always select first
        channels_elements = self._driver.find_elements(*self.__ALL_CHANNELS_LOC)
        visible_channels = [element for element in channels_elements if
                            self._driver.is_web_element_in_viewport(element)]
        visible_channels[0].click()
