from uuid import uuid4

from qdrant_client.http.models import PointStruct
from zenml import log_metadata, step

from app.model.embeddings import EmbeddingModel
from app.model.section import Section
from app.service.chunking_service import chunk_article

# @step
# def section_embedding_step(sections: list[Section]) -> list[PointStruct]:
#     all_points = []
#     model = EmbeddingModel()
#
#     for section in sections:
#         chunks = chunk_article(section.content, 50, 500)
#
#         payload = dict(book_id=str(section.book_id),
#                        chapter_id=str(section.chapter_id),
#                        section_id=str(section._id))
#
#         embeddings = model.encode(chunks).tolist()
#
#         points = [PointStruct(id=uuid4(), vector=embedding, payload=payload) for i, embedding in enumerate(embeddings)]
#         all_points.extend(points)
#
#         metadata={"section_title": section.title, "section_no": section.section_no, "vector_count": len(points)}
#         log_metadata(metadata=metadata)
#
#     return all_points

# @step
# def section_embedding_step(section: Section) -> list[PointStruct]:
#
#     chunks = chunk_article(section.content, 50, 500)
#
#     payload = dict(book_id=str(section.book_id),
#                    chapter_id=str(section.chapter_id),
#                    section_id=str(section._id))
#
#     embeddings = EmbeddingModel().encode(chunks).tolist()
#
#     points = [PointStruct(id=uuid4(), vector=embedding, payload=payload) for i, embedding in enumerate(embeddings)]
#
#     metadata = {"section_title": section.title, "section_no": section.section_no, "vector_count": len(points)}
#     log_metadata(metadata=metadata)
#
#     return points

@step
def section_embedding_step(section: dict) -> list[PointStruct]:

    chunks = chunk_article(section['content'], 50, 500)

    payload = dict(book_id=str(section['book_id']),
                   chapter_id=str(section['chapter_id']),
                   section_id=str(section['_id']))

    embeddings = EmbeddingModel().encode(chunks).tolist()

    points = [PointStruct(id=uuid4(), vector=embedding, payload=payload) for i, embedding in enumerate(embeddings)]

    metadata = {"section_title": section['title'], "section_no": section['section_no'], "vector_count": len(points)}
    log_metadata(metadata=metadata)

    return points

