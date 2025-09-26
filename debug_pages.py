#!/usr/bin/env python3
"""Debug script to check page content."""

from src.pdf_extractor import PDFExtractor
from pathlib import Path
from typing import List


def debug_pages() -> None:
    pdf_path = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
    extractor = PDFExtractor(pdf_path)

    pages: List[str] = extractor.extract_pages(max_pages=30)

    for i, page_text in enumerate(pages[:15]):
        page_num = i + 1
        print(f"\n=== PAGE {page_num} ===")
        try:
            text: str = page_text[:500].encode("ascii", "ignore").decode("ascii")
            print(text)
            print("...")
            if "contents" in page_text.lower() or "table" in page_text.lower():
                print("*** FOUND TOC KEYWORDS ***")
        except Exception:
            print("[Encoding error - skipping page]")


if __name__ == "__main__":
    debug_pages()
