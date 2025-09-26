from src.parsing_strategies import RegexTOCParser
from src.extractor import PDFExtractor
from pathlib import Path

try:
    # Extract pages 13-16 where TOC is located
    extractor = PDFExtractor(
        "assets/USB_PD_R3_2 V1.1 2024-10.pdf", Path("outputs"), True, 20
    )
    pages = extractor.extract_content()

    # Get TOC pages
    toc_pages = [(p.page, p.text) for p in pages if p.page >= 13 and p.page <= 16]

    # Test parser
    parser = RegexTOCParser()
    entries = parser.parse(toc_pages)

    print(f"Found {len(entries)} TOC entries:")
    for entry in entries[:10]:
        print(f"  {entry.section_id}: {entry.title} (page {entry.page})")

except FileNotFoundError as e:
    print(f"Error: PDF file not found - {e}")
except Exception as e:
    print(f"Error during parsing: {e}")
