import os

from openai import AsyncOpenAI
from ragas.embeddings.base import embedding_factory, HuggingfaceEmbeddings, LangchainEmbeddingsWrapper
from ragas.llms import llm_factory
from ragas.metrics.collections import AnswerRelevancy
from ragas.metrics.collections import Faithfulness, ContextPrecision, ContextRecall

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
SENTENCE_TRANSFORMERS_MODEL = "sentence-transformers/" + os.getenv("SENTENCE_TRANSFORMERS_MODEL")

client = AsyncOpenAI(
    api_key="ollama",
    base_url=OLLAMA_URL
)

llm = llm_factory(OLLAMA_MODEL, provider="openai", client=client, max_tokens=8192, )

def faithfulness_score(question: str, response: str, contexts: list[str]):
    scorer = Faithfulness(llm=llm)
    result = scorer.score(
        user_input=question,
        response=response,
        retrieved_contexts=contexts
    )
    return result.value

def context_precision_score(question: str, ground_truth: str, contexts: list[str]):
    scorer = ContextPrecision(llm=llm)
    result = scorer.score(
        user_input=question,
        reference=ground_truth,
        retrieved_contexts=contexts
    )
    return result.value

def context_recall_score(question: str, ground_truth: str, contexts: list[str]):
    scorer = ContextRecall(llm=llm)
    result = scorer.score(
        user_input=question,
        retrieved_contexts=contexts,
        reference = ground_truth
    )

    return result.value

def answer_relevancy_score(question: str, response: str):
    embeddings = embedding_factory("huggingface", SENTENCE_TRANSFORMERS_MODEL)
    scorer = AnswerRelevancy(llm=llm, embeddings=embeddings)
    result = scorer.score(
        user_input=question,
        response=response,
    )

    return result.value

async def discrete_metric():
    pass
