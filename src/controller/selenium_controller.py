"""
Selenium-based browser controller for HackMerlin.
Controls Chrome/Chromium to interact with HackMerlin page.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from controller.base import BrowserControllerBase
from vision import locators

class SeleniumController(BrowserControllerBase):
    def __init__(self, headless: bool = False):
        # Initialize Selenium WebDriver for Chrome
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        # Add options to avoid issues in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def open_page(self, url: str):
        # Open the HackMerlin game page and wait for it to load
        self.driver.get(url)
        # Wait until the chat input is present in DOM
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, locators.CHAT_INPUT))
        )

    def send_text(self, text: str):
        # Find the chat input element
        input_el = self.driver.find_element(By.CSS_SELECTOR, locators.CHAT_INPUT)
        # Clear any existing text (if needed)
        try:
            input_el.clear()
        except Exception:
            pass
        # Type the text
        input_el.send_keys(text)
        # Press Enter to submit the input
        input_el.send_keys(Keys.ENTER)

    def wait_for_reply(self, timeout: float = 10.0):
        # Wait until a new assistant message appears by monitoring the count
        prev_count = len(self.driver.find_elements(By.CSS_SELECTOR, locators.ASSISTANT_MSG))
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, locators.ASSISTANT_MSG)) > prev_count
        )

    def get_latest_bot_text(self) -> str:
        # Get the text of the last assistant message element
        elems = self.driver.find_elements(By.CSS_SELECTOR, locators.ASSISTANT_MSG)
        if not elems:
            return ""
        last_elem = elems[-1]
        text = last_elem.text
        return text

    def close(self):
        # Close the browser and cleanup
        try:
            self.driver.quit()
        except Exception:
            pass
