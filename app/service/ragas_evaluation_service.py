from openai import AsyncOpenAI
from ragas.embeddings.base import embedding_factory, HuggingfaceEmbeddings, LangchainEmbeddingsWrapper
from ragas.llms import llm_factory
from ragas.metrics.collections import AnswerRelevancy
from ragas.metrics.collections import Faithfulness, ContextPrecision, ContextRecall

from app.service.llm_query_service import answer

client = AsyncOpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

llm = llm_factory("gemma4", provider="openai", client=client)

async def faithfulness_score(answer: dict):
    scorer = Faithfulness(llm=llm)
    result = await scorer.ascore(
        user_input=answer['question'],
        response=answer['response'],
        retrieved_contexts=answer['contexts']
    )
    return result.value

async def context_precision_score(answer: dict):
    scorer = ContextPrecision(llm=llm)
    result = await scorer.ascore(
        user_input=answer['question'],
        reference=answer['ground_truth'],
        retrieved_contexts=answer['contexts']
    )
    return result.value

async def context_recall_score(answer: dict):
    scorer = ContextRecall(llm=llm)
    result = await scorer.ascore(
        user_input=answer['question'],
        retrieved_contexts=answer['contexts'],
        reference = answer['ground_truth']
    )

    return result.value

async def response_relevancy_score(answer: dict):
    embeddings = embedding_factory("huggingface", "sentence-transformers/all-MiniLM-L6-v2")
    scorer = AnswerRelevancy(llm=llm, embeddings=embeddings)
    result = await scorer.ascore(
        user_input=answer['question'],
        response=answer['response']
    )

    return result.value

async def discrete_metric():
    pass


if __name__ == "__main__":
    import asyncio

    sample = {
        "question": "Zaman Prasejarah merupakan zaman sebelum manusia mengetahui dan mengenali tulisan. Zaman ini terbahagi kepada dua, iaitu Zaman Batu dan Zaman Logam, Senaraikan tiga tahap Zaman Batu dan terangkan Zaman Batu Tersebut",
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
    sample["references"] = references

    result_relevancy = asyncio.run(response_relevancy_score(sample))
    print(result_relevancy)
