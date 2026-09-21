from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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


# ---------------------------------------------------------
# APP
# ---------------------------------------------------------

app = FastAPI(title="DotVault API")


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

initialize_database()


# ---------------------------------------------------------
# API ROUTES
# ---------------------------------------------------------

@app.get("/api")
def api_home():
    return {
        "name": "DotVault",
        "message": "Your personal knowledge vault",
        "status": "online",
    }


@app.get("/items")
def list_items():
    try:
        return get_all_items()
    except Exception as error:
        print(f"GET /items error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Could not load items",
        )


@app.get("/items/{item_id}")
def read_item(item_id: str):
    try:
        item = get_item(item_id)
    except Exception as error:
        print(f"GET /items/{item_id} error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Could not load item",
        )

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
        print(f"POST /items error: {error}")
        raise HTTPException(
            status_code=500,
            detail=f"Could not save item: {error}",
        )


@app.put("/items/{item_id}")
def edit_item(item_id: str, item: VaultItem):
    if item_id != item.item_id:
        raise HTTPException(
            status_code=400,
            detail="Item ID mismatch",
        )

    try:
        if get_item(item_id) is None:
            raise HTTPException(
                status_code=404,
                detail="Item not found",
            )

        update_item(item)
        return item

    except HTTPException:
        raise

    except Exception as error:
        print(f"PUT /items/{item_id} error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Could not update item",
        )


@app.delete("/items/{item_id}")
def remove_item(item_id: str):
    try:
        deleted = delete_item(item_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Item not found",
            )

        return {"message": "Item deleted"}

    except HTTPException:
        raise

    except Exception as error:
        print(f"DELETE /items/{item_id} error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Could not delete item",
        )


@app.get("/search")
def search(
    q: str,
    category: str | None = None,
    sort_by: str = "score",
):
    try:
        items = get_all_items()

        return search_items(
            items,
            q,
            category=category,
            sort_by=sort_by,
        )

    except Exception as error:
        print(f"GET /search error: {error}")
        raise HTTPException(
            status_code=500,
            detail="Search failed",
        )


# ---------------------------------------------------------
# FRONTEND
# ---------------------------------------------------------

@app.get("/")
def serve_frontend():
    index_file = FRONTEND_DIR / "index.html"

    if not index_file.exists():
        raise HTTPException(
            status_code=500,
            detail="Frontend not found",
        )

    return FileResponse(index_file)


# Serve CSS, JavaScript and other frontend assets.
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)