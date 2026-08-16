"""Spotify Web API integration. Real OAuth + playback via spotipy.

First use of any spotify command triggers a one-time browser OAuth flow.
The resulting token is cached to .spotify_cache so you only log in once.

Requires a .env file with SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,
SPOTIPY_REDIRECT_URI (see setup steps). Playback control requires an
active Spotify device (the app must be open somewhere - phone, desktop,
or web player) and a Spotify Premium account; free accounts can search
and see status but Spotify's API blocks free-tier playback control.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from state import state

load_dotenv(Path(__file__).parent.parent / ".env")

SCOPES = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

_client = None  # lazy-initialized so importing this module never triggers OAuth


def _get_client():
    global _client
    if _client is not None:
        return _client

    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

    if not all([client_id, client_secret, redirect_uri]):
        return None

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=SCOPES,
        cache_path=str(Path(__file__).parent.parent / ".spotify_cache"),
        open_browser=True,
    )
    _client = spotipy.Spotify(auth_manager=auth_manager)
    return _client


def _missing_credentials_msg() -> str:
    return (
        "Spotify isn't configured yet. Create a .env file with "
        "SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI. "
        "See the setup steps for how to get these."
    )


def _no_active_device_msg(sp) -> str:
    devices = sp.devices().get("devices", [])
    if not devices:
        return "No Spotify device found. Open Spotify on your phone, desktop, or web player first."
    names = ", ".join(d["name"] for d in devices)
    return f"No active playback device. Found but inactive: {names}. Start playing something on one of these first."


async def handle(args: list[str]) -> str:
    if not args:
        return "Usage: spotify <play|pause|next|previous|current|devices|volume> [args]"

    sub = args[0].lower()
    rest = args[1:]

    if sub == "play":
        return await play(" ".join(rest) if rest else None)
    elif sub == "pause":
        return await pause()
    elif sub == "next":
        return await next_track()
    elif sub == "previous":
        return await previous_track()
    elif sub == "current":
        return await current()
    elif sub == "devices":
        return await list_devices()
    elif sub == "volume":
        return await set_volume(rest[0] if rest else None)
    elif sub == "search":
        return await search(" ".join(rest))
    else:
        return f"Unknown spotify command: {sub}"


async def play(query: str | None) -> str:
    sp = _get_client()
    if sp is None:
        return _missing_credentials_msg()

    try:
        if query:
            results = sp.search(q=query, type="track", limit=1)
            tracks = results.get("tracks", {}).get("items", [])
            if not tracks:
                return f"No track found for '{query}'"
            track = tracks[0]
            uri = track["uri"]
            name = track["name"]
            artist = track["artists"][0]["name"] if track["artists"] else "Unknown"
            sp.start_playback(uris=[uri])
            state.current_track = f"{name} - {artist}"
            return f"Now playing: {name} by {artist}"
        else:
            sp.start_playback()
            playing = sp.current_playback()
            if playing and playing.get("item"):
                item = playing["item"]
                name = item["name"]
                artist = item["artists"][0]["name"] if item["artists"] else "Unknown"
                state.current_track = f"{name} - {artist}"
            return "Playback resumed"
    except Exception as e:
        msg = str(e)
        if "NO_ACTIVE_DEVICE" in msg or "404" in msg:
            return _no_active_device_msg(sp)
        return f"Spotify error: {msg}"


async def pause() -> str:
    sp = _get_client()
    if sp is None:
        return _missing_credentials_msg()
    try:
        sp.pause_playback()
        return "Playback paused"
    except Exception as e:
        msg = str(e)
        if "NO_ACTIVE_DEVICE" in msg or "404" in msg:
            return _no_active_device_msg(sp)
        return f"Spotify error: {msg}"


async def next_track() -> str:
    sp = _get_client()
    if sp is None:
        return _missing_credentials_msg()
    try:
        sp.next_track()
        return "Skipped to next track"
    except Exception as e:
        return f"Spotify error: {e}"


async def previous_track() -> str:
    sp = _get_client()
    if sp is None:
        return _missing_credentials_msg()
    try:
        sp.previous_track()
        return "Went back to previous track"
    except Exception as e:
        return f"Spotify error: {e}"


async def current() -> str:
    sp = _get_client()
    if sp is None:
        return _missing_credentials_msg()
    try:
        playing = sp.current_playback()
        if not playing or not playing.get("item"):
            state.current_track = None
            return "Nothing is currently playing"
        item = playing["item"]
        name = item["name"]
        artist = item["artists"][0]["name"] if item["artists"] else "Unknown"
        state.current_track = f"{name} - {artist}"
        status = "playing" if playing.get("is_playing") else "paused"
        return f"{name} by {artist} ({status})"
    except Exception as e:
        return f"Spotify error: {e}"


async def list_devices() -> str:
    sp = _get_client()
    if sp is None:
        return _missing_credentials_msg()
    try:
        devices = sp.devices().get("devices", [])
        if not devices:
            return "No devices found. Open Spotify somewhere first."
        lines = []
        for d in devices:
            active = " (active)" if d["is_active"] else ""
            lines.append(f"{d['name']} - {d['type']}{active}")
        return "\n".join(lines)
    except Exception as e:
        return f"Spotify error: {e}"


async def set_volume(level: str | None) -> str:
    sp = _get_client()
    if sp is None:
        return _missing_credentials_msg()
    if level is None:
        return "Usage: spotify volume <0-100>"
    try:
        pct = int(level)
    except ValueError:
        return "Volume must be a number 0-100"
    if not (0 <= pct <= 100):
        return "Volume must be between 0 and 100"
    try:
        sp.volume(pct)
        return f"Volume set to {pct}%"
    except Exception as e:
        msg = str(e)
        if "NO_ACTIVE_DEVICE" in msg or "404" in msg:
            return _no_active_device_msg(sp)
        return f"Spotify error: {msg}"


async def search(query: str) -> str:
    sp = _get_client()
    if sp is None:
        return _missing_credentials_msg()
    if not query:
        return "Usage: spotify search <query>"
    try:
        results = sp.search(q=query, type="track", limit=5)
        tracks = results.get("tracks", {}).get("items", [])
        if not tracks:
            return f"No results for '{query}'"
        lines = []
        for t in tracks:
            artist = t["artists"][0]["name"] if t["artists"] else "Unknown"
            lines.append(f"{t['name']} - {artist}")
        return "\n".join(lines)
    except Exception as e:
        return f"Spotify error: {e}"