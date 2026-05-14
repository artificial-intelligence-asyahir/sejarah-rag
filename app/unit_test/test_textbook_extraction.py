import pymupdf
import pymupdf4llm
from app.service.textbook_extractor import TextbookExtractor
import unittest

class TestTextbookExtraction(unittest.TestCase):
    def test_textbook_extraction(self):
        document = pymupdf.open("../../chapters/sejarah_tingkatan_1_bab_1_mengenali_sejarah.pdf")
        content = pymupdf4llm.to_markdown(document)
        metadata = document.metadata

        textbook_ext = TextbookExtractor(metadata, content);
        book = textbook_ext.get_book()
        self.assertIsNotNone(book)

        chapter = textbook_ext.get_chapter()
        self.assertIsNotNone(chapter)

        sections = textbook_ext.get_sections()
        self.assertIsNotNone(sections)

if __name__ == "__main__":
    unittest.main()



