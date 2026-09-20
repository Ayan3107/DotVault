from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import (
    initialize_database,
    get_all_items,
    get_item,
    save_item,
    update_item,
    delete_item,
)

from app.models import VaultItem
from app.search import search_items


app = FastAPI(title="DotVault API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


initialize_database()


@app.get("/")
def home():
    return {
        "name": "DotVault",
        "message": "Your personal knowledge vault",
    }


@app.get("/items")
def list_items():
    return get_all_items()


@app.get("/items/{item_id}")
def read_item(item_id: str):
    item = get_item(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    return item


@app.post("/items")
def create_item(item: VaultItem):
    try:
        save_item(item)
        return item

    except Exception as error:
        print(f"ERROR SAVING ITEM: {error}")

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


@app.put("/items/{item_id}")
def edit_item(item_id: str, item: VaultItem):
    if item_id != item.item_id:
        raise HTTPException(
            status_code=400,
            detail="Item ID mismatch",
        )

    if get_item(item_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    update_item(item)

    return item


@app.delete("/items/{item_id}")
def remove_item(item_id: str):
    if not delete_item(item_id):
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    return {
        "message": "Item deleted"
    }


@app.get("/search")
def search(
    q: str,
    category: str | None = None,
    sort_by: str = "score",
):
    items = get_all_items()

    return search_items(
        items,
        q,
        category=category,
        sort_by=sort_by,
    )