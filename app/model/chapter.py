from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class Chapter:
    id: UUID
    book_id: UUID
    chapter: str
    chapter_title: str
    inserted_datetime: datetime