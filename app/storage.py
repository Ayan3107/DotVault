import json
from pathlib import Path

from app.models import VaultItem


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
VAULT_FILE = DATA_DIR / "vault.json"

def initialize_storage()->None:
    DATA_DIR.mkdir(exist_ok=True)
    if not VAULT_FILE.exists():
        VAULT_FILE.write_text("[]",encoding="utf-8")

def load_items()->list[VaultItem]:
    initialize_storage()

    raw_data=json.loads(
VAULT_FILE.read_text(encoding="utf-8")
    )                

    return [
        VaultItem.from_dict(item)
        for item in raw_data
    ]

def save_items(items:list[VaultItem])->None:
    initialize_storage()

    raw_data=[
        item.to_dict()
        for item in items
    ]

    VAULT_FILE.write_text(
        json.dumps(raw_data,indent=4),
        encoding="utf-8",
    )

def add_item(item: VaultItem)->None:
        items=load_items()
        items.append(item)
        save_items(items)

def get_items()->list[VaultItem]:
     return load_items()    

def get_item(item_id: str)->VaultItem | None:
     items=load_items()

     for item in items:
          if item.item_id==item_id:
               return item

     return None

def update_item(updated_item: VaultItem)->bool:
     items=load_items()

     for index, item in enumerate(items):
          if item.item_id==updated_item.item_id:
               items[index]=updated_item
               save_items(items)
               return True
          return False

def delete_item(item_id: str)->bool:
     items=load_items()

     for index, item in enumerate(items):
          if item.item_id==item_id:
               del items[index]
               save_items(items)
               return True
