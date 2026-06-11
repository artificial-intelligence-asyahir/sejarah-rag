import time

from zenml import pipeline

from steps.section_embedding_step import section_embedding_step, section_chunking
from steps.textbook_repository_step import load_all_sections, save_vector_embedding, save_chunking
from zenml.artifacts.external_artifact import ExternalArtifact


@pipeline(enable_cache=False)
def textbook_embedding_pipeline(section: dict):
    chunk = section_chunking(ExternalArtifact(value=section))
    save_chunking(chunk)

    points = section_embedding_step(chunk)
    save_vector_embedding(points=points)

if __name__ == '__main__':
    sections = load_all_sections()
    for sec in sections:
        textbook_embedding_pipeline(sec)
        time.sleep(5)
