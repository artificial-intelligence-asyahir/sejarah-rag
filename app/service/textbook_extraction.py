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

def read_document(doc: pymupdf.Document | str, book: Book):
    logging.info("Start reading document: %s", doc)
    pages = pymupdf4llm.to_markdown(doc=doc, page_chunks=true)
    document_non_chunk = pymupdf4llm.to_markdown(doc=doc)
    print(document_non_chunk)

    chapter = Chapter(id=uuid.uuid4(), book_id=book.id, chapter="1", chapter_title="Mengenali Sejarah", inserted_datetime=datetime.now())

    for page in pages:
        section = Section(id=uuid.uuid4(), book_id=book.id, chapter_id=chapter.id)

    logging.info("Complete reading document: %s", doc)

def test_document(document: pymupdf.Document):
    print("begin writing")

    # w:write b:binary
    out = open("../../data/output.md", "wb")
    doc = pymupdf4llm.to_markdown(document);
    print("my buku sejarah")
    print(doc)
    out.write(doc.encode("utf-8"))
    out.close()
    print("writing completed")


def get_book_metadata(document: pymupdf.Document) -> Book:
    logging.info("Start getting book metadata: %s", document)

    metadata = document.metadata
    book = Book(id=uuid.uuid4(),
                title=metadata["title"],
                author=metadata["author"],
                subject=metadata["subject"],
                inserted_datetime=datetime.now())

    logging.info("Complete getting book metadata: %s", book)
    return book


def get_toc(document: pymupdf.Document):
    toc = document.get_toc()
    print(toc)

if __name__ == "__main__":
    document = pymupdf.open("../../textbooks/sejarah_tingkatan_1.pdf")
    # book = get_book_metadata(document)
    # test_document(document)
    # read_document(document)
    # get_toc(document)