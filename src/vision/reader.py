"""
Utility functions for reading content from the HackMerlin DOM.
""" 
from controller.base import BrowserControllerBase
from vision import locators

def wait_for_new_assistant(controller: BrowserControllerBase, prev_count: int, timeout: float = 10.0) -> bool:
    """
    Wait for a new assistant message beyond prev_count.
    Returns True if a new message appeared, False if timed out.
    """
    try:
        controller.wait_for_reply(timeout=timeout)
        return True
    except Exception:
        return False

def get_latest_assistant_message(controller: BrowserControllerBase) -> str:
    """
    Retrieve the latest assistant message text using the controller.
    """
    return controller.get_latest_bot_text()
