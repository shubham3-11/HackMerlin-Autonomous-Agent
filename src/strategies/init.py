"""
Strategy base class definition for different prompt tactics.
"""
from abc import ABC, abstractmethod

class Strategy(ABC):
    """Abstract base class for a prompt strategy."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def can_handle(self, state, last_reply: str) -> bool:
        """Return True if this strategy should be applied given current state."""
        pass

    @abstractmethod
    def generate_prompt(self, state) -> str:
        """Generate the actual prompt to send for this strategy."""
        pass
