"""Ping/network check. Fully real, uses the system ping command."""

import asyncio
import re
import sys


async def handle(args: list[str]) -> str:
    host = args[0] if args else "8.8.8.8"

    count_flag = "-n" if sys.platform == "win32" else "-c"
    cmd = ["ping", count_flag, "4", host]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)
    except asyncio.TimeoutError:
        return f"Ping to {host} timed out"
    except FileNotFoundError:
        return "ping command not found on this system"

    output = stdout.decode(errors="ignore")

    if proc.returncode != 0:
        return f"Could not reach {host}"

    times = re.findall(r"time[=<]([\d.]+)\s*ms", output)
    if times:
        floats = [float(t) for t in times]
        avg = sum(floats) / len(floats)
        return f"{host}: reachable, avg {avg:.0f}ms over {len(floats)} pings"

    return f"{host}: reachable"