"""Content extraction pipeline."""

import logging
from pathlib import Path
from typing import Optional

from .config import Config
from .content_processor import ContentProcessor
from .pdf_extractor import PDFExtractor


class ContentPipeline:
    """Handles content extraction pipeline."""

    def __init__(self, config: Config, logger: logging.Logger):
        self.cfg = config
        self.logger = logger

    def extract_content(self, pdf_path: Path, max_pages: Optional[int] = None) -> int:
        """Extract structured content from PDF."""
        pdf_extractor = PDFExtractor(pdf_path)
        doc_title = pdf_extractor.get_doc_title()

        # Extract structured content
        content_iterator = pdf_extractor.extract_structured_content(max_pages)
        content_processor = ContentProcessor(doc_title)
        processed_content = content_processor.process_structured_content(
            content_iterator
        )

        # Save content directly to spec file
        spec_path = Path(self.cfg.output_directory) / "usb_pd_spec.jsonl"
        content_count = content_processor.save_content(processed_content, spec_path)

        self.logger.info(f"Extracted {content_count} content items to {spec_path}")
        return content_count
