from dataclasses import dataclass

@dataclass
class Chunk:
    contents: list[str]
    payload: dict