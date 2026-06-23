import dataclasses

import numpy as np
from ollama import chat
from ollama import ChatResponse
from qdrant_client.http.models import QueryResponse
from sentence_transformers import CrossEncoder

from app.model.citation import Citation
from app.model.embeddings import EmbeddingModel, CrossEncoderModel
from app.repository.textbook_repository import TextbookRepository
from app.repository.vector_repository import VectorRepository

textbook_repo = TextbookRepository()
vector_repo = VectorRepository()

def _retrieve(query: str):
    embeddings = EmbeddingModel().encode(query).tolist()
    search_results: QueryResponse = vector_repo.search_vector(embeddings)

    # reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    # pairs = [[query, point.payload['text']] for point in search_results.points]
    # scores =  reranker.predict(pairs).tolist()
    # points_v2 = [search_results.points[i] for i in np.argsort(scores)[-7:]]

    results = [point.payload['text'] for point in search_results.points]
    references = [_get_citations(point.payload['book_id'], point.payload['chapter_id'], point.payload['section_id']) for point in search_results.points]
    return results, references

def _rag_query(question: str):
    context, references = _retrieve(question)

    prompt = f"""
    [LANGUAGE]
    Response in Bahasa Melayu and plain text. 
    
    [TONE]
    Academic, objective and concise.
    
    Context:
    {chr(10).join(context)}

    Question: {question}

    Answer:"""

    return prompt, context, references

def _get_citations(book_id: str, chapter_id: str, section_id: str):
    book = textbook_repo.find_book_by_id(book_id)
    chapter = textbook_repo.find_chapter_by_id(chapter_id)
    section = textbook_repo.find_section_by_id(section_id)

    citation = Citation(
        book_title=book['title'],
        book_author=book['author'],
        chapter_title=chapter['title'],
        chapter_no=chapter['chapter_no'],
        section_title=section['title'],
        section_no=section['section_no']
    )

    return dataclasses.asdict(citation)

def answer(question: str):
    prompt, context, references = _rag_query(question)
    response: ChatResponse = chat(model="gemma4", messages=[
        {"role": "user",
         "content": prompt}
    ])

    return response.message.content, context, references


