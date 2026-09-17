from app.models import VaultItem
from datetime import datetime
from app.search import search_items

items = [
    VaultItem(
            title="API request example",
            content="send a request using Python",
            category="api",
            tags=["requests"],
    ),
    VaultItem(
        title="Git status",
        content="git status",
        category="command",
        tags=["git", "terminal"],
    ),
    VaultItem(
        title="Python environment",
        content="create a virtual environment with venv",
        category="command",
        tags=["python"],
        created_at="2026-09-17T16:00:00",
    ),
    VaultItem(
        title="Python API request",
        content="send a request using Python",
        category="api",
        tags=["api", "requests"],
        created_at="2026-09-17T17:00:00"
    ),
]

results=search_items(items, "python")
print(results)

assert results[0][0] ==5
assert results[1][0] ==4
assert results[2][0] ==1

upper_results =search_items(items, "PYTHON")
assert upper_results[0][0] ==5

command_results = [
    item
    for score, item in results
    if item.category == "command"
]

assert len(command_results) == 1
assert command_results[0].title == "Python environment"

command_results =search_items(items, "python", category="command")

assert len(command_results) == 1
assert command_results[0][1].title == "Python environment"

missing_results =search_items(items,"python",category="regex")
assert len(missing_results) == 0

recent_results = search_items(items, "python", sort_by="recent")

assert recent_results[0][1].title == "Python API request"