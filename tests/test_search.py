from driver import driver as d
from pages.home_mobile_page import HomeMobilePage
from pages.search_mobile_page import SearchMobilePage
from pages.streamer_mobile_page import StreamerMobilePage

"""
NOTE:
According to the 
    "Some streamers will have a modal or pop-up before loading the video, 
    the Auto test case should be able to handle this pop-up."
    
in all regions with various streamers I have checked - there is no pop-up before loading the video. 
This requires more time to investigate: find a specific streamer with restrictions for a specific region.
"""


def test_should_search_and_make_screenshot(mobile_chrome_driver: d.SportyWebDriver):
    # Arrange
    search_subject_name = "StarCraft II"

    home_page = HomeMobilePage(mobile_chrome_driver)
    search_page = SearchMobilePage(mobile_chrome_driver)
    streamer_page = StreamerMobilePage(mobile_chrome_driver)

    # Act
    home_page.open()
    home_page.accept_cookies()
    home_page.search_for(search_subject_name)

    search_page.open_channels_tab()
    search_page.scroll(times=2)
    search_page.select_any_channel()

    streamer_page.wait_until_page_is_fully_loaded()
    streamer_page.wait_until_video_starts_playing()
    streamer_page.take_streamer_page_screenshot()

    # Assert
    # nothing to assert according to the task
