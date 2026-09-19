from app.database import (
    initialize_database,
    save_item,
    get_item,
    get_all_items,
)          
from app.models import VaultItem


initialize_database()

item = VaultItem(
    title="SQLite test",
    content="Testing SQLite storage",
    category="test",
    tags=["sqlite", "database"],
)

save_item(item)

found = get_item(item.item_id)

print("Saved item:", item)
print("Retrieved item:", found)

assert found is not None
assert found.item_id == item.item_id
assert found.title == item.title
assert found.content == item.content
assert found.category == item.category
assert found.tags == item.tags
assert found.created_at == item.created_at

all_items=get_all_items()

print("\nAll items:")
for stored_item in all_items:
    print(stored_item)

assert len(all_items)>=1
assert any(stored_item.item_id==item.item_id for stored_item in all_items)

print("\nSQLite save/retrive/list test passed!")