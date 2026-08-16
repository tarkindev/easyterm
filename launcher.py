"""App launcher — fuzzy-matches a typed keyword against config.toml and launches it.

This one is fully implemented (no external API/OAuth needed), unlike spotify/email stubs.
"""

import difflib
import subprocess
import sys
import tomllib
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.toml"


def _load_launcher_config() -> tuple[dict[str, str], float]:
    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
    keywords = config.get("launcher", {})
    threshold = config.get("app", {}).get("fuzzy_match_threshold", 0.6)
    return keywords, threshold


async def launch(args: list[str]) -> str:
    """Entry point for the 'open' command. args = [keyword, ...]."""
    if not args:
        return "Usage: open <keyword>"

    query = args[0].lower()
    keywords, threshold = _load_launcher_config()

    if not keywords:
        return "No apps configured. Edit config.toml under [launcher]."

    # Exact match first
    if query in keywords:
        return _run(query, keywords[query])

    # Fuzzy match against configured keywords
    matches = difflib.get_close_matches(query, keywords.keys(), n=1, cutoff=threshold)
    if matches:
        best = matches[0]
        return _run(best, keywords[best])

    return f"No app matched '{query}'. Configured: {', '.join(keywords.keys())}"


def _run(keyword: str, path: str) -> str:
    try:
        if sys.platform == "win32":
            subprocess.Popen(path, shell=True)
        else:
            subprocess.Popen(path.split())
        return f"Launching {keyword}..."
    except Exception as e:
        return f"Failed to launch {keyword}: {e}"