#!/usr/bin/env python3
"""Test the search functionality."""

from src.extractor import PDFExtractor
from src.search import TOCSearcher
from pathlib import Path

# Extract first 20 pages
extractor = PDFExtractor('assets/USB_PD_R3_2 V1.1 2024-10.pdf', Path('outputs'), True, 20)
pages = extractor.extract_content()

# Search for TOC
searcher = TOCSearcher()
entries = searcher.search_toc(pages)

print(f"Found {len(entries)} TOC entries:")
for entry in entries[:10]:
    print(f"  {entry.section_id}: {entry.title} (page {entry.page})")