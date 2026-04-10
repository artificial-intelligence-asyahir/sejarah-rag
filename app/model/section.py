from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Section:
    id: UUID
    book_id: UUID
    chapter_id: UUID
    section: str
    section_title: str
    content: str
    inserted_datetime: datetime