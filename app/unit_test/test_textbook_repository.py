import unittest

from bson import ObjectId

from app.model.book import Book
from app.model.chapter import Chapter
from app.model.section import Section
from app.repository.textbook_repository import TextbookRepository


class TestTextbookRepository(unittest.TestCase):

    def test_textbook_repository(self):
        textbook_repo = TextbookRepository()
        book = self._test_book(textbook_repo)
        self.assertIsNotNone(book)

        chapter = self._test_chapter(textbook_repo, book._id)
        self.assertIsNotNone(chapter)

        sections = self._test_section(textbook_repo, book._id, chapter._id)
        self.assertIsNotNone(sections)

    def _test_book(self, textbook_repo: TextbookRepository) -> Book:
        new_book = Book(title="Book 1",
                        author="Author 1")
        book = textbook_repo.find_book_by_title(new_book.title)

        if book is not None:
            print("Book find by title", book['_id'])
            self.assertIsNotNone(book['_id'])

            book = textbook_repo.find_book_by_id(book['_id'])
            print("Book find by id", book['_id'])

            new_book = Book(**book)

        new_book.author = new_book.author + "+"
        textbook_repo.save_book(new_book)
        return new_book

    def _test_chapter(self, textbook_repo: TextbookRepository, book_id: ObjectId) -> Chapter:
        new_chapter = Chapter(book_id=book_id,
                              chapter_no=1,
                              title="Title 1",
                              summary="Summary 1")

        chapter = textbook_repo.find_chapter_by_chapter_no_and_book_id(new_chapter.chapter_no, book_id)

        if chapter is not None:
            print("Chapter find by chapter number and book id", chapter['_id'])
            self.assertIsNotNone(chapter['_id'])

            new_chapter = Chapter(**chapter)

        new_chapter.summary = new_chapter.summary + "+"
        textbook_repo.save_chapter(new_chapter)
        return new_chapter

    def _test_section(self, textbook_repo: TextbookRepository, book_id: ObjectId, chapter_id: ObjectId) -> list[Section]:
        new_section = Section(book_id=book_id,
                              chapter_id=chapter_id,
                              section_no=1.1,
                              title="Section Title 1",
                              content="Content 1")

        section = textbook_repo.find_section_by_chapter_id_and_section_no(chapter_id, new_section.section_no)

        if section is not None:
            print("Section find by section number and book id", section['_id'])
            self.assertIsNotNone(section['_id'])

            new_section = Section(**section)

        new_section.content = new_section.content + "+"
        sections = [new_section]
        textbook_repo.save_sections(sections)

        return sections




if __name__ == "__main__":
    unittest.main()