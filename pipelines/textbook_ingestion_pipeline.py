from pathlib import Path

from zenml import pipeline

from steps.textbook_ingestion_step import step_1_open_document, step_2_get_book, step_3_get_chapter, step_4_get_sections
from steps.textbook_repository_step import save_book, save_chapter, save_sections
import shutil
import time

path = Path("/Users/syahirghariff/Developer/2026/sejarah-rag/chapters")
processed_path = Path("/Users/syahirghariff/Developer/2026/sejarah-rag/processed")


@pipeline(enable_cache=False)
def textbook_ingestion_pipeline(filepath: str):
    txtbook_ingest_svc = step_1_open_document(filepath)
    book = step_2_get_book(txtbook_ingest_svc)
    book = save_book(book)

    chapter = step_3_get_chapter(txtbook_ingest_svc, book)
    chapter = save_chapter(chapter)

    sections = step_4_get_sections(txtbook_ingest_svc, book, chapter)
    save_sections(sections)

if __name__ == "__main__":
    for doc_path in path.glob("*.pdf"):
        print(f"Processing {doc_path.name}")
        textbook_ingestion_pipeline(filepath=str(doc_path))
        
        # Move file to processed directory
        dest_path = processed_path / doc_path.name
        shutil.move(str(doc_path), str(dest_path))
        print(f"Moved {doc_path.name} to {processed_path}")
        
        time.sleep(5)
