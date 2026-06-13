from dataclasses import dataclass


@dataclass
class Citation:
    book_title: str
    book_author: str
    chapter_no: int
    chapter_title: str
    section_no: int
    section_title: str