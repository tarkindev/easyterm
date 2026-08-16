"""Homepage widget: the dashboard shown on launch and refreshed by 'stats'."""

import pyfiglet
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static

from state import state
from commands import HELP_TEXT

_ascii_art = pyfiglet.figlet_format("EASYTERM", font="small").rstrip("\n")
BANNER = f"[bold #39ff9d]{_ascii_art}[/bold #39ff9d]"


class StatsPanel(Static):
    """Left panel: live session stats."""

    def on_mount(self) -> None:
        self.refresh_stats()

    def refresh_stats(self) -> None:
        unread = state.unread_email_count if state.unread_email_count is not None else "—"
        track = state.current_track or "—"
        content = (
            f"[bold #7ee787]◆ SESSION[/bold #7ee787]\n"
            f"[#6e7681]⏱[/#6e7681]  Uptime        [white]{state.uptime_str()}[/white]\n"
            f"[#6e7681]▸[/#6e7681]  Commands run  [white]{state.commands_run}[/white]\n\n"
            f"[bold #7ee787]◆ LIVE[/bold #7ee787]\n"
            f"[#6e7681]✉[/#6e7681]  Unread email  [white]{unread}[/white]\n"
            f"[#6e7681]♫[/#6e7681]  Now playing   [white]{track}[/white]\n"
        )
        self.update(content)


class HelpPanel(Static):
    """Right panel: static command reference."""

    def on_mount(self) -> None:
        lines = HELP_TEXT.strip().split("\n")
        formatted = "[bold #7ee787]◆ COMMANDS[/bold #7ee787]\n"
        for line in lines[1:]:  # skip the "Commands:" header line
            formatted += f"[#c9d1d9]{line}[/#c9d1d9]\n"
        self.update(formatted)


class Banner(Static):
    def on_mount(self) -> None:
        self.update(BANNER)


class Homepage(Vertical):
    """Container combining banner + stats/help side by side."""

    def compose(self) -> ComposeResult:
        yield Banner(id="banner")
        with Horizontal():
            yield StatsPanel(id="stats-panel")
            yield HelpPanel(id="help-panel")

    def refresh_stats(self) -> None:
        self.query_one(StatsPanel).refresh_stats()