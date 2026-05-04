from pymupdf import Document
from app.model.book import Book

import logging
import uuid

class TextbookService:
    def __init__(self, doc: Document):
        self.doc = doc
        self.book = self.__get_book_metadata()

    def _get_book_metadata(self) -> Book:
        logging.info("Start getting book metadata: %s", self.doc)
        metadata = self.doc.metadata

        book = Book(id=uuid.uuid4(),
                    title=metadata["title"],
                    author=metadata["author"])

        logging.info("Complete getting book metadata: %s", book)
        return book





