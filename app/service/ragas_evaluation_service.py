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

llm = llm_factory("gemma4", provider="openai", client=client, max_tokens=8192)

def faithfulness_score(answer: dict):
    scorer = Faithfulness(llm=llm)
    result = scorer.score(
        user_input=answer['question'],
        response=answer['response'],
        retrieved_contexts=answer['contexts']
    )
    return result.value

def context_precision_score(answer: dict):
    scorer = ContextPrecision(llm=llm)
    result = scorer.score(
        user_input=answer['question'],
        reference=answer['ground_truth'],
        retrieved_contexts=answer['contexts']
    )
    return result.value

def context_recall_score(answer: dict):
    scorer = ContextRecall(llm=llm)
    result = scorer.score(
        user_input=answer['question'],
        retrieved_contexts=answer['contexts'],
        reference = answer['ground_truth']
    )

    return result.value

def response_relevancy_score(answer: dict):
    embeddings = embedding_factory("huggingface", "sentence-transformers/all-MiniLM-L6-v2")
    scorer = AnswerRelevancy(llm=llm, embeddings=embeddings)
    result = scorer.score(
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
        "ground_truth": """
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

    result_relevancy = response_relevancy_score(sample)
    print(f"Relevancy Score: {result_relevancy}")

    result_recall = context_recall_score(sample)
    print(f"Context Recall Score: {result_recall}")

    result_precision = context_precision_score(sample)
    print(f"Context Precision Score: {result_precision}")

    result_faithfulness = faithfulness_score(sample)
    print(f"Faithfulness Score: {result_faithfulness}")