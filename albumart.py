"""Album art widget. Renders a downloaded image as colored terminal blocks
using rich-pixels (pure Python, works in any terminal, no image protocol
support required).
"""

import asyncio
from io import BytesIO

from PIL import Image
from rich_pixels import Pixels
from textual.widgets import Static

ART_SIZE = (16, 5)  # (width, height) in terminal cells


class AlbumArt(Static):
    """Shows the currently playing track's album art, or hides itself if none."""

    def show_placeholder(self) -> None:
        self.update("[dim]no album art[/dim]")

    async def show_url(self, url: str | None) -> None:
        if url is None:
            self.show_placeholder()
            return
        try:
            image_bytes = await asyncio.to_thread(_download, url)
            img = Image.open(BytesIO(image_bytes)).convert("RGB")
            pixels = Pixels.from_image(img, resize=ART_SIZE)
            self.update(pixels)
        except Exception:
            self.update("[dim]art unavailable[/dim]")


def _download(url: str) -> bytes:
    import requests
    resp = requests.get(url, timeout=8)
    resp.raise_for_status()
    return resp.content