import unittest
from unittest.mock import MagicMock, patch
from app.service.textbook_service import TextbookService
from app.model.book import Book
from app.model.chapter import Chapter
from app.model.section import Section
import uuid

class TestTextbookService(unittest.TestCase):
    @patch('app.service.textbook_service.TextbookRepository')
    @patch('app.service.textbook_service.TextbookExtractor')
    def test_process_and_save_pdf(self, MockExtractor, MockRepository):
        # Setup mocks
        mock_repo = MockRepository.return_value
        mock_ext = MockExtractor.return_value
        
        book_id = uuid.uuid4()
        chapter_id = uuid.uuid4()
        
        mock_ext.get_book.return_value = Book(id=book_id, title="Test Book", author="Author")
        mock_ext.get_chapter.return_value = Chapter(id=chapter_id, book_id=book_id, chapter=1, title="Chapter 1", summary="Summary")
        mock_ext.get_sections.return_value = [Section(id=uuid.uuid4(), book_id=book_id, chapter_id=chapter_id, section="1.1", title="S1", content="C1")]
        
        service = TextbookService()
        result = service.process_and_save_pdf({"title": "Test"}, "Content")
        
        # Verify repository calls
        self.assertTrue(mock_repo.save_book.called)
        self.assertTrue(mock_repo.save_chapter.called)
        self.assertTrue(mock_repo.save_sections.called)
        self.assertEqual(result["sections_count"], 1)
        self.assertEqual(result["book_id"], str(book_id))

    @patch('app.service.textbook_service.TextbookRepository')
    def test_get_full_chapter_data(self, MockRepository):
        mock_repo = MockRepository.return_value
        chapter_id = "test-id"
        mock_repo.get_chapter.return_value = {"id": chapter_id, "title": "Test Chapter"}
        mock_repo.get_sections_by_chapter.return_value = [{"id": "s1", "title": "Section 1"}]
        
        service = TextbookService()
        result = service.get_full_chapter_data(chapter_id)
        
        self.assertEqual(result["chapter"]["id"], chapter_id)
        self.assertEqual(len(result["sections"]), 1)

if __name__ == "__main__":
    unittest.main()
