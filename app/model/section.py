from dataclasses import dataclass
from uuid import UUID


@dataclass
class Section:
    id: UUID
    book_id: UUID
    chapter_id: UUID
    section: str
    title: str
    content: str