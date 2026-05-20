from dataclasses import dataclass, field

from bson import ObjectId


@dataclass
class Section:
    book_id: ObjectId
    chapter_id: ObjectId
    section_no: float
    title: str
    content: str
    _id: ObjectId = field(default_factory=ObjectId)