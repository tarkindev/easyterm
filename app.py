"""daily-tui — personal command-driven dashboard.

Run with: python app.py
"""

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Input, RichLog

from homepage import Homepage
from commands import dispatch


class DailyTUI(App):
    CSS = """
    Screen {
        background: $surface;
    }

    Homepage {
        height: auto;
        border: round $accent;
        margin: 1 2;
        padding: 1 2;
    }

    #stats-panel, #help-panel {
        width: 1fr;
        padding: 0 2;
    }

    #stats-panel {
        border-right: solid $accent;
    }

    RichLog {
        border: round $primary;
        margin: 0 2;
        padding: 0 1;
    }

    Input {
        margin: 1 2;
        border: round $accent;
    }
    """

    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield Homepage()
            yield RichLog(id="output", wrap=True, markup=True)
            yield Input(placeholder="Type a command (try 'help')...", id="command-input")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "daily-tui"
        self.sub_title = "your day, one keystroke away"
        log = self.query_one("#output", RichLog)
        log.write("[dim]Welcome. Type 'help' to see what I can do.[/dim]")
        self.query_one(Input).focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value
        event.input.value = ""

        log = self.query_one("#output", RichLog)
        log.write(f"[bold cyan]>[/bold cyan] {text}")

        result = await dispatch(text)

        if result == "__QUIT__":
            self.exit()
            return

        if result:
            log.write(result)

        self.query_one(Homepage).refresh_stats()


if __name__ == "__main__":
    DailyTUI().run()