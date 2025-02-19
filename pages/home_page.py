import os
import time
from datetime import datetime
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utilities.helpers import Helper
from utilities.logger import LogGen

logger = LogGen.loggen()


class PageOperationError(Exception):
    """Base exception for page operation failures"""
    pass


class BasePage(Helper):
    COOKIES_XPATH = "//div[text()='Accept']"
    VIDEO_CONTAINER_LOCATOR = (By.XPATH, "//div[@data-a-target='video-ref']")
    VIDEO_ELEMENT_LOCATOR = (By.TAG_NAME, "video")

    def __init__(self, driver: WebDriver):
        """Initialize BasePage instance with WebDriver"""
        try:
            super().__init__(driver)
            self.driver = driver
        except Exception as e:
            logger.error(f"Failed to initialize BasePage: {str(e)}")
            raise PageOperationError("Page initialization failed") from e

    def accept_cookie(self):
        """Attempt to accept cookies consent dialog"""
        try:
            logger.info("Attempting to accept cookies")
            accept_button = Helper.wait_until_element_clickable(
                self,
                locator_type=By.XPATH,
                locator=self.COOKIES_XPATH,
                timeout=10
            )
            accept_button.click()
            logger.info("Cookies accepted successfully")
        except TimeoutException:
            logger.warning("Cookie acceptance dialog not found within timeout")
        except NoSuchElementException:
            logger.warning("Cookie acceptance element not found")
        except WebDriverException as e:
            logger.error(f"Failed to accept cookies: {str(e)}")
            raise PageOperationError("Cookie acceptance failed") from e

    def search(self):
        """Perform search operation for 'StarCraft II'"""
        try:
            logger.info("Executing search operation")
            browse_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Browse']"))
            )
            browse_button.click()

            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
            )
            search_box.send_keys("StarCraft II" + Keys.RETURN)
            logger.info("Search operation completed successfully")

        except TimeoutException as e:
            logger.error("Search elements not found within timeout")
            raise PageOperationError("Search operation timed out") from e
        except WebDriverException as e:
            logger.error(f"Search operation failed: {str(e)}")
            raise PageOperationError("Search operation failed") from e

    def scroll(self):
        """Scroll through search results"""
        try:
            logger.info("Scrolling through results twice")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@src, 'live_user')]"))
            )
            viewport_height = self.driver.execute_script("return window.innerHeight")
            for _ in range(2):
                self.driver.execute_script(f"window.scrollBy(0, {viewport_height // 2})")
                time.sleep(2)
            logger.info("Scrolling completed successfully")

        except WebDriverException as e:
            logger.error(f"Scrolling failed: {str(e)}")
            raise PageOperationError("Scrolling operation failed") from e

    def live_streamers(self):
        """Select and interact with the first live streamer"""
        try:
            logger.info("Processing live streamers")
            streamers = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@src, 'live_user')]"))
            )

            if not streamers:
                logger.warning("No live streamers found")
                return
            first_streamer = streamers[0]
            parent_element = first_streamer.find_element(By.XPATH, "./ancestor::button")

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", parent_element)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", parent_element)
            logger.info("Clicked on the first live streamer")

            WebDriverWait(self.driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

        except TimeoutException as e:
            logger.error("Streamer elements not found or page didn't load")
            raise PageOperationError("Streamer interaction timed out") from e
        except WebDriverException as e:
            logger.error(f"Streamer interaction failed: {str(e)}")
            raise PageOperationError("Streamer operation failed") from e

    def take_screenshot(self) -> str:
        """Capture and save screenshot with test name and timestamp"""
        try:
            logger.info("Capturing final screenshot")
            self.get_video_element()

            test_name = getattr(self.driver, 'test_name', 'screenshot')
            sanitized_name = self._sanitize_filename(test_name)
            timestamp = datetime.now().strftime("%d-%b-%y_%I.%M.%S%p").lower()

            screenshot_dir = os.path.join(self.project_root, "screenshots")
            filename = f"{sanitized_name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, filename)

            os.makedirs(screenshot_dir, exist_ok=True)
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved to: {screenshot_path}")
            return screenshot_path

        except WebDriverException as e:
            logger.error(f"Browser screenshot failed: {str(e)}")
            raise PageOperationError("Screenshot capture failed") from e
        except OSError as e:
            logger.error(f"File system error: {str(e)}")
            raise PageOperationError("Screenshot storage failed") from e

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize strings for filesystem-safe filenames"""
        return "".join([c if c.isalnum() or c in ('_', '-') else '_' for c in name])

    @property
    def project_root(self) -> str:
        """Get absolute path to project root directory"""
        try:
            return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        except Exception as e:
            logger.error(f"Project root resolution failed: {str(e)}")
            raise PageOperationError("Path resolution error") from e

    def get_video_element(self, timeout: int = 20) -> WebElement:
        """Locate and return the video player element, ensuring the video is playing.
        """
        try:
            logger.info("Attempting to locate video player")
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.VIDEO_CONTAINER_LOCATOR)
            )
            video_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.VIDEO_ELEMENT_LOCATOR)
            )
            WebDriverWait(self.driver, timeout).until(
                lambda d: video_element.get_attribute('readyState') == '4'
            )
            logger.info("Video element located and ready")
            return video_element
        except TimeoutException as e:
            error_msg = "Video element not found or not ready within timeout"
            logger.error(error_msg)
            raise PageOperationError(error_msg) from e
        except WebDriverException as e:
            error_msg = f"Failed to locate video element: {str(e)}"
            logger.error(error_msg)
            raise PageOperationError(error_msg) from e