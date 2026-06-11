from uuid import uuid4

from qdrant_client.http.models import PointStruct
from zenml import log_metadata, step

from app.model.chunk import Chunk
from app.model.embeddings import EmbeddingModel
from app.service.chunking_service import chunk_article


@step
def section_chunking(section: dict) -> Chunk:
    chunks = chunk_article(section['content'], 50, 500)

    payload = dict(book_id=str(section['book_id']),
                   chapter_id=str(section['chapter_id']),
                   section_id=str(section['_id']))

    metadata = {"section_title": section['title'], "section_no": section['section_no'],
                "chunk_count": len(chunks)}
    log_metadata(metadata=metadata)

    return Chunk(contents=chunks, payload=payload)


@step
def section_embedding_step(chunk: Chunk) -> list[PointStruct]:

    # chunks = chunk_article(section['content'], 50, 500)
    #
    # payload = dict(book_id=str(section['book_id']),
    #                chapter_id=str(section['chapter_id']),
    #                section_id=str(section['_id']))

    embeddings = EmbeddingModel().encode(chunk.contents).tolist()

    points = [PointStruct(id=uuid4(), vector=embedding, payload=chunk.payload) for i, embedding in enumerate(embeddings)]

    metadata = {"book_id": chunk.payload['book_id'],
                "chapter_id": chunk.payload['chapter_id'],
                "section_id": chunk.payload['section_id'],
                "vector_count": len(points)}
    log_metadata(metadata=metadata)

    return points

