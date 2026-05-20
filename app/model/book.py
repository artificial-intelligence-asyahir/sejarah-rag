from dataclasses import dataclass, field

from bson import ObjectId


@dataclass
class Book:
    title: str
    author: str
    _id: ObjectId = field(default_factory=ObjectId)

