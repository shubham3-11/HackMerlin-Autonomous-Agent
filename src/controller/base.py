"""
Base interface for browser controllers (Playwright/Selenium).
Defines the methods that concrete controllers must implement.
"""
from abc import ABC, abstractmethod

class BrowserControllerBase(ABC):
    """Abstract base class defining browser automation interface."""

    @abstractmethod
    def open_page(self, url: str):
        """Open the HackMerlin game page in the browser and wait for it to load."""
        pass

    @abstractmethod
    def send_text(self, text: str):
        """Send the given text to the chat input (and submit it)."""
        pass

    @abstractmethod
    def wait_for_reply(self, timeout: float = 10.0):
        """Wait until a new response from Merlin appears (or timeout in seconds)."""
        pass

    @abstractmethod
    def get_latest_bot_text(self) -> str:
        """Retrieve the text content of Merlin's latest response message."""
        pass

    @abstractmethod
    def close(self):
        """Cleanup and close the browser."""
        pass
