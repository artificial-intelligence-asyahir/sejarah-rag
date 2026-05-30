from dataclasses import dataclass

from bson import ObjectId


@dataclass
class Metadata:
    book_id: ObjectId
    chapter_id: ObjectId
    section_id: ObjectId