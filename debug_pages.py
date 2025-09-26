#!/usr/bin/env python3
"""Debug script to check page content."""

from src.extractor import PDFExtractor
from pathlib import Path


def debug_pages():
    extractor = PDFExtractor(
        "assets/USB_PD_R3_2 V1.1 2024-10.pdf",
        Path("outputs"),
        ocr_fallback=True,
        max_pages=30,
    )

    pages = extractor.extract_content()

    for i, page in enumerate(pages[:15]):
        print(f"\n=== PAGE {page.page} ===")
        try:
            text = page.text[:500].encode("ascii", "ignore").decode("ascii")
            print(text)
            print("...")
            if "contents" in page.text.lower() or "table" in page.text.lower():
                print("*** FOUND TOC KEYWORDS ***")
        except:
            print("[Encoding error - skipping page]")


if __name__ == "__main__":
    debug_pages()
