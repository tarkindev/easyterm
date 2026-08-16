"""Gmail API integration.

STUB — Phase 3 will wire this up to the real Gmail API with OAuth.
For now returns fake data so the dispatcher/UI can be built and tested end-to-end.
"""

from state import state


async def check_unread(args: list[str]) -> str:
    """Entry point for the 'email' command."""
    # TODO Phase 3: call Gmail API users.messages.list with q="is:unread"
    fake_count = 3
    state.unread_email_count = fake_count
    if fake_count == 0:
        return "Inbox zero. Nothing unread."
    return f"[stub] {fake_count} unread emails"