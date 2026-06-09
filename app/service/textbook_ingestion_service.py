import logging
import re
from app.model.book import Book
from app.model.chapter import Chapter
from app.model.section import Section

class TextbookIngestionService:
    def __init__(self, metadata: dict, content: str):
        self.metadata = metadata
        self.content = content

        self._book = None
        self._chapter = None
        self._sections = []

    def get_book(self) -> Book:
        logging.info("Start getting book metadata")
        self._book = Book(
            title=self.metadata.get("title", ""),
            author=self.metadata.get("author", "")
        )
        logging.info("Complete getting book metadata: %s", self._book)
        return self._book

    def get_chapter(self, book: Book = None) -> Chapter:
        if book:
            self._book = book

        subject = self.metadata.get("subject", "")
        chapter_number, chapter_title = self._parse_subject(subject)

        if not self._book:
            raise ValueError("Book must be set before creating a chapter")

        self._chapter = Chapter(
            book_id=self._book._id,
            chapter_no=chapter_number,
            title=chapter_title,
            summary=self._get_kesimpulan()
        )

        return self._chapter

    def get_sections(self, book: Book = None, chapter: Chapter = None) -> list[Section]:
        if book:
            self._book = book
        if chapter:
            self._chapter = chapter

        # section_pattern = re.compile(
        #     r'\*\*(\d+\.\d+)\**\s*\n?\s*(?:#{1,6}\s*)?\**\s*([^\*\n]+)\**',
        #     re.DOTALL
        # )

        # section_pattern = re.compile(
        #     r'(?:\*\*|#{1,6}\s*|>\s*)(\d+\.\d+)\**\s*\**\s*([^\*\n]+)',
        #     re.DOTALL
        # )

        # section_pattern = re.compile(
        #     r'(?:#{1,6}\s*|\*\*|>\s*)(?:[»\d\s]*)(\d+\.\d+)\s*([^\*\n]+)',
        #     re.DOTALL
        # )

        section_pattern = re.compile(
            r'\*\*(\d+\.\d+)\*\*\s*\n+\s*(?:#{1,6}\s*)?\*?\*?\s*([^\*\n]+)'
            r'|(?:#{1,6}\s*|\*\*|>\s*)(?:[»\d\s]*)(\d+\.\d+)\s*([^\*\n]+)',
            re.DOTALL
        )

        self._sections = []
        matches = list(section_pattern.finditer(self.content))

        for i, match in enumerate(matches):
            section_num = match.group(1) or match.group(3)
            section_title = (match.group(2) or match.group(4) or '').strip()

            content_start = match.end()
            content_end = matches[i + 1].start() if i + 1 < len(matches) else len(self.content)

            raw_content = self.content[content_start:content_end].strip()

            if not self._book:
                raise ValueError("Book must be set before creating a section")
            elif not self._chapter:
                raise ValueError("Chapter must be set before creating a section")

            section = Section(
                book_id=self._book._id,
                chapter_id=self._chapter._id,
                section_no=float(section_num),
                title=section_title,
                content=self._clean_text(raw_content)
            )
            self._sections.append(section)
        return self._sections

    def _parse_subject(self, subject: str):
        match = re.search(r'(\d+)\s+(.*)', subject)
        if match:
            return int(match.group(1)), match.group(2).strip()
        return None, None

    def _get_kesimpulan(self) -> str:
        match = re.search(r'((?:Kesimpulan|Sinopsis).*?)(\*\*\d+\*\*)', self.content, re.DOTALL)
        if match:
            return self._clean_text(match.group(1).strip())
        return None

    def _clean_text(self, text: str) -> str:
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