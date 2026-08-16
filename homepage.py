"""Homepage widget: the dashboard shown on launch and refreshed by 'stats'."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static

from state import state
from commands import HELP_TEXT


class StatsPanel(Static):
    """Left panel: live session stats."""

    def refresh_stats(self) -> None:
        unread = state.unread_email_count if state.unread_email_count is not None else "not checked"
        track = state.current_track or "none"
        content = (
            f"[b]SESSION[/b]\n"
            f"Uptime        {state.uptime_str()}\n"
            f"Commands run  {state.commands_run}\n\n"
            f"[b]LIVE[/b]\n"
            f"Unread email  {unread}\n"
            f"Now playing   {track}\n"
        )
        self.update(content)


class HelpPanel(Static):
    """Right panel: static command reference."""

    def on_mount(self) -> None:
        self.update(f"[b]COMMANDS[/b]\n{HELP_TEXT}")


class Homepage(Vertical):
    """Container combining stats + help side by side."""

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield StatsPanel(id="stats-panel")
            yield HelpPanel(id="help-panel")

    def refresh_stats(self) -> None:
        self.query_one(StatsPanel).refresh_stats()