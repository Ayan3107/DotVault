import json
import os
import sqlite3
from pathlib import Path

from app.models import VaultItem


# ---------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATABASE_FILE = DATA_DIR / "dotvault.db"


# ---------------------------------------------------------
# SQLITE - LOCAL DEVELOPMENT
# ---------------------------------------------------------

def get_sqlite_connection():
    DATA_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DATABASE_FILE)


# ---------------------------------------------------------
# POSTGRES - PRODUCTION
# ---------------------------------------------------------

def get_postgres_connection():
    import psycopg

    return psycopg.connect(DATABASE_URL)


# ---------------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------------

def initialize_database() -> None:

    if DATABASE_URL:

        connection = get_postgres_connection()

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

    else:

        connection = get_sqlite_connection()

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


# ---------------------------------------------------------
# SAVE ITEM
# ---------------------------------------------------------

def save_item(item: VaultItem) -> None:

    if DATABASE_URL:

        connection = get_postgres_connection()

        connection.execute(
            """
            INSERT INTO vault_items
            (item_id, title, content, category, tags, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
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

    else:

        connection = get_sqlite_connection()

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


# ---------------------------------------------------------
# GET ONE ITEM
# ---------------------------------------------------------

def get_item(item_id: str) -> VaultItem | None:

    if DATABASE_URL:

        connection = get_postgres_connection()

        row = connection.execute(
            """
            SELECT item_id, title, content, category, tags, created_at
            FROM vault_items
            WHERE item_id = %s
            """,
            (item_id,),
        ).fetchone()

        connection.close()

    else:

        connection = get_sqlite_connection()

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


# ---------------------------------------------------------
# GET ALL ITEMS
# ---------------------------------------------------------

def get_all_items() -> list[VaultItem]:

    if DATABASE_URL:

        connection = get_postgres_connection()

        rows = connection.execute(
            """
            SELECT item_id, title, content, category, tags, created_at
            FROM vault_items
            ORDER BY created_at DESC
            """
        ).fetchall()

        connection.close()

    else:

        connection = get_sqlite_connection()

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


# ---------------------------------------------------------
# UPDATE ITEM
# ---------------------------------------------------------

def update_item(item: VaultItem) -> bool:

    if DATABASE_URL:

        connection = get_postgres_connection()

        cursor = connection.execute(
            """
            UPDATE vault_items
            SET title = %s,
                content = %s,
                category = %s,
                tags = %s,
                created_at = %s
            WHERE item_id = %s
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

    else:

        connection = get_sqlite_connection()

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


# ---------------------------------------------------------
# DELETE ITEM
# ---------------------------------------------------------

def delete_item(item_id: str) -> bool:

    if DATABASE_URL:

        connection = get_postgres_connection()

        cursor = connection.execute(
            """
            DELETE FROM vault_items
            WHERE item_id = %s
            """,
            (item_id,),
        )

        connection.commit()
        connection.close()

    else:

        connection = get_sqlite_connection()

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