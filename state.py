"""In-memory session state. Nothing here persists between runs (single-session app)."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SessionState:
    started_at: datetime = field(default_factory=datetime.now)
    unread_email_count: int | None = None       # None = not checked yet this session
    current_track: str | None = None
    last_command: str | None = None
    commands_run: int = 0

    def uptime_str(self) -> str:
        delta = datetime.now() - self.started_at
        minutes, seconds = divmod(int(delta.total_seconds()), 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours}h {minutes}m"
        if minutes:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"


# Single shared instance for the app's lifetime
state = SessionState()