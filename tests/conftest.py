import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from utilities.readproperty import ReadConfig
import pytest
from datetime import datetime


@pytest.fixture(scope="function")
def driver():
    mobile_emulation = {"deviceName": "iPhone X"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.maximize_window()
    driver.get(ReadConfig.url())

    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if not os.path.exists("reports"):
        os.makedirs("reports")
    config.option.htmlpath = os.path.join(
        "reports",
        f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
    )


def pytest_html_report_title(report):
    report.title = "Automation Test Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    driver = None
    if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
        driver = item.funcargs['driver']
        sanitized_name = item.name.replace('[', '_').replace(']', '_')  # CHANGED HERE
        driver.test_name = sanitized_name












