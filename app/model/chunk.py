from dataclasses import dataclass
from uuid import UUID
from app.model.metadata import Metadata


@dataclass
class Chunk:
    id: UUID
    vector: float
    metadata: Metadata