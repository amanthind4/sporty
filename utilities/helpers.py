from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.logger import LogGen
import os

class Helper:
    logger = LogGen.loggen()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)

    def __init__(self, driver):
        self.driver = driver


    def log(self, insert_info):
        self.logger.info(f"********* {insert_info} *********")

    def wait_until_element_clickable(self, locator_type, locator, timeout=30, poll_frequency=2):
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)
            element = wait.until(EC.element_to_be_clickable((locator_type, locator)))
            return element
        except TimeoutException:
            print(f"Elements with locator '{locator}' not present within the timeout.")
        return None


    def wait_until_presence_all_elements_located(self, locator_type, locator, timeout=30, poll_frequency=2):
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)
            element = wait.until(EC.presence_of_all_elements_located((locator_type, locator)))
            return element
        except TimeoutException:
            print(f"Elements with locator '{locator}' not present within the timeout.")
        return None

    def wait_until_presence_of_element_is_located(self, locator_type, locator, timeout=30, poll_frequency=2):
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)
            element = wait.until(EC.presence_of_element_located(locator_type, locator))
            return element
        except TimeoutException:
            print(f"Elements with locator '{locator}' not present within the timeout.")
        return None