from zenml import step, log_metadata
import pymupdf
import pymupdf4llm

from app.service.textbook_ingestion_service import TextbookIngestionService

from app.model.book import Book
from app.model.chapter import Chapter

@step
def step_1_open_document(filepath: str) -> TextbookIngestionService:
    document = pymupdf.open(filepath)
    content = pymupdf4llm.to_markdown(document)
    metadata = document.metadata
    textbook_ingestion_svc = TextbookIngestionService(metadata, content)
    log_metadata(metadata={"filename": filepath})
    return textbook_ingestion_svc


@step
def step_2_get_book(textbook_ingestion_svc: TextbookIngestionService):
    book = textbook_ingestion_svc.get_book()
    log_metadata(metadata={"title": book.title, "author": book.author})
    return book


@step
def step_3_get_chapter(textbook_ingestion_svc: TextbookIngestionService, book: Book):
    chapter = textbook_ingestion_svc.get_chapter(book=book)
    log_metadata(metadata={"chapter_no": chapter.chapter_no, "title": chapter.title})
    return chapter

@step
def step_4_get_sections(textbook_ingestion_svc: TextbookIngestionService, book: Book, chapter: Chapter):
    sections = textbook_ingestion_svc.get_sections(book=book, chapter=chapter)
    metadata = {
        "section_count": str(len(sections))
    }

    for i, sect in enumerate(sections):
        metadata[f"section_{i}_no"] = str(sect.section_no)
        metadata[f"section_{i}_title"] = sect.title

    log_metadata(metadata=metadata)
    return sections