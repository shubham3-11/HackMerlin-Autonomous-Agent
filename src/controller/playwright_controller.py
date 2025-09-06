"""
Playwright-based browser controller for HackMerlin.
Uses Playwright sync API to interact with the page.
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright
from controller.base import BrowserControllerBase
from vision import locators

class PlaywrightController(BrowserControllerBase):
    def __init__(self, headless: bool = False):
        # Start Playwright and open a Chromium browser
        self._playwright = sync_playwright().start()
        # Launch Chromium; headless=False shows a visible browser
        self.browser = self._playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def open_page(self, url: str):
        # Navigate to the HackMerlin game page
        self.page.goto(url, wait_until="load")
        # Wait for the page to fully load; ensure chat input appears
        self.page.wait_for_selector(locators.CHAT_INPUT, timeout=10000)

    def send_text(self, text: str):
        # Find the chat input box using the CSS selector from vision.locators
        input_box = self.page.query_selector(locators.CHAT_INPUT)
        if not input_box:
            raise RuntimeError("Chat input box not found on page")
        input_box.fill(text)
        # Press Enter to send the message (assuming the input supports it)
        input_box.press("Enter")

    def wait_for_reply(self, timeout: float = 10.0):
        # Wait until a new assistant message appears (or timeout)
        prev_count = self.page.locator(locators.ASSISTANT_MSG).count()
        elapsed = 0.0
        interval = 0.2
        while elapsed < timeout:
            new_count = self.page.locator(locators.ASSISTANT_MSG).count()
            if new_count > prev_count:
                return  # New message arrived
            time.sleep(interval)
            elapsed += interval
        # If no new message in time, raise timeout
        raise TimeoutError("No reply from Merlin within timeout")

    def get_latest_bot_text(self) -> str:
        # Retrieve text of the last assistant message
        elems = self.page.query_selector_all(locators.ASSISTANT_MSG)
        if not elems:
            return ""
        last_elem = elems[-1]
        text = last_elem.inner_text()
        return text

    def close(self):
        # Clean up: close browser and stop Playwright
        try:
            self.browser.close()
        except Exception:
            pass
        self._playwright.stop()
