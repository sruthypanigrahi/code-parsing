#!/usr/bin/env python3
"""Check TOC format in PDF pages."""

from pathlib import Path
from typing import List

from src.pdf_extractor import PDFExtractor


class TOCFormatChecker:
    """Check and display TOC format from PDF pages."""

    def __init__(self, pdf_path: str, start_page: int = 13, end_page: int = 16):
        self.pdf_path = Path(pdf_path)
        self.start_page = start_page
        self.end_page = end_page
        self.extractor = PDFExtractor(self.pdf_path)

    def check_format(self, max_chars: int = 1000) -> None:
        """Check and display TOC format."""
        pages: List[str] = self.extractor.extract_pages(max_pages=20)

        for page_num, page_text in enumerate(pages, 1):
            if self.start_page <= page_num <= self.end_page:
                self._display_page(page_num, page_text, max_chars)

    def _display_page(self, page_num: int, page_text: str, max_chars: int) -> None:
        """Display a single page with formatting."""
        print(f"\n=== PAGE {page_num} ===")
        try:
            text = page_text[:max_chars].encode("ascii", "ignore").decode("ascii")
            print(text)
        except Exception:
            print("[Encoding error]")
        print("=" * 50)


if __name__ == "__main__":
    checker = TOCFormatChecker("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
    checker.check_format()
