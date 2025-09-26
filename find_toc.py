from src.pdf_extractor import PDFExtractor
from pathlib import Path
from typing import List

try:
    pdf_path = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
    extractor = PDFExtractor(pdf_path)
except Exception as init_error:
    print(f"Error initializing extractor: {init_error}")
    exit(1)

try:
    pages: List[str] = extractor.extract_pages(max_pages=50)

    for page_num, page_text in enumerate(pages, 1):
        text_lower: str = page_text.lower()
        if "contents" in text_lower or "table of contents" in text_lower:
            print(f"Page {page_num}: TOC found")
            print(page_text[:200])
            break
    else:
        print("No TOC found in first 50 pages")

except FileNotFoundError as file_error:
    print(f"Error: PDF file not found - {file_error}")
except Exception as extraction_error:
    print(f"Error during extraction: {extraction_error}")
