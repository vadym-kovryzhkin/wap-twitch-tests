from time import sleep
from typing import Tuple, Callable, Any, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support import event_firing_webdriver

GLOBAL_WAIT_ELEMENT_TIMEOUT = 4
GLOBAL_EC_TIMEOUT = 10
GLOBAL_EC_POLL_FREQUENCY = 0.05


class EventListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        wait = WebDriverWait(driver, timeout=GLOBAL_WAIT_ELEMENT_TIMEOUT,
                             ignored_exceptions=(StaleElementReferenceException, NoSuchElementException))
        try:
            wait.until(EC.visibility_of_element_located((by, value)))
        except TimeoutException:
            pass


class SportyWebDriver(event_firing_webdriver.EventFiringWebDriver):
    def wait_until_images_loaded(self, timeout: float = GLOBAL_EC_TIMEOUT,
                                 poll_frequency: float = GLOBAL_EC_POLL_FREQUENCY):
        WebDriverWait(self._driver, timeout=timeout, poll_frequency=poll_frequency).until(
            lambda d: all(
                d.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0", img)
                for img in d.find_elements(By.TAG_NAME, "img")
            )
        )

    def wait_until_video_is_loaded_and_started(self, timeout: float = GLOBAL_EC_TIMEOUT,
                                               poll_frequency: float = GLOBAL_EC_POLL_FREQUENCY):
        WebDriverWait(self._driver, timeout=timeout, poll_frequency=poll_frequency).until(
            lambda d: d.execute_script("""
                const video = document.querySelector('video');
                return video && video.currentTime > 0 && !video.paused && !video.ended && video.readyState >= 3;
            """)  # readyState 3 or 4 means the video has enough data to play
        )

    def wait_until_page_is_loaded(self, timeout: float = GLOBAL_EC_TIMEOUT,
                                  poll_frequency: float = GLOBAL_EC_POLL_FREQUENCY):
        WebDriverWait(self._driver, timeout=timeout, poll_frequency=poll_frequency).until(
            lambda d: d.execute_script("return document.readyState") == "complete")

    def wait_until_element_is_visible(self, locator: Tuple[str, str], timeout: float = GLOBAL_EC_TIMEOUT,
                                      poll_frequency: float = GLOBAL_EC_POLL_FREQUENCY):
        WebDriverWait(self._driver, timeout=timeout, poll_frequency=poll_frequency).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_until_element_is_clickable(self, locator: Tuple[str, str], timeout: float = GLOBAL_EC_TIMEOUT,
                                        poll_frequency: float = GLOBAL_EC_POLL_FREQUENCY):
        WebDriverWait(self._driver, timeout=timeout, poll_frequency=poll_frequency).until(
            EC.element_to_be_clickable(locator)
        )

    def scroll(self, timeout: float = 2, wait_for_action: Optional[Callable[..., Any]] = None):
        self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(timeout)
        if wait_for_action:
            wait_for_action()

    def is_web_element_in_viewport(self, web_element: WebElement):
        return self._driver.execute_script(
            "var elem = arguments[0],"
            "    box = elem.getBoundingClientRect(),"
            "    cx = box.left + box.width / 2,"
            "    cy = box.top + box.height / 2,"
            "    isVisible = (cx >= 0 && cx <= window.innerWidth) && (cy >= 0 && cy <= window.innerHeight);"
            "if (!isVisible) return false;"
            "var style = window.getComputedStyle(elem);"
            "if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return false;"
            "var topElem = document.elementFromPoint(cx, cy);"
            "return elem === topElem || elem.contains(topElem);",
            web_element
        )
