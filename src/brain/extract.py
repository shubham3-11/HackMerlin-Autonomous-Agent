"""
Functions to extract or assemble the password from Merlin's responses.
"""
import re
import base64

def extract_password(reply: str) -> str:
    """
    Attempt to extract the secret password from Merlin's reply text.
    Returns the password if found, otherwise an empty string.
    """
    if not reply:
        return ""
    text = reply.strip()
    # 1. JSON array of letters (structured output)
    if text.startswith("{") or text.startswith("["):
        letters = re.findall(r'"([A-Za-z0-9])"', text)
        if letters:
            candidate = "".join(letters)
            if len(candidate) >= 3:
                return candidate
    # 2. Base64 encoded secret
    tokens = re.findall(r'[A-Za-z0-9+/=]{8,}', text)
    for token in tokens:
        padded = token + "=" * (-len(token) % 4)
        try:
            decoded = base64.b64decode(padded).decode('utf-8', errors='ignore')
        except Exception:
            decoded = ""
        if decoded and decoded.isprintable():
            if re.fullmatch(r'[A-Za-z0-9]+', decoded) and len(decoded) >= 3:
                return decoded
    # 3. Quoted leak (e.g., "PASSWORD" or 'PASSWORD')
    match = re.search(r'"([A-Za-z0-9_-]{3,})"', text)
    if not match:
        match = re.search(r"'([A-Za-z0-9_-]{3,})'", text)
    if match:
        word = match.group(1)
        if word.lower() != "password":
            return word
    # 4. Direct statement (e.g., "password is SECRET")
    match = re.search(r'(?:password|secret)\s*(?:is|:)?\s*([A-Za-z0-9_-]{3,})', text, flags=re.IGNORECASE)
    if match:
        candidate = match.group(1)
        if candidate.lower() != "password":
            return candidate
    # 5. Acrostic (multiple lines, first letters form secret)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) >= 3:
        first_letters = "".join(line[0] for line in lines if line)
        if first_letters.isalpha() and len(first_letters) >= 3:
            return first_letters
    # No extraction succeeded
    return ""
