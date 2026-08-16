"""Command dispatcher. Parses raw input text, routes to the right module.

Adding a new command later = write the handler, add one line to COMMANDS.
"""

from modules import spotify, email, launcher
from state import state

HELP_TEXT = """\
Commands:
  email              Check unread Gmail count
  spotify play [q]   Play track/artist
  spotify pause      Pause playback
  spotify next       Skip track
  spotify search <q> Search Spotify
  open <keyword>     Launch an app
  stats              Refresh dashboard
  help               Show this message
  quit / exit        Close the app
"""


async def show_help(args: list[str]) -> str:
    return HELP_TEXT


async def show_stats(args: list[str]) -> str:
    return (
        f"Uptime: {state.uptime_str()}  |  "
        f"Commands run: {state.commands_run}  |  "
        f"Unread email: {state.unread_email_count if state.unread_email_count is not None else 'not checked'}  |  "
        f"Current track: {state.current_track or 'none'}"
    )


COMMANDS = {
    "email": email.check_unread,
    "spotify": spotify.handle,
    "open": launcher.launch,
    "help": show_help,
    "stats": show_stats,
}


async def dispatch(raw_input: str) -> str:
    """Parse raw text, call the matching handler, return the result string."""
    raw_input = raw_input.strip()
    if not raw_input:
        return ""

    parts = raw_input.split()
    cmd, args = parts[0].lower(), parts[1:]

    state.commands_run += 1
    state.last_command = raw_input

    if cmd in ("quit", "exit"):
        return "__QUIT__"  # app.py checks for this sentinel

    handler = COMMANDS.get(cmd)
    if handler is None:
        return f"Unknown command: '{cmd}'. Type 'help' for a list of commands."

    return await handler(args)