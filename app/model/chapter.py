from dataclasses import dataclass, field
from bson import ObjectId


@dataclass
class Chapter:
    book_id: ObjectId
    chapter_no: int
    title: str
    summary: str
    _id: ObjectId = field(default_factory=ObjectId)