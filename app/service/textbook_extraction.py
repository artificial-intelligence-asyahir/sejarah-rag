import logging
import uuid
from datetime import datetime

import pymupdf
import pymupdf4llm
from sympy import true

from app.model.book import Book
from app.model.chapter import Chapter
from app.model.section import Section

logging.basicConfig(level=logging.INFO)

def read_document(doc: pymupdf.Document | str = "../../data/SEJARAH_F1.pdf"):
    logging.info("Start reading document: %s", doc)
    pages = pymupdf4llm.to_markdown(doc=doc, page_chunks=true)
    document_non_chunk = pymupdf4llm.to_markdown(doc=doc)
    print(document_non_chunk)

    book = Book(id = uuid.uuid4(), title="Sejarah Tingkatan 1", inserted_datetime=datetime.now())
    chapter = Chapter(id=uuid.uuid4(), book_id=book.id, chapter="1", chapter_title="Mengenali Sejarah", inserted_datetime=datetime.now())

    for page in pages:
        section = Section(id=uuid.uuid4(), book_id=book.id, chapter_id=chapter.id)

    logging.info("Complete reading document: %s", doc)


def get_book_metadata(document: pymupdf.Document) -> Book:
    # logging.info("Start getting book metadata: %s", document)

    metadata = document.metadata
    book = Book(id=uuid.uuid4(),
                title=metadata["title"],
                author=metadata["author"],
                subject=metadata["subject"],
                inserted_datetime=datetime.now())

    # logging.info("Complete getting book metadata: %s", book)
    return book

if __name__ == "__main__":
    document = pymupdf.open("../../textbooks/sejarah_tingkatan_1.pdf")
    book = get_book_metadata(document)
    read_document()