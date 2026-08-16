"""Clipboard copy. Fully real via pyperclip."""

import pyperclip


async def handle(args: list[str]) -> str:
    if not args:
        return "Usage: clip <text>"
    text = " ".join(args)
    try:
        pyperclip.copy(text)
        return f"Copied to clipboard: {text}"
    except Exception as e:
        return f"Clipboard error: {e}"