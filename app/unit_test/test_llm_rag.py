import unittest
import pymupdf
import pymupdf4llm

from app.model.embeddings import EmbeddingModel
from app.service.chunking import chunk_article
from app.service.textbook_ingestion_service import TextbookIngestionService


class TestLlmRag(unittest.TestCase):
    def test_llm_rag(self):
        book, chapter, sections = self._textbook_ingestion()

        chunks = []
        for s in sections:
            chunks.extend(chunk_article(s.content, 100, 500))

        model = EmbeddingModel()
        embedding = model.encode(chunks)

        print(embedding.shape)

    def _textbook_ingestion(self):
        document = pymupdf.open("chapters/sejarah_tingkatan_1_bab_1_mengenali_sejarah.pdf")
        content = pymupdf4llm.to_markdown(document)
        metadata = document.metadata

        textbook_ext = TextbookIngestionService(metadata, content)
        book = textbook_ext.get_book()
        self.assertIsNotNone(book)

        chapter = textbook_ext.get_chapter()
        self.assertIsNotNone(chapter)

        sections = textbook_ext.get_sections()
        self.assertIsNotNone(sections)

        return book, chapter, sections


if __name__ == "__main__":
    unittest.main()