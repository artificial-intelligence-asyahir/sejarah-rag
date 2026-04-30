from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Book:
    id: UUID
    title: str
    author: str
    subject: str
    inserted_datetime: datetime

