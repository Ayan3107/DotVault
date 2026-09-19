import json
import os

import psycopg

from app.models import VaultItem


DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable is not configured."
        )

    return psycopg.connect(DATABASE_URL)


def initialize_database() -> None:
    with get_connection() as connection:
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


def save_item(item: VaultItem) -> None:
    with get_connection() as connection:
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


def get_item(item_id: str) -> VaultItem | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT item_id, title, content, category, tags, created_at
            FROM vault_items
            WHERE item_id = %s
            """,
            (item_id,),
        ).fetchone()

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
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT item_id, title, content, category, tags, created_at
            FROM vault_items
            ORDER BY created_at DESC
            """
        ).fetchall()

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
    with get_connection() as connection:
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

        return cursor.rowcount > 0


def delete_item(item_id: str) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM vault_items
            WHERE item_id = %s
            """,
            (item_id,),
        )

        return cursor.rowcount > 0