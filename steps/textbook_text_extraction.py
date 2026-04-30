from zenml import step, pipeline
import pymupdf4llm

@step
def read_text() -> str:
    return "syahir test"

@step
def read_document():
    text = pymupdf4llm.to_markdown("../data/sejarah_f1_example.pdf")
    print(text)

@pipeline
def simple_pipeline() -> str:
    read_document()
    return read_text()


@step
def read_title():
    return "syahir test";

@step
def read_text_from_file():
    return "syahir test";



if __name__ == "__main__":
    simple_pipeline()
