from app.models import VaultItem


item = VaultItem(
    title="Git status",
    content="git status",
    category="command",
    tags=["git", "terminal"],
)


print(item)
print()
print(item.to_dict())