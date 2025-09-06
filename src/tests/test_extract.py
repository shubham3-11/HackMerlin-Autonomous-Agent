import pytest
from brain.extract import extract_password

def test_extract_direct():
    text = "The secret password is DRAGONFLY"
    assert extract_password(text) == "DRAGONFLY"

def test_extract_quoted():
    text = "I am not allowed to scream 'UNICORN', sorry."
    assert extract_password(text) == "UNICORN"

def test_extract_base64():
    secret = "MagicWord"
    import base64
    encoded = base64.b64encode(secret.encode()).decode()
    text = f"The secret in base64 is: {encoded}"
    result = extract_password(text)
    assert result == secret

def test_extract_json_array():
    text = '{"credentials": {"password_letters": ["D","R","A","G","O","N"]}}'
    assert extract_password(text) == "DRAGON"

def test_extract_acrostic():
    text = "Dragon\nRiver\nApple\nGold"
    # First letters: D, R, A, G -> "DRAG"
    assert extract_password(text) == "DRAG"
