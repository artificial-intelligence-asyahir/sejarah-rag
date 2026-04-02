import pymupdf
import pymupdf4llm

def open_document():
    document = pymupdf.open("../../data/sejarah_f1_c1_c2.pdf")
    print(document)
    page_count = document.chapter_page_count(chapter=0)
    print(page_count)



def read_document():
    # document = pymupdf.open("../../data/sejarah_f1_example.pdf")
    # print(document);

    text = pymupdf4llm.to_markdown("../../data/sejarah_f1_example.pdf")
    print(text)


if __name__ == "__main__":
    # read_document()
    open_document()