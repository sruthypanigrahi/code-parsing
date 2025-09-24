"""Application orchestrator for USB PD Parser."""

from typing import List, Any
from .config import Config
from .logger import get_logger
from .extractor import PDFExtractor
from .parser import TOCParser

from .validator import Validator
from .models import PageContent, TOCEntry



class USBPDParser:
    """Main application class for USB PD specification parsing."""
    
    def __init__(self, config_path: str = "application.yml"):
        self.cfg = Config(config_path)
        self.logger = get_logger(output_dir=self.cfg.output_directory)
    
    def run(self) -> None:
        """Execute the complete parsing workflow."""
        try:
            pages = self._extract_content()
            toc_entries = self._parse_toc(pages)
            self._save_results(pages, toc_entries)
            self._validate_and_report(toc_entries, pages)
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
    
    def _extract_content(self) -> List[PageContent]:
        """Extract PDF content."""
        self.logger.info("Starting PDF extraction...")
        extractor = PDFExtractor(
            str(self.cfg.pdf_input_file), 
            self.cfg.output_directory, 
            self.cfg.ocr_fallback, 
            self.cfg.max_pages
        )
        pages = extractor.extract_full_content()
        self.logger.info(f"Extracted {len(pages)} pages.")
        return pages
    
    def _parse_toc(self, pages: List[PageContent]) -> List[TOCEntry]:
        """Parse table of contents."""
        self.logger.info("Parsing Table of Contents...")
        parser = TOCParser()
        toc_entries = parser.parse_toc([(p.page, p.text) for p in pages])
        self.logger.info(f"Found {len(toc_entries)} TOC entries.")
        return toc_entries
    
    def _save_results(self, pages: List[PageContent], toc_entries: List[TOCEntry]) -> None:
        """Save results to file."""
        with open(self.cfg.toc_file, "w", encoding="utf-8") as f:
            for p in pages:
                f.write(p.model_dump_json() + "\n")
            for entry in toc_entries:
                f.write(entry.model_dump_json() + "\n")
    
    def _validate_and_report(self, toc_entries: List[TOCEntry], pages: List[PageContent]) -> None:
        """Validate and report statistics."""
        self.logger.info("Validating TOC...")
        issues: dict[str, Any] = Validator.validate(toc_entries)  # type: ignore
        if any(issues.values()):
            self.logger.warning(f"Validation issues: {len(sum(issues.values(), []))} found")  # type: ignore
        else:
            self.logger.info("TOC validation passed.")
        
        # Statistics
        total_words = sum(len(p.text.split()) for p in pages)
        total_images = sum(p.image_count for p in pages)
        total_tables = sum(p.table_count for p in pages)
        
        self.logger.info(f"Pages: {len(pages)}")
        self.logger.info(f"Words: {total_words}")
        self.logger.info(f"Images: {total_images}")
        self.logger.info(f"Tables: {total_tables}")
        self.logger.info("Done.")