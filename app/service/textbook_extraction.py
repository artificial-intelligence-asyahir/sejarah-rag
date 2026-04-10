import uuid
from datetime import datetime
from uuid import uuid5

import pymupdf
import pymupdf4llm
from sympy import true

from app.model.book import Book
from app.model.chapter import Chapter
from app.model.section import Section


def read_document(doc: pymupdf.Document | str = "../../data/sejarah_f1_example.pdf"):
    pages = pymupdf4llm.to_markdown(doc=doc, page_chunks=true)

    book = Book(id = uuid.uuid4(), title="Sejarah Tingkatan 1", inserted_datetime=datetime.now())
    chapter = Chapter(id=uuid.uuid4(), book_id=book.id, chapter="1", chapter_title="Mengenali Sejarah", inserted_datetime=datetime.now())

    for page in pages:
        section = Section(id=uuid.uuid4(), book_id=book.id, chapter_id=chapter.id)
        print(page)



if __name__ == "__main__":
    read_document()