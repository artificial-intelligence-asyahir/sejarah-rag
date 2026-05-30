from uuid import uuid4

from sentence_transformers import SentenceTransformer
import unittest

from app.model.chunk import Chunk
from app.model.embeddings import EmbeddingModel
from app.model.metadata import Metadata
from app.model.section import Section
from app.repository.textbook_repository import TextbookRepository
from app.service.chunking import chunk_article, chunk_text


class TestTextChunkEmbed(unittest.TestCase):
    def test_text_embedding(self):

        section = self._find_section_from_unittest()
        section = Section(**section)

        chunks1 = chunk_article(section.content, 1, 200)
        print(chunks1)

        chunks2 = chunk_text(section.content)
        print(chunks2)

        model = EmbeddingModel()
        embedding = model.encode(chunks1)
        print('Embedding: ', embedding.shape)

        metadata = Metadata(book_id=section.book_id, chapter_id=section.chapter_id, section_id=section._id)
        chunk = Chunk(metadata=metadata, id=uuid4(), vector=embedding)
        print(chunk)


    def _find_section_from_unittest(self) -> Section:
        textbook_repo = TextbookRepository()
        section = textbook_repo.find_section_by_id('6a0dd06bc923557f95b2a76f')
        print(section)
        return section

if __name__ == "__main__":
    unittest.main()