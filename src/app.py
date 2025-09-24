"""Application orchestrator for USB PD Parser."""

from typing import List, Any
from .config import Config
from .logger import get_logger
from .extractor import PDFExtractor
from .parser import TOCParser

from .validator import Validator
from .writer import JSONLWriter
from .models import PageContent, TOCEntry
from pathlib import Path



class USBPDParser:
    """Main application class for USB PD specification parsing."""
    
    def __init__(self, config_path: str = "application.yml", debug: bool = False):
        self.cfg = Config(config_path)
        self.logger = get_logger(output_dir=self.cfg.output_directory, debug=debug)
    
    def run(self) -> None:
        """Execute the complete parsing workflow."""
        try:
            pages = self._extract_content()
            toc_entries = self._parse_toc(pages)
            self._save_results(pages, toc_entries)
            self._validate_and_report(toc_entries, pages)
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise  # Re-raise the exception so main.py can handle it
    
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
        """Save results to file using JSONLWriter."""
        self.logger.info("Saving results...")
        JSONLWriter.write_mixed(pages, toc_entries, self.cfg.toc_file)
        self.logger.info(f"Results saved to {self.cfg.toc_file}")
    
    def _validate_and_report(self, toc_entries: List[TOCEntry], pages: List[PageContent]) -> None:
        """Validate and report statistics with comprehensive validation report."""
        self.logger.info("Validating TOC...")
        
        # Comprehensive validation
        validation_report = Validator.validate_comprehensive(toc_entries, pages)
        
        # Save validation report
        report_path = self.cfg.output_directory / "validation_report.json"
        validation_report.save_to_file(report_path)
        
        # Log validation results
        if validation_report.validation_passed:
            self.logger.info("TOC validation passed.")
        else:
            issues_count = (
                len(validation_report.duplicates) +
                len(validation_report.out_of_order) +
                len(validation_report.missing_pages) +
                len(validation_report.duplicate_pages)
            )
            self.logger.warning(f"Validation issues: {issues_count} found")
            
            if validation_report.duplicates:
                self.logger.warning(f"Duplicate section IDs: {validation_report.duplicates}")
            if validation_report.out_of_order:
                self.logger.warning(f"Out-of-order sections: {validation_report.out_of_order}")
            if validation_report.missing_pages:
                self.logger.warning(f"Missing pages: {validation_report.missing_pages}")
            if validation_report.duplicate_pages:
                self.logger.warning(f"Duplicate page numbers: {validation_report.duplicate_pages}")
        
        self.logger.info(f"Validation report saved to: {report_path}")
        
        # Statistics
        total_words = sum(len(p.text.split()) for p in pages)
        total_images = sum(p.image_count for p in pages)
        total_tables = sum(p.table_count for p in pages)
        
        self.logger.info(f"Pages: {len(pages)}")
        self.logger.info(f"Words: {total_words}")
        self.logger.info(f"Images: {total_images}")
        self.logger.info(f"Tables: {total_tables}")
        self.logger.info(f"TOC Entries: {len(toc_entries)}")
        self.logger.info("Done.")