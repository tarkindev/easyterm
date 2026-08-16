"""Top status bar: compact ASCII wordmark, live stats line, and album art.

Kept in homepage.py to avoid churning the repo's file layout, but this is
now a slim always-visible strip rather than a full dashboard - the bulky
version got replaced with something that leaves most of the screen to
the actual command output.
"""

import pyfiglet
from rich.markup import escape
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static

from state import state
from albumart import AlbumArt

_ascii_art = escape(pyfiglet.figlet_format("EASYTERM", font="mini").rstrip("\n"))


class Banner(Static):
    """Small persistent wordmark. Fades in once on mount; can pulse on events."""

    def on_mount(self) -> None:
        self.update(_ascii_art)

    def pulse(self) -> None:
        """Brief bounded flash - used for event feedback, never loops."""
        self.styles.animate("opacity", value=0.4, duration=0.15, easing="out_cubic", on_complete=self._pulse_back)

    def _pulse_back(self) -> None:
        self.styles.animate("opacity", value=1.0, duration=0.35, easing="out_cubic")


class StatusLine(Static):
    """Single-line live stats. Dim labels, bright values - reads fast."""

    def refresh_stats(self) -> None:
        unread = state.unread_email_count if state.unread_email_count is not None else "n/a"
        track = state.current_track or "none"
        parts = [
            f"[dim]uptime[/dim] {state.uptime_str()}",
            f"[dim]cmds[/dim] {state.commands_run}",
            f"[dim]mail[/dim] {unread}",
            f"[dim]track[/dim] {escape(track)}",
            f"[dim]timer[/dim] {escape(state.timer_str())}",
            f"[dim]theme[/dim] {state.theme_name}",
        ]
        self.update("   ".join(parts))


class TopBar(Horizontal):
    """Container combining banner + status line + album art."""

    def compose(self) -> ComposeResult:
        yield Banner(id="banner")
        yield StatusLine(id="statusline")
        yield AlbumArt(id="albumart")

    def on_mount(self) -> None:
        self.query_one(StatusLine).refresh_stats()
        self.query_one(AlbumArt).show_placeholder()

    def refresh_stats(self) -> None:
        self.query_one(StatusLine).refresh_stats()


# Kept as an alias so nothing else needs to change if it still imports Homepage.
Homepage = TopBar