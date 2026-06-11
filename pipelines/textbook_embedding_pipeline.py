import time

from zenml import pipeline

from steps.section_embedding_step import section_embedding_step
from steps.textbook_repository_step import load_all_sections, save_vector_embedding
from zenml.artifacts.external_artifact import ExternalArtifact


@pipeline(enable_cache=False)
def textbook_embedding_pipeline(section: dict):
    points = section_embedding_step(ExternalArtifact(value=section))
    save_vector_embedding(points=points)

if __name__ == '__main__':
    sections = load_all_sections()
    for sec in sections:
        textbook_embedding_pipeline(sec)
        time.sleep(5)
