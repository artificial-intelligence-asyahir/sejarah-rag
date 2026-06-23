import dataclasses

from bson import ObjectId

from app.model.book import Book
from app.model.chapter import Chapter
from app.model.chunk import Chunk
from app.model.section import Section
from app.repository.mongodb import connection, DATABASE_NAME

class TextbookRepository:
    def __init__(self):
        self.db = connection.get_database(DATABASE_NAME)
        self.books = self.db['books']
        self.chapters = self.db['chapters']
        self.sections = self.db['sections']
        self.chunks = self.db['chunks']
        self.evaluations = self.db['evaluations']

    def save_book(self, book: Book):
        book_dict = dataclasses.asdict(book)
        book_dict["_id"] = ObjectId(book_dict["_id"])
        self.books.update_one({"_id": book_dict["_id"]},
                              {"$set": book_dict},
                              upsert=True)

    def save_chapter(self, chapter: Chapter):
        chapter_dict = dataclasses.asdict(chapter)
        chapter_dict["_id"] = ObjectId(chapter_dict["_id"])
        chapter_dict["book_id"] = ObjectId(chapter_dict["book_id"]) if chapter_dict["book_id"] else None
        self.chapters.update_one({"_id": chapter_dict["_id"]},
                                 {"$set": chapter_dict},
                                 upsert=True)

    def save_sections(self, sections: list[Section]):
        for section in sections:
            section_dict = dataclasses.asdict(section)
            section_dict["_id"] = ObjectId(section_dict["_id"])
            section_dict["book_id"] = ObjectId(section_dict["book_id"]) if section_dict["book_id"] else None
            section_dict["chapter_id"] = ObjectId(section_dict["chapter_id"]) if section_dict["chapter_id"] else None
            self.sections.update_one({"_id": section_dict["_id"]}, {"$set": section_dict}, upsert=True)

    def find_book_by_title(self, name: str):
        return self.books.find_one({"title": name})

    def find_book_by_id(self, id: str | ObjectId):
        if isinstance(id, str):
            id = ObjectId(id)
        return self.books.find_one({"_id": id})

    def find_chapter_by_chapter_no_and_book_id(self, chapter_no: int, book_id: str | ObjectId):
        if isinstance(book_id, str):
            book_id = ObjectId(book_id)

        return self.chapters.find_one({"chapter_no": chapter_no, "book_id": book_id})

    def find_section_by_chapter_id_and_section_no(self, chapter_id: str | ObjectId, section: float):
        if isinstance(chapter_id, str):
            chapter_id = ObjectId(chapter_id)

        return self.sections.find_one({"chapter_id": chapter_id, "section_no": section})

    def find_chapter_by_id(self, id: str | ObjectId):
        if isinstance(id, str):
            id = ObjectId(id)
        return self.chapters.find_one({"_id": id})

    def find_section_by_id(self, id: str | ObjectId):
        if isinstance(id, str):
            id = ObjectId(id)
        return self.sections.find_one({"_id": id})

    def find_all_sections(self) -> list[Section]:
        return [Section(**sec) for sec in self.sections.find()]

    def find_all_sections_v2(self) -> list[dict]:
        return list(self.sections.find())

    def find_all_unevaluated(self) -> list[dict]:
        return list(self.evaluations.find({"evaluated": False}))

    def update_evaluation(self, evaluation: dict):
        evaluation_id = evaluation["_id"]
        evaluation.pop("_id", None)

        self.evaluations.update_one({"_id": ObjectId(evaluation_id)}, {"$set": evaluation}, upsert=True)

    def save_chunk(self, chunk: Chunk):
        chunk_dict = dataclasses.asdict(chunk)
        chunk_dict["_id"] = ObjectId()
        self.chunks.update_one({"_id": chunk_dict["_id"]},
                                 {"$set": chunk_dict},
                                 upsert=True)

    def find_all_evaluations(self):
        return list(self.evaluations.find())
