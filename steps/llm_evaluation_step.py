from zenml import step, log_metadata

from app.service.llm_query_service import answer
from app.service.ragas_evaluation_service import faithfulness_score, context_precision_score, context_recall_score, \
    answer_relevancy_score


@step
def llm_answering_step(question: str):
    response, context, references = answer(question)
    return {"response": response, "contexts": context, "references": references}

@step
def evaluate_faithfulness_score(answer: dict, eval: dict):
    try:
        result = faithfulness_score(eval['question'], answer['response'], answer['contexts'])
        log_metadata(metadata={"faithfulness_score": result})
        return result
    except Exception as e:
        log_metadata(metadata={"faithfulness_score": "Error"})
        return -1


@step
def evaluate_context_precision_score(answer: dict, eval: dict):

    try:
        result = context_precision_score(eval['question'], eval['ground_truth'], answer['contexts'])
        log_metadata(metadata={"context_precision_score": result})
        return result
    except Exception as e:
        log_metadata(metadata={"context_precision_score": "Error"})
        return -1


@step
def evaluate_context_recall_score(answer: dict, eval: dict):
    try:
        result = context_recall_score(eval['question'], eval['ground_truth'], answer['contexts'])
        log_metadata(metadata={"context_recall_score": result})
        return result
    except Exception as e:
        log_metadata(metadata={"context_recall_score": "Error"})
        return -1


@step
def evaluate_answer_relevancy_score(answer: dict, eval: dict):
    try:
        result = answer_relevancy_score(eval['question'], answer['response'])
        log_metadata(metadata={"answer_relevancy_score": result})
        return result
    except Exception as e:
        log_metadata(metadata={"answer_relevancy_score": "Error"})
        return -1


