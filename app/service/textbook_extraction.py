import logging
import uuid
import pymupdf
import pymupdf4llm
import re

from sympy import true
from app.model.book import Book
from app.model.chapter import Chapter
from app.model.section import Section
from pymupdf import Document
from datetime import datetime

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

def test_document(document: Document):
    print("begin writing")

    # w:write b:binary
    out = open("../../data/output.md", "wb")
    doc = pymupdf4llm.to_markdown(document);
    print("my buku sejarah")
    print(doc)
    out.write(doc.encode("utf-8"))
    out.close()
    print("writing completed")


def get_book_metadata(metadata: dict) -> Book:
    logging.info("Start getting book metadata: %s", document)

    book = Book(id=uuid.uuid4(),
                title=metadata["title"],
                author=metadata["author"])

    logging.info("Complete getting book metadata: %s", book)
    return book

def get_chapter_metadata(metadata: dict, book_id: str, ) -> Chapter:

    subject = metadata["subject"]

    # \d: digit
    # \s: spaces
    # +: one or more occurrence
    # (): capture and group
    # .: any character
    # *: zero or more occurrence
    match = re.search(r'(\d+)\s+(.*)', subject)
    if match:
        chapter_number = int(match.group(1))
        chapter_title = str(match.group(2)).strip()

    chapter = Chapter(id=uuid.uuid4(),
                      book_id= book_id,
                      chapter = chapter_number,
                      title = chapter_title,
                      summary = "")

    print(chapter)
    return chapter

def get_toc(document: Document):
    toc = document.get_toc()
    print(toc)

if __name__ == "__main__":
    document = pymupdf.open("../../chapters/sejarah_tingkatan_1_bab_1_mengenali_sejarah.pdf")
    metadata = document.metadata
    book = get_book_metadata(metadata)
    chapter = get_chapter_metadata(metadata, book.id)




    # test_document(document)
    # read_document(document)
    # get_toc(document)