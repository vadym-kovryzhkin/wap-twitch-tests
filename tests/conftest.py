import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import config

from driver import driver

"""
NOTE:

There is a difference between resizing the browser window to match a mobile device’s dimensions 
    and using Chrome DevTools to emulate a mobile device.
    
When we resize the Chrome browser window to the X mobile device dimensions 
    versus selecting the X mobile device in Chrome’s DevTools mobile emulation, there are some important differences:

    1. Screen Resolution and Pixel Density:
        resizing the window to iPhone dimensions does not change the pixel density. 
        It only matches the physical width and height in pixels, 
            but our desktop monitor’s pixel density can be lower than mobile device.

        in devtools emulation, Chrome simulates the actual pixel density of the iPhone 14 Pro

    2. Touch Events:
        resizing the window doesn’t let us interact with the page using touch gestures like tap, swipe, 
            or pinch-to-zoom.
    
        In mobile emulation, Chrome mimics touch events

    3. User-Agent:
        When we resize the window, the browser still identifies as a desktop device because of user-agent.
        Of course we can set a custom user-agent. But we will have to support it manually.
        With mobile emulations, the user-agent switches to match the X device, 
            so the site might serve mobile-specific content.

However, mobileEmulation is still experimental and may not work as expected in some cases.
    For example, there are known issues with scrolling in mobile emulation mode on Ubuntu 24.04.
    Related StackOverflow thread:
    https://stackoverflow.com/questions/22722727/chrome-devtools-mobile-emulation-scroll-not-working
At the same time, we may face some issues with resizing the browser window to match a mobile device’s dimensions.
    For example, we can't interact with the page using touch gestures like tap, swipe, or pinch-to-zoom.
    
    
For this specific task - it is not a big deal which option to use. 
But for production version - this approach should be investigated in more detail.
"""


@pytest.fixture()
def mobile_chrome_driver():
    mobile_emulation = {"deviceName": config.DEVICE_NAME}
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    d = driver.SportyWebDriver(
        webdriver.Chrome(options=chrome_options),
        driver.EventListener()
    )
    yield d
    d.quit()
