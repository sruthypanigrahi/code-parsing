"""Minimal pipeline orchestrator."""

import logging
from pathlib import Path
from typing import Any

from .config import Config
from .models import TOCEntry
from .pdf_extractor import PDFExtractor
from .toc_extractor import TOCExtractor
from .output_writer import JSONLWriter


class PipelineOrchestrator:
    """Simple pipeline orchestrator for PDF processing."""
    
    def __init__(self, config_path: str = "application.yml", debug: bool = False):
        self.cfg = Config(config_path)
        self.logger = logging.getLogger(__name__)
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        
        # Ensure output directory exists
        self.cfg.output_directory.mkdir(exist_ok=True)
    
    def run_full_pipeline(self, mode: int = 1) -> dict[str, Any]:
        """Run complete pipeline."""
        pdf_path = self.cfg.pdf_input_file
        max_pages = None if mode == 1 else (600 if mode == 2 else 200)
        
        # Extract TOC
        toc_extractor = TOCExtractor()
        toc_entries = toc_extractor.extract_toc(pdf_path)
        
        # Save TOC
        toc_path = self.cfg.output_directory / "usb_pd_toc.jsonl"
        toc_writer = JSONLWriter(toc_path)
        toc_writer.write_entries(toc_entries)
        
        # Extract content
        pdf_extractor = PDFExtractor()
        content_items = pdf_extractor.extract_content(pdf_path, max_pages)
        
        # Save content
        spec_path = self.cfg.output_directory / "usb_pd_spec.jsonl"
        content_writer = JSONLWriter(spec_path)
        content_writer.write_content(content_items)
        
        # Count content types
        counts = {
            "pages": max_pages or len(set(item.get("page", 0) for item in content_items)),
            "paragraphs": sum(1 for item in content_items if item.get("type") == "paragraph"),
            "images": sum(1 for item in content_items if item.get("type") == "image"),
            "tables": sum(1 for item in content_items if item.get("type") == "table"),
        }
        
        return {
            "toc_entries": len(toc_entries),
            "toc_path": str(toc_path),
            "spec_path": str(spec_path),
            "spec_counts": counts,
        }
    
    def run_toc_only(self) -> list[TOCEntry]:
        """Extract only TOC."""
        toc_extractor = TOCExtractor()
        return toc_extractor.extract_toc(self.cfg.pdf_input_file)
    
    def run_content_only(self) -> int:
        """Extract only content."""
        pdf_extractor = PDFExtractor()
        content_items = pdf_extractor.extract_content(self.cfg.pdf_input_file)
        return len(content_items)