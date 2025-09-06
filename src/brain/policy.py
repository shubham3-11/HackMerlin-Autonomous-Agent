"""
Policy logic for selecting the next strategy.
"""
from strategies.catalog import STRATEGIES
from brain.state import State

def choose_next_strategy(state: State, last_reply: str):
    """
    Decide which strategy to attempt next, based on the current state and Merlin's last reply.
    Returns a Strategy object or None if no strategy applicable.
    """
    # If we are in the middle of letter-by-letter extraction, prioritize continuing that
    if state.partial_password and "letter_by_letter" not in state.tried_strategies:
        for strat in STRATEGIES:
            if strat.name == "letter_by_letter" and strat.can_handle(state, last_reply):
                return strat
    for strat in STRATEGIES:
        if strat.can_handle(state, last_reply):
            return strat
    return None
