from zenml import step, pipeline
import pymupdf4llm

@step
def read_text() -> str:
    return "syahir test"

@step
def read_document():
    text = pymupdf4llm.to_markdown("../textbook/SEJARAH_F2_copy.pdf")
    print(text)

@pipeline
def simple_pipeline() -> str:
    read_document()
    return read_text()

if __name__ == "__main__":
    simple_pipeline()
