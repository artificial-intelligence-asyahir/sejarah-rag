from langchain_ollama import ChatOllama, OllamaEmbeddings
from openai import AsyncOpenAI, OpenAI
from ragas import Dataset, experiment
from ragas.metrics import DiscreteMetric
from ragas.llms import llm_factory
import dataclasses
from ollama import chat
from ollama import ChatResponse
from qdrant_client.http.models import QueryResponse
from ragas.metrics.collections import Faithfulness

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
    references = [_get_citations(point.payload['book_id'], point.payload['chapter_id'], point.payload['section_id']) for point in search_results.points]
    return results, references

def _rag_query(question: str):
    context, references = _retrieve(question)

    prompt = f"""
    [LANGUAGE CONSTRAINT]
    All responses should be in Bahasa Melayu.
    
    [ROLE]
    Anda merupakan skema jawapan bagi matapelajaran Sejarah di Sekolah Menengah Kebangsaan Malaysia.
    Sila berikan jawapan yang mudah dibaca dan mudah dipahami.
    
    Context:
    {chr(10).join(context)}

    Question: {question}

    Answer:"""

    return prompt, context, references

def answer(question: str):
    prompt, context, references = _rag_query(question)
    response: ChatResponse = chat(model="gemma4", messages=[
        {"role": "user",
         "content": prompt}
    ])

    return response.message.content, context, references

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

# def ragas_evaluation():
#     eval_llm = ChatOllama(model="gemma4")
#     eval_embedding = OllamaEmbeddings(model="all-MiniLM-L6-v2")
#
#
#     pass

@experiment()
async def run_experiment(row):

    my_metric = DiscreteMetric(
        name="correctness",
        prompt="Check if the response contains points mentioned from the grading notes and return 'pass' or 'fail'.\nResponse: {response} Grading Notes: {grading_notes}",
        allowed_values=["pass", "fail"],
    )

    client = OpenAI(
        api_key="ollama",  # Ollama doesn't require a real key
        base_url="http://localhost:11434/v1"
    )
    llm = llm_factory("gemma4", provider="openai", client=client)

    score = my_metric.score(
        llm=llm,
        response=row['response'],
        grading_notes=row["grading_notes"]
    )

    experiment_view = {
        **row,
        "response": sample['response'],
        "score": score.value
    }
    print(experiment_view)
    return experiment_view

async def test_faithfulness(sample):
    client = AsyncOpenAI(
        api_key="ollama",  # Ollama doesn't require a real key
        base_url="http://localhost:11434/v1"
    )
    llm = llm_factory("gemma4", provider="openai", client=client, max_tokens=8192)

    scorer = Faithfulness(llm=llm)

    result = await scorer.ascore(
        user_input=sample['question'],
        response=sample['response'],
        retrieved_contexts=sample['contexts']
    )

    print(f"Faithfulness Score: {result.value}")


if __name__ == "__main__":
    import asyncio



    sample = {
        "question" : "Zaman Prasejarah merupakan zaman sebelum manusia mengetahui dan mengenali tulisan. Zaman ini terbahagi kepada dua, iaitu Zaman Batu dan Zaman Logam, Senaraikan tiga tahap Zaman Batu dan terangkan Zaman Batu Tersebut",
        "grading_notes": """
        1.Zaman Paleolitik, 2.Zaman Mesolitik, 3.Zaman Neolitik. 
        ## Zaman Paleolitk 
        - Manusia perlu meneruskan kelangsungan hidup dengan menggunakan teknologi batu yang serba ringkas
        - Menggunakan peralatan daripada tulang binatang dalam aktiviti harian
        
        ## Zaman Mesolitik 
        - Memburu binatang dan menangkap ikan sebagai sumber makanan 
        
        ## Zaman Neolitik 
        - Perkembangan teknologi dan corak kehidupan lebih baik 
        - Wujud kawasan petempatan yang mengamalkan aktiviti bercucuk tanam, membuat tembikar dan menternak binatang
        """
    }

    response, context, references = answer(sample['question'])
    sample["contexts"] = context
    sample["response"] = response
    sample["references"] =  references

    # evaluation_dataset = EvaluationDataset(list(sample))
    #
    # result = evaluate(dataset=evaluation_dataset, metrics=[LLMContextRecall(), Faithfulness(), FactualCorrectness()],
    #                   llm=evaluator_llm)
    # result

    dataset = Dataset(name="test_dataset", backend="local/csv", root_dir=".")
    dataset.append(sample)
    dataset.save()

    _ = asyncio.run(run_experiment.arun(dataset, name="ragas_evaluation"))
    _2 = asyncio.run(test_faithfulness(sample))


    print (sample)

