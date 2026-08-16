"""Theme selector. Switches the app's live color theme."""

from state import state
from themes import THEMES


async def handle(args: list[str]) -> str:
    if not args:
        names = ", ".join(sorted(THEMES.keys()))
        return f"Current theme: {state.theme_name}\nAvailable: {names}\nUsage: theme <name>"

    name = args[0].lower()
    if name not in THEMES:
        names = ", ".join(sorted(THEMES.keys()))
        return f"Unknown theme '{name}'. Available: {names}"

    if state.set_theme is None:
        return "Theme system not ready yet"

    state.set_theme(name)
    return f"Theme switched to {name}"