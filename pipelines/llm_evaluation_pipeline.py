from zenml import pipeline, ExternalArtifact

from steps.llm_evaluation_step import llm_answering_step, evaluate_faithfulness_score, evaluate_context_precision_score, \
    evaluate_context_recall_score, evaluate_answer_relevancy_score
from steps.textbook_repository_step import load_all_evalutions, update_evaluation


@pipeline(enable_cache=False)
def llm_evaluation_pipeline(eval: dict):
    res = llm_answering_step(eval['question'])

    ex_eval = ExternalArtifact(value=eval)

    faithfulness = evaluate_faithfulness_score(res, ex_eval)

    context_precision = evaluate_context_precision_score(res, ex_eval)

    context_recall = evaluate_context_recall_score(res, ex_eval)

    answer_relevancy = evaluate_answer_relevancy_score(res, ex_eval)

    update_evaluation(ex_eval,
                      res,
                      faithfulness,
                      context_precision,
                      context_recall,
                      answer_relevancy)


if __name__ == '__main__':
    evaluations = load_all_evalutions()
    for eval in evaluations:
        llm_evaluation_pipeline(eval)