"""Todo list. Persisted to todos.json so it survives across app runs
(unlike the rest of the app's in-memory session state).
"""

import json
from pathlib import Path

TODO_PATH = Path(__file__).parent.parent / "todos.json"


def _load() -> list[dict]:
    if not TODO_PATH.exists():
        return []
    try:
        with open(TODO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save(todos: list[dict]) -> None:
    with open(TODO_PATH, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)


async def handle(args: list[str]) -> str:
    if not args:
        return await list_todos()

    sub = args[0].lower()
    rest = args[1:]

    if sub == "add":
        return await add(" ".join(rest))
    elif sub == "done":
        return await mark_done(rest[0] if rest else None)
    elif sub == "remove" or sub == "rm":
        return await remove(rest[0] if rest else None)
    elif sub == "clear":
        return await clear_done()
    elif sub == "list":
        return await list_todos()
    else:
        # treat unrecognized first word as the start of a task to add,
        # e.g. "todo buy milk" instead of requiring "todo add buy milk"
        return await add(" ".join(args))


async def add(task: str) -> str:
    if not task:
        return "Usage: todo add <task>"
    todos = _load()
    todos.append({"task": task, "done": False})
    _save(todos)
    return f"Added: {task}"


async def list_todos() -> str:
    todos = _load()
    if not todos:
        return "No todos yet. Add one with: todo add <task>"
    lines = []
    for i, t in enumerate(todos, 1):
        mark = "x" if t["done"] else " "
        lines.append(f"[{mark}] {i}. {t['task']}")
    return "\n".join(lines)


async def mark_done(index_str: str | None) -> str:
    if index_str is None:
        return "Usage: todo done <number>"
    todos = _load()
    idx = _parse_index(index_str, len(todos))
    if idx is None:
        return f"No todo #{index_str}"
    todos[idx]["done"] = True
    _save(todos)
    return f"Marked done: {todos[idx]['task']}"


async def remove(index_str: str | None) -> str:
    if index_str is None:
        return "Usage: todo remove <number>"
    todos = _load()
    idx = _parse_index(index_str, len(todos))
    if idx is None:
        return f"No todo #{index_str}"
    removed = todos.pop(idx)
    _save(todos)
    return f"Removed: {removed['task']}"


async def clear_done() -> str:
    todos = _load()
    remaining = [t for t in todos if not t["done"]]
    cleared = len(todos) - len(remaining)
    _save(remaining)
    return f"Cleared {cleared} completed todo(s)"


def _parse_index(index_str: str, length: int) -> int | None:
    try:
        idx = int(index_str) - 1
    except ValueError:
        return None
    if 0 <= idx < length:
        return idx
    return None