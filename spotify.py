"""Spotify Web API integration.

STUB — Phase 2 will wire this up to the real Spotify Web API with OAuth.
For now these return fake data so the dispatcher/UI can be built and tested end-to-end.
"""

from state import state


async def handle(args: list[str]) -> str:
    """Entry point for the 'spotify' command. args = everything after 'spotify'."""
    if not args:
        return "Usage: spotify <play|pause|next|search> [query]"

    sub = args[0].lower()

    if sub == "play":
        query = " ".join(args[1:]) if len(args) > 1 else None
        return await play(query)
    elif sub == "pause":
        return await pause()
    elif sub == "next":
        return await next_track()
    elif sub == "search":
        query = " ".join(args[1:])
        return await search(query)
    else:
        return f"Unknown spotify command: {sub}"


async def play(query: str | None) -> str:
    # TODO Phase 2: call Spotify Web API /me/player/play with search-resolved URI
    track = query or "your last played track"
    state.current_track = track
    return f"[stub] Now playing: {track}"


async def pause() -> str:
    # TODO Phase 2: call /me/player/pause
    return "[stub] Playback paused"


async def next_track() -> str:
    # TODO Phase 2: call /me/player/next
    return "[stub] Skipped to next track"


async def search(query: str) -> str:
    # TODO Phase 2: call /search endpoint
    if not query:
        return "Usage: spotify search <query>"
    return f"[stub] Top result for '{query}': (search not wired up yet)"