"""In-memory session state. Nothing here persists between runs (single-session app)."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Awaitable, Callable, Optional

from themes import DEFAULT_THEME


@dataclass
class SessionState:
    started_at: datetime = field(default_factory=datetime.now)
    unread_email_count: int | None = None       # None = not checked yet this session
    current_track: str | None = None
    last_command: str | None = None
    commands_run: int = 0
    theme_name: str = DEFAULT_THEME

    # Timer module state
    active_timer_label: str | None = None
    active_timer_finish: datetime | None = None
    timers_completed: int = 0

    # Set by app.py on startup. Lets background tasks (like a finishing timer)
    # push a message into the output log without holding a reference to the app.
    notify: Optional[Callable[[str], None]] = None

    # Set by app.py on startup. Switches the live theme by name.
    set_theme: Optional[Callable[[str], None]] = None

    # Set by app.py on startup. Pass an image URL (or None to clear) to
    # render/hide the album art widget. Async since it downloads the image.
    set_album_art: Optional[Callable[[str | None], Awaitable[None]]] = None

    def uptime_str(self) -> str:
        delta = datetime.now() - self.started_at
        minutes, seconds = divmod(int(delta.total_seconds()), 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours}h {minutes}m"
        if minutes:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"

    def timer_str(self) -> str:
        if not self.active_timer_label or not self.active_timer_finish:
            return "none"
        remaining = (self.active_timer_finish - datetime.now()).total_seconds()
        if remaining <= 0:
            return "finishing..."
        minutes, seconds = divmod(int(remaining), 60)
        return f"{self.active_timer_label} ({minutes}m {seconds}s left)"


# Single shared instance for the app's lifetime
state = SessionState()