from dataclasses import dataclass
from uuid import UUID


@dataclass
class Book:
    id: UUID
    title: str
    author: str

