from uuid import uuid4

from qdrant_client.http.models import PointStruct, Payload
import unittest

from app.model.embeddings import EmbeddingModel
from app.model.section import Section
from app.repository.textbook_repository import TextbookRepository
from app.repository.vector_repository import VectorRepository
from app.service.chunking import chunk_article, chunk_text


class TestTextChunkEmbed(unittest.TestCase):
    def test_text_embedding(self):

        section = self._find_section_from_unittest()
        section = Section(**section)

        chunks1 = chunk_article(section.content, 1, 200)
        print(chunks1)

        model = EmbeddingModel()
        embedding = model.encode(chunks1)
        embedding = embedding.tolist()
        print(embedding[0])


        payload = dict(book_id=str(section.book_id),
                       chapter_id=str(section.chapter_id),
                       section_id=str(section._id))

        point = PointStruct(id=uuid4(), vector=embedding[0], payload=payload)
        vector_repo = VectorRepository()
        vector_repo.save_vector([point])
        print("Completed")


    def _find_section_from_unittest(self) -> Section:
        textbook_repo = TextbookRepository()
        section = textbook_repo.find_section_by_id('6a0dd06bc923557f95b2a76f')
        print(section)
        return section

if __name__ == "__main__":
    unittest.main()