import dataclasses
from app.model.book import Book
from app.model.chapter import Chapter
from app.model.section import Section
from app.repository.mongodb import connection, DATABASE_NAME

class TextbookRepository:
    def __init__(self):
        self.db = connection.get_database(DATABASE_NAME)
        self.books = self.db['books']
        self.chapters = self.db['chapters']
        self.sections = self.db['sections']

    def save_book(self, book: Book):
        book_dict = dataclasses.asdict(book)
        book_dict["id"] = str(book_dict["id"])
        self.books.update_one({"id": book_dict["id"]},
                              {"$set": book_dict},
                              upsert=True)

    def save_chapter(self, chapter: Chapter):
        chapter_dict = dataclasses.asdict(chapter)
        chapter_dict["id"] = str(chapter_dict["id"])
        chapter_dict["book_id"] = str(chapter_dict["book_id"]) if chapter_dict["book_id"] else None
        self.chapters.update_one({"id": chapter_dict["id"]},
                                 {"$set": chapter_dict},
                                 upsert=True)

    def save_sections(self, sections: list[Section]):
        for section in sections:
            section_dict = dataclasses.asdict(section)
            section_dict["id"] = str(section_dict["id"])
            section_dict["book_id"] = str(section_dict["book_id"]) if section_dict["book_id"] else None
            section_dict["chapter_id"] = str(section_dict["chapter_id"]) if section_dict["chapter_id"] else None
            self.sections.update_one({"id": section_dict["id"]}, {"$set": section_dict}, upsert=True)