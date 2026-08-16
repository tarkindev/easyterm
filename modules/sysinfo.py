"""System stats: CPU, RAM, battery. Fully real via psutil, no stub."""

import psutil


async def handle(args: list[str]) -> str:
    cpu = psutil.cpu_percent(interval=0.3)
    mem = psutil.virtual_memory()

    lines = [
        f"CPU     {cpu:.0f}%",
        f"RAM     {mem.percent:.0f}%  ({_gb(mem.used)}GB / {_gb(mem.total)}GB)",
    ]

    disk = psutil.disk_usage("/")
    lines.append(f"Disk    {disk.percent:.0f}%  ({_gb(disk.used)}GB / {_gb(disk.total)}GB)")

    battery = psutil.sensors_battery()
    if battery is not None:
        status = "plugged in" if battery.power_plugged else "on battery"
        lines.append(f"Battery {battery.percent:.0f}%  ({status})")

    return "\n".join(lines)


def _gb(num_bytes: int) -> str:
    return f"{num_bytes / (1024 ** 3):.1f}"