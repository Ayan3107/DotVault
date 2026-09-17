from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import uuid4

@dataclass
class VaultItem:
    title: str
    content: str
    category: str
    item_id: str =field(default_factory=lambda: str(uuid4()))
    tags: List[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VaultItem":
        return cls(
            item_id=data.get("item_id",str(uuid4())),
            title=data["title"],
            content=data["content"],
            category=data["category"],
            tags=data.get("tags", []),
            created_at=data.get(
                "created_at",
                datetime.now().isoformat()
            ),
        )