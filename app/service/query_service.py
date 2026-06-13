from ollama import chat
from ollama import ChatResponse
from qdrant_client.http.models import QueryResponse

from app.model.citation import Citation
from app.model.embeddings import EmbeddingModel
from app.repository.textbook_repository import TextbookRepository
from app.repository.vector_repository import VectorRepository

textbook_repo = TextbookRepository()
vector_repo = VectorRepository()

def _retrieve(query: str):
    embeddings = EmbeddingModel().encode(query).tolist()
    search_results: QueryResponse = vector_repo.search_vector(embeddings)
    results = [point.payload['text'] for point in search_results.points]
    sumber = [_get_citations(point.payload['book_id'], point.payload['chapter_id'], point.payload['section_id']) for point in search_results.points]
    return results, sumber

def _rag_query(question: str):
    context, sumber = _retrieve(question)

    citation = "\n".join(
        f"""Book Title: {c.book_title}
    Author: {c.book_author}
    Chapter: {c.chapter_no} - {c.chapter_title}
    Section: {c.section_no} - {c.section_title}
    """
        for c in sumber
    )

    prompt = f"""
    [LANGUAGE CONSTRAINT]
    All responses should be in Bahasa Melayu.
    
    [ROLE]
    Anda merupakan skema jawapan bagi matapelajaran Sejarah di Sekolah Menengah Kebangsaan Malaysia.
    Sila berikan jawapan yang mudah dibaca dan mudah dipahami.
    
    [SOURCE] 
    Include the source of the information you use in your response.
    {citation}

    Context:
    {chr(10).join(context)}

    Question: {question}

    Answer:"""

    return prompt

def answer(question: str):
    prompt = _rag_query(question)
    response: ChatResponse = chat(model="gemma4", messages=[
        {"role": "user",
         "content": prompt}
    ])

    return response.message.content

def _get_citations(book_id: str, chapter_id: str, section_id: str):
    book = textbook_repo.find_book_by_id(book_id)
    chapter = textbook_repo.find_chapter_by_id(chapter_id)
    section = textbook_repo.find_section_by_id(section_id)

    return Citation(
        book_title=book['title'],
        book_author=book['author'],
        chapter_title=chapter['title'],
        chapter_no=chapter['chapter_no'],
        section_title=section['title'],
        section_no=section['section_no']
    )

if __name__ == "__main__":
    jawapan = answer("Apa itu sejarah?")
    print(jawapan)

