from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

mobile_emulation = {"deviceName": "iPhone X"}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)


driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=chrome_options
)

try:
    driver.get("https://www.twitch.tv")
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Accept']"))
        )
        accept_button.click()
    except:
        print("No Accept button found, skipping...")
    browse_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Browse']"))
    )
    browse_button.click()
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
    )
    search_box.send_keys("StarCraft II" + Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@src, 'live_user')]"))
    )
    viewport_height = driver.execute_script("return window.innerHeight")
    for _ in range(2):
        driver.execute_script(f"window.scrollBy(0, {viewport_height // 2})")
        time.sleep(2)
    streamers = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@src, 'live_user')]"))
    )

    if streamers:
        first_streamer = streamers[0]
        parent_element = first_streamer.find_element(By.XPATH, "./ancestor::button")

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", parent_element)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", parent_element)
        print("Clicked on the first live streamer.")
    time.sleep(3)
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    driver.save_screenshot("streamer_page.png")
    print("Screenshot saved as 'streamer_page.png'.")

finally:
    driver.quit()
