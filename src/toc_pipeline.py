"""TOC extraction pipeline."""

from pathlib import Path
from typing import List

from .models import TOCEntry
from .pdf_extractor import PDFExtractor
from .toc_extractor import TOCExtractor
from .writer import write_jsonl


class TOCPipeline:
    """Handles TOC extraction pipeline."""

    def __init__(self, config, logger):
        self.cfg = config
        self.logger = logger

    def extract_toc(self, pdf_path: Path) -> list[TOCEntry]:
        """Extract TOC entries from PDF."""
        pdf_extractor = PDFExtractor(pdf_path)
        doc_title = pdf_extractor.get_doc_title()

        # Extract first 15 pages for TOC
        pages = pdf_extractor.extract_pages(15)

        # Extract TOC
        toc_extractor = TOCExtractor(doc_title)
        combined_text = "\\n".join(pages)
        toc_entries = toc_extractor.extract_from_content(combined_text)

        # Save TOC
        toc_path = Path(self.cfg.output_directory) / "usb_pd_toc.jsonl"
        write_jsonl(iter(toc_entries), toc_path)

        self.logger.info(f"Extracted {len(toc_entries)} TOC entries to {toc_path}")
        return toc_entries
