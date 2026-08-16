"""Current date/time. Fully real, no stub."""

from datetime import datetime


async def handle(args: list[str]) -> str:
    now = datetime.now()
    return now.strftime("%A, %B %d %Y - %I:%M:%S %p").replace(" 0", " ")