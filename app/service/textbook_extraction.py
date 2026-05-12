import logging
import uuid
import pymupdf
import pymupdf4llm
import re
from app.model.book import Book
from app.model.chapter import Chapter
from app.model.section import Section

logging.basicConfig(level=logging.INFO)

def get_book_metadata(metadata: dict) -> Book:
    logging.info("Start getting book metadata: %s", document)

    book = Book(id=uuid.uuid4(),
                title=metadata["title"],
                author=metadata["author"])

    logging.info("Complete getting book metadata: %s", book)
    return book

def get_chapter_metadata(metadata: dict, book_id: str, summary: str) -> Chapter:

    subject = metadata["subject"]

    # \d: digit
    # \s: spaces
    # +: one or more occurrence
    # (): capture and group
    # .: any character
    # *: zero or more occurrence
    match = re.search(r'(\d+)\s+(.*)', subject)
    if match:
        chapter_number = int(match.group(1))
        chapter_title = str(match.group(2)).strip()

    chapter = Chapter(id=uuid.uuid4(),
                      book_id= book_id,
                      chapter = chapter_number,
                      title = chapter_title,
                      summary = summary)

    print(chapter)
    return chapter

def get_kesimpulan(content: str) -> str:
    kesimpulan = None

    # .: any character - usually not included new line
    # *: zero or more occurrences
    # ?: zero or one occurrences
    # +: one or more occurrences
    # re.DOTALL: makes the 'dot' matches new line
    match = re.search(r'(Kesimpulan.*?)(\*\*\d+\*\*)', content, re.DOTALL)
    if match:
        kesimpulan = match.group(1).strip()

    if kesimpulan:
        kesimpulan = __clean_text(kesimpulan)

    return kesimpulan


def get_section(text: str, book_id: str, chapter_id: str):
    # Pattern to match section headers like 1.1, 1.2, 1.3
    # section_pattern = re.compile(r'(##\s*\*\*(\d+\.\d+)\s+(.*?)\*\*)', re.MULTILINE)
    section_pattern = re.compile(r'\*\*(\d+\.\d+)\**\s*\n?\s*(?:#{1,6}\s*)?\**\s*([^\*\n]+)\**', re.DOTALL)

    sections = []
    matches = list(section_pattern.finditer(text))

    for i, match in enumerate(matches):
        section_num = match.group(1)
        section_title = match.group(2).strip()

        # Content starts after the header
        content_start = match.end()

        # Content ends at the start of the next section (or end of text)
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        content = text[content_start:content_end].strip()

        # Clean up excessive whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)

        section = Section(id=uuid.uuid4(),
                          book_id=book_id,
                          chapter_id=chapter_id,
                          section=section_num,
                          title=section_title,
                          content=__clean_text(content))

        sections.append(section)

    return sections


def __clean_text(text):
    # Remove image artifact markers
    text = re.sub(r'\*\*----- Start of picture text -----\*\*', '', text)
    text = re.sub(r'\*\*----- End of picture text -----\*\*', '', text)
    text = re.sub(r'\*\*==>.*?<==\*\*', '', text)

    # Remove standalone single characters on their own
    # text = re.sub(r'(?<!\w)\b[a-zA-Z]\b(?!\w)', '', text)

    # Remove HTML line breaks
    text = re.sub(r'<br>', ' ', text)

    # Remove excessive blank lines (keep max 1)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Collapse multiple spaces into one
    text = re.sub(r' {2,}', ' ', text)

    # Remove coordinate-like OCR artifacts e.g. "0M10M  100M  1000M"
    text = re.sub(r'(\d+M\s*)+', '', text)

    # Remove garbled OCR lines (lines with mostly symbols/short noise)
    text = re.sub(r'——+\w*', '', text)  # e.g. ——————EEe
    text = re.sub(r'\b(eb|Te d|=\|)\b', '', text)  # stray fragments

    # Strip leading/trailing whitespace
    text = text.strip()

    return text

if __name__ == "__main__":
    # document and content
    document = pymupdf.open("../../chapters/sejarah_tingkatan_1_bab_1_mengenali_sejarah.pdf")
    content = pymupdf4llm.to_markdown(document)
    metadata = document.metadata

    # book
    book = get_book_metadata(metadata)
    chapter = get_chapter_metadata(metadata, book.id, get_kesimpulan(content))
    sections = get_section(content, book.id, chapter.id)
    print("completed")

