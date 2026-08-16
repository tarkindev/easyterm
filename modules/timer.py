"""Countdown timer. Runs in the background; notifies the log when it finishes.

Fully real - no stub. Uses asyncio.create_task so the UI stays responsive while it runs.
"""

import asyncio
from datetime import datetime, timedelta

from state import state


async def handle(args: list[str]) -> str:
    if not args:
        return "Usage: timer <minutes> [label]"

    try:
        minutes = float(args[0])
    except ValueError:
        return "Usage: timer <minutes> [label] - minutes must be a number"

    if minutes <= 0:
        return "Timer length must be greater than 0"

    label = " ".join(args[1:]) if len(args) > 1 else "Timer"
    seconds = minutes * 60

    state.active_timer_label = label
    state.active_timer_finish = datetime.now() + timedelta(seconds=seconds)

    asyncio.create_task(_run_timer(seconds, label))

    return f"{label} started for {_fmt_minutes(minutes)}. You'll be notified when it's done."


async def _run_timer(seconds: float, label: str) -> None:
    await asyncio.sleep(seconds)
    state.active_timer_label = None
    state.active_timer_finish = None
    state.timers_completed += 1
    if state.notify:
        state.notify(f"[bold #7ee787]Timer done:[/bold #7ee787] {label}")


def _fmt_minutes(minutes: float) -> str:
    if minutes == int(minutes):
        return f"{int(minutes)} min"
    return f"{minutes:g} min"