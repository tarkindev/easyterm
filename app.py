"""daily-tui — personal command-driven dashboard.

Run with: python app.py
"""

from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Header, Footer, Input, RichLog

from homepage import Homepage
from commands import dispatch


class DailyTUI(App):
    CSS = """
    Screen {
        background: #0a0e14;
    }

    Header {
        background: #0d1117;
        color: #39ff9d;
        text-style: bold;
    }

    Footer {
        background: #0d1117;
        color: #6e7681;
    }

    #main-scroll {
        height: 1fr;
    }

    Homepage {
        height: auto;
        border: round #39ff9d;
        margin: 1 2 1 2;
        padding: 1 2;
        background: #0d1117;
    }

    Homepage Horizontal {
        height: auto;
    }

    #banner {
        height: auto;
        margin-bottom: 1;
        content-align: center middle;
    }

    #stats-panel, #help-panel {
        height: auto;
        padding: 0 2;
        color: #c9d1d9;
    }

    #stats-panel {
        width: 1fr;
        border-right: solid #21262d;
    }

    #help-panel {
        width: 2fr;
    }

    RichLog {
        border: round #1f6feb;
        margin: 0 2 1 2;
        padding: 0 1;
        background: #0d1117;
        color: #c9d1d9;
        min-height: 8;
    }

    Input {
        dock: bottom;
        margin: 0 2 1 2;
        border: round #39ff9d;
        background: #0d1117;
        color: #39ff9d;
    }

    Input:focus {
        border: round #7ee787;
    }
    """

    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(id="main-scroll"):
            yield Homepage()
            yield RichLog(id="output", wrap=True, markup=True)
        yield Input(placeholder="❯ Type a command (try 'help')...", id="command-input")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "⚡ EASYTERM"
        self.sub_title = "your day, one keystroke away"
        log = self.query_one("#output", RichLog)
        log.write("[#7ee787]Welcome. Type 'help' to see what I can do.[/#7ee787]")
        self.query_one(Input).focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value
        event.input.value = ""

        log = self.query_one("#output", RichLog)
        log.write(f"[bold #39ff9d]❯[/bold #39ff9d] {text}")

        result = await dispatch(text)

        if result == "__QUIT__":
            self.exit()
            return

        if result:
            log.write(result)

        self.query_one(Homepage).refresh_stats()
        self.query_one("#main-scroll").scroll_end(animate=False)


if __name__ == "__main__":
    DailyTUI().run()