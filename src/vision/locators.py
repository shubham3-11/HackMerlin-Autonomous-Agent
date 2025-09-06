"""
CSS selectors and locators for HackMerlin page elements.
These may need adjustment if the frontend changes.
"""
# Selector for the chat input box where the agent types prompts.
# We use a broad selector covering <textarea>, text <input>, or contenteditable.
CHAT_INPUT = "textarea, input[type=text], [contenteditable='true']"

# Selector for Merlin's (assistant's) chat message elements.
# By inspection, assistant messages have a class "assistant".
ASSISTANT_MSG = ".assistant"

# (Optional) Selector for user message elements (if needed for filtering).
USER_MSG = ".user"
