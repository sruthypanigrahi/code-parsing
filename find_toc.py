from src.extractor import PDFExtractor
from pathlib import Path

try:
    e = PDFExtractor("assets/USB_PD_R3_2 V1.1 2024-10.pdf", Path("outputs"), True, 50)
except (ValueError, PermissionError) as e:
    print(f"Error initializing extractor: {e}")
    exit(1)

try:
    pages = e.extract_content()

    for p in pages:
        if "contents" in p.text.lower() or "table of contents" in p.text.lower():
            print(f"Page {p.page}: TOC found")
            print(p.text[:200])
            break
    else:
        print("No TOC found in first 50 pages")

except FileNotFoundError as e:
    print(f"Error: PDF file not found - {e}")
except Exception as e:
    print(f"Error during extraction: {e}")
