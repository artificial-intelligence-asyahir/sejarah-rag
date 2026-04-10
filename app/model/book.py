from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Book:
    id: UUID
    title: str
    year: str
    inserted_datetime: datetime
    author: str = 'Kementerian Pendidikan Malaysia (KPM)'

