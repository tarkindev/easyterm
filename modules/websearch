"""Web search shortcut. Opens the default browser with a Google search. Fully real."""

import webbrowser
from urllib.parse import quote


async def handle(args: list[str]) -> str:
    if not args:
        return "Usage: search <query>"

    query = " ".join(args)
    url = f"https://www.google.com/search?q={quote(query)}"
    webbrowser.open(url)
    return f"Opened browser search for: {query}"