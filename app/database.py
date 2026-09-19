import json
import sqlite3
from pathlib import Path

from app.models import VaultItem


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATABASE_FILE = DATA_DIR / "dotvault.db"


def initialize_database() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS vault_items (
            item_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            tags TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_item(item: VaultItem) -> None:
    connection = sqlite3.connect(DATABASE_FILE)

    connection.execute(
        """
        INSERT INTO vault_items
        (item_id, title, content, category, tags, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            item.item_id,
            item.title,
            item.content,
            item.category,
            json.dumps(item.tags),
            item.created_at,
        ),
    )

    connection.commit()
    connection.close()


def get_item(item_id: str) -> VaultItem | None:
    connection = sqlite3.connect(DATABASE_FILE)

    row = connection.execute(
        """
        SELECT item_id, title, content, category, tags, created_at
        FROM vault_items
        WHERE item_id = ?
        """,
        (item_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return VaultItem(
        item_id=row[0],
        title=row[1],
        content=row[2],
        category=row[3],
        tags=json.loads(row[4]),
        created_at=row[5],
    )
def get_all_items() -> list[VaultItem]:
    connection = sqlite3.connect(DATABASE_FILE)

    rows = connection.execute(
        """
        SELECT item_id, title, content, category, tags, created_at
        FROM vault_items
        ORDER BY created_at DESC
        """
    ).fetchall()

    connection.close()

    return [
        VaultItem(
            item_id=row[0],
            title=row[1],
            content=row[2],
            category=row[3],
            tags=json.loads(row[4]),
            created_at=row[5],
        )
        for row in rows
    ]
def update_item(item: VaultItem) -> bool:
    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.execute(
        """
        UPDATE vault_items
        SET title = ?,
            content = ?,
            category = ?,
            tags = ?,
            created_at = ?
        WHERE item_id = ?
        """,
        (
            item.title,
            item.content,
            item.category,
            json.dumps(item.tags),
            item.created_at,
            item.item_id,
        ),
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0


def delete_item(item_id: str) -> bool:
    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.execute(
        """
        DELETE FROM vault_items
        WHERE item_id = ?
        """,
        (item_id,),
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0