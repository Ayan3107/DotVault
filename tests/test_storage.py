import tempfile
from pathlib import Path


import app.storage as storage
from app.models import VaultItem

add_item=storage.add_item
get_items=storage.get_items
get_items=storage.get_items
get_item=storage.get_item
update_item=storage.update_item
delete_item=storage.delete_item

with tempfile.TemporaryDirectory() as temp_dir:
    storage.DATA_DIR=Path(temp_dir)
    storage.VAULT_FILE=storage.DATA_DIR/"vault.json"


item = VaultItem(
    title="Python virtual environment",
    content="python -m venv .venv",
    category="command",
    tags=["python", "venv"],
)

add_item(item)

items = get_items()

print(f"Total items: {len(items)}")

for saved_item in items:
    print()
    print(f"Title: {saved_item.title}")
    print(f"Category: {saved_item.category}")
    print(f"Tags: {saved_item.tags}")
    print(f"ID: {saved_item.item_id}")

first_item=items[0]

found_item=get_item(first_item.item_id)

print()
print("Found by ID")
print(found_item)

found_item.title="Updated Python virtual environment"

updated=update_item(found_item)

print()
print(f"Updatesuccessful: {updated}")

updated_item=get_item(found_item.item_id)

print(f"Updated title: {updated_item.title}")

deleted=delete_item(found_item.item_id)

print()
print(f"Delete successful: {deleted}")

remaining_item=get_item(found_item.item_id)

print(f"Found after delete: {remaining_item}")