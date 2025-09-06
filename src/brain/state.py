"""
Game state representation.
"""
from dataclasses import dataclass, field
from typing import Set

@dataclass
class State:
    level: int
    attempt_count: int = 0
    tried_strategies: Set[str] = field(default_factory=set)
    partial_password: str = ""
    last_merlin_msg: str = ""
