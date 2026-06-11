from qdrant_client.http.models import PointStruct
from zenml import step, log_metadata

from app.model.book import Book
from app.model.chapter import Chapter
from app.model.section import Section
from app.repository.textbook_repository import TextbookRepository
from app.repository.vector_repository import VectorRepository

textbook_repo = TextbookRepository()


@step
def save_book(book: Book):
    existing_book = textbook_repo.find_book_by_title(book.title)

    if existing_book:
        book._id = existing_book["_id"]

    textbook_repo.save_book(book)
    log_metadata(metadata={"book_id": str(book._id)})

    return book

@step
def save_chapter(chapter: Chapter):
    existing_chapter = textbook_repo.find_chapter_by_chapter_no_and_book_id(chapter.chapter_no, chapter.book_id)

    if existing_chapter:
        chapter._id = existing_chapter["_id"]

    textbook_repo.save_chapter(chapter)
    log_metadata(metadata={"chapter_id": str(chapter._id)})

    return chapter

@step
def save_sections(sections: list[Section]):

    for section in sections:
        existing_section = textbook_repo.find_section_by_chapter_id_and_section_no(section.chapter_id, section.section_no)

        if existing_section:
            section._id = existing_section["_id"]

    textbook_repo.save_sections(sections)
    metadata = {
        "section_count": str(len(sections))
    }

    for i, sect in enumerate(sections):
        metadata[f"section_{i}_id"] = str(sect._id)

    log_metadata(metadata=metadata)


def load_all_sections() -> list[dict]:
    sections = textbook_repo.find_all_sections_v2()
    for section in sections:
        section['_id'] = str(section['_id'])
        section['book_id'] = str(section['book_id'])
        section['chapter_id'] = str(section['chapter_id'])

    # metadata = {}
    # for i, sect in enumerate(sections):
    #     metadata[f"section_{i}_title"] = str(sect.title)

    return sections

@step
def save_vector_embedding(points: list[PointStruct]):
    vector_repo = VectorRepository()
    vector_repo.save_vector(points)
    metadata = {"vector_count": str(len(points))}
    log_metadata(metadata=metadata)

