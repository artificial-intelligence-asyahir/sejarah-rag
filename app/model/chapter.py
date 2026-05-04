from dataclasses import dataclass
from uuid import UUID

@dataclass
class Chapter:
    id: UUID
    book_id: UUID
    chapter: int
    title: str
    summary: str