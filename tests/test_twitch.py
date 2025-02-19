import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.home_page import BasePage
from utilities.logger import LogGen

logger = LogGen.loggen()


def test_twitch_workflow(driver: WebDriver):
    """Test complete Twitch workflow including cookie acceptance, search, and streamer selection"""
    try:
        logger.info("Starting Twitch workflow test")
        base_page = BasePage(driver)
        base_page.accept_cookie()
        base_page.search()
        base_page.scroll()
        base_page.live_streamers()
        base_page.take_screenshot()
        logger.info("Test completed successfully")

    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        pytest.fail(f"Test failed due to: {str(e)}")