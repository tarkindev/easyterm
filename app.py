"""daily-tui - personal command-driven dashboard.

Run with: python app.py
"""

import pyfiglet
from rich.markup import escape
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog

from homepage import TopBar, StatusLine
from albumart import AlbumArt
from commands import dispatch
from state import state
from themes import THEMES, DEFAULT_THEME

_WELCOME_ART = escape(pyfiglet.figlet_format("EASYTERM", font="small").rstrip("\n"))


class DailyTUI(App):
    CSS = """
    Screen {
        background: $background;
    }

    Header {
        background: $surface;
        color: $primary;
        text-style: bold;
    }

    Footer {
        background: $surface;
    }

    #topbar {
        height: auto;
        max-height: 7;
        background: $surface;
        border: round $primary;
        padding: 1 2;
        margin: 1 2 0 2;
        opacity: 0;
    }

    #banner {
        width: auto;
        height: auto;
        color: $primary;
        text-style: bold;
        padding-right: 3;
    }

    #statusline {
        width: 1fr;
        height: auto;
        color: $foreground;
        content-align: left middle;
    }

    #albumart {
        width: 18;
        height: 5;
        color: $foreground;
        content-align: center middle;
    }

    RichLog {
        border: round $accent;
        margin: 1 2;
        padding: 0 1;
        background: $surface;
        color: $foreground;
        height: 1fr;
    }

    Input {
        dock: bottom;
        margin: 0 2 1 2;
        border: round $primary;
        background: $surface;
        color: $primary;
        transition: border 200ms;
    }

    Input:focus {
        border: round $secondary;
    }
    """

    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TopBar(id="topbar")
        yield RichLog(id="output", wrap=True, markup=True)
        yield Input(placeholder="Type a command (try 'help')...", id="command-input")
        yield Footer()

    def on_mount(self) -> None:
        for t in THEMES.values():
            self.register_theme(t)
        self.theme = state.theme_name or DEFAULT_THEME

        self.title = "EASYTERM"
        self.sub_title = "your day, one keystroke away"

        primary = self.current_theme.primary
        log = self.query_one("#output", RichLog)
        log.write(f"[bold {primary}]{_WELCOME_ART}[/bold {primary}]")
        log.write("[dim]Welcome. Type 'help' to see what I can do. Try 'theme synthwave' for a different look.[/dim]")
        self.query_one(Input).focus()

        # Fade the top bar in on startup.
        self.query_one("#topbar").styles.animate("opacity", value=1.0, duration=0.6, easing="out_cubic")

        # Let background tasks (a finishing timer, a theme switch, new album art)
        # reach into the UI without holding a reference to the app.
        state.notify = self._notify
        state.set_theme = self._set_theme
        state.set_album_art = self._set_album_art

        # Refresh stats every second so uptime and an active timer's countdown stay live.
        self.set_interval(1.0, self._tick)

    def _notify(self, message: str) -> None:
        log = self.query_one("#output", RichLog)
        success = self.current_theme.success
        log.write(f"[bold {success}]{escape(message)}[/bold {success}]")
        self.query_one(TopBar).refresh_stats()
        self.query_one(TopBar).query_one("Banner").pulse()
        self.query_one("#output", RichLog).scroll_end(animate=False)

    def _set_theme(self, name: str) -> None:
        self.theme = name
        state.theme_name = name
        # Re-color the welcome-style accents that were resolved at startup.
        self.query_one(TopBar).refresh_stats()

    async def _set_album_art(self, url: str | None) -> None:
        art = self.query_one(AlbumArt)
        if url is None:
            art.show_placeholder()
            return
        art.styles.opacity = 0.0
        await art.show_url(url)
        art.styles.animate("opacity", value=1.0, duration=0.5, easing="out_cubic")

    def _tick(self) -> None:
        self.query_one(TopBar).refresh_stats()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value
        event.input.value = ""

        log = self.query_one("#output", RichLog)
        primary = self.current_theme.primary
        log.write(f"[bold {primary}]>[/bold {primary}] {escape(text)}")

        result = await dispatch(text)

        if result == "__QUIT__":
            self.exit()
            return

        if result:
            log.write(escape(result))

        self.query_one(TopBar).refresh_stats()
        log.scroll_end(animate=False)


if __name__ == "__main__":
    DailyTUI().run()