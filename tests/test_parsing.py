from pathlib import Path

from src.models import TOCEntry
from src.pdf_extractor import PDFExtractor
from src.toc_extractor import TOCExtractor

try:
    # Extract pages 13-16 where TOC is located
    pdf_path = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
    extractor = PDFExtractor(pdf_path)

    # Extract pages as text
    pages: list[str] = extractor.extract_pages(max_pages=20)

    # Get TOC pages content (pages 13-16, but using 0-based indexing)
    toc_content = ""
    for i, page_text in enumerate(pages):
        if 12 <= i <= 15:  # Pages 13-16 in 0-based indexing
            toc_content += page_text + "\n"

    # Test TOC extractor
    toc_extractor = TOCExtractor(extractor.get_doc_title())
    entries: list[TOCEntry] = toc_extractor.extract_from_content(toc_content)

    print(f"Found {len(entries)} TOC entries:")
    for entry in entries[:10]:
        print(f"  {entry.section_id}: {entry.title} (page {entry.page})")

except FileNotFoundError as e:
    print(f"Error: PDF file not found - {e}")
except Exception as e:
    print(f"Error during parsing: {e}")
