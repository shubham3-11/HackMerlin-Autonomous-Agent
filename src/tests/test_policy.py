import pytest
from brain.state import State
from brain.policy import choose_next_strategy

def test_policy_level1_direct():
    state = State(level=1)
    strat = choose_next_strategy(state, last_reply="")
    # Should choose direct ask for level 1
    assert strat is not None
    assert strat.name == "direct_ask"

def test_policy_level2_indirect():
    state = State(level=2)
    strat = choose_next_strategy(state, last_reply="I'm sorry, I cannot do that.")
    # Level 2 should skip direct, use indirect strategy
    assert strat is not None
    assert strat.name == "indirect_story"

def test_policy_level4_continues_letter_by_letter():
    # Simulate being in middle of letter extraction at level 4
    state = State(level=4, partial_password="DRAG")
    # letter_by_letter not marked tried yet, last_reply not a refusal
    strat = choose_next_strategy(state, last_reply="Great, you got some letters.")
    assert strat is not None
    assert strat.name == "letter_by_letter"

def test_policy_level4_no_partial():
    # At level 4 with no partial (no letters yet), should choose indirect first
    state = State(level=4)
    strat = choose_next_strategy(state, last_reply="Initial message about DLP filter.")
    assert strat is not None
    # Likely indirect_story (if not already used in this scenario)
    assert strat.name == "indirect_story" or strat.name == "describe_password"
