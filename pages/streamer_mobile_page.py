import os
import time
from selenium.webdriver.common.by import By

from helpers.page_log import log_method_call
from pages.base_mobile_page import BaseMobilePage


class StreamerMobilePage(BaseMobilePage):
    __STREAMER_NAME_LOC = By.CSS_SELECTOR, ".tw-title"
    __FOLLOW_BUTTON_LOC = By.CSS_SELECTOR, "[aria-label*='Follow']"

    @log_method_call
    def wait_until_video_starts_playing(self):
        self._driver.wait_until_video_is_loaded_and_started(timeout=10)

    @log_method_call
    def get_streamer_name(self):
        return self._driver.find_element(*self.__STREAMER_NAME_LOC).text

    @log_method_call
    def follow_streamer(self):
        self._driver.find_element(*self.__FOLLOW_BUTTON_LOC).click()

    @log_method_call
    def take_streamer_page_screenshot(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        streamer_name = self.get_streamer_name()
        file_name = f"{streamer_name}-{time.time()}.png"
        screenshot_path = os.path.join(project_root, file_name)
        self._driver.save_screenshot(screenshot_path)
