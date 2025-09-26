"""Main pipeline orchestrator class."""

from pathlib import Path
from typing import List, Dict, Any
from .config import Config
from .logger import get_logger
from .pdf_extractor import PDFExtractor
from .toc_pipeline import TOCPipeline
from .content_pipeline import ContentPipeline
from .spec_builder import SpecBuilder
from .models import TOCEntry
from .performance import timer, timed_operation, monitor
from .exceptions import USBPDParserError


class PipelineOrchestrator:
    """Orchestrates the complete PDF processing pipeline."""

    def __init__(self, config_path: str = "application.yml", debug: bool = False):
        self.cfg = Config(config_path)
        self.logger = get_logger(output_dir=self.cfg.output_directory, debug=debug)
        self.toc_pipeline = TOCPipeline(self.cfg, self.logger)
        self.content_pipeline = ContentPipeline(self.cfg, self.logger)
        self.spec_builder = SpecBuilder(self.cfg, self.logger)

    @timer
    def run_full_pipeline(self, mode: int = 1) -> Dict[str, Any]:
        """Run the complete pipeline with TOC and content extraction."""
        try:
            pdf_path = Path(self.cfg.pdf_input_file)
            max_pages = None if mode == 1 else (600 if mode == 2 else 200)

            # Extract TOC
            with timed_operation("TOC extraction"):
                toc_entries = self.toc_pipeline.extract_toc(pdf_path)

            # Extract content
            with timed_operation("Content extraction"):
                content_count = self.content_pipeline.extract_content(
                    pdf_path, max_pages
                )

            # Create spec file
            with timed_operation("Creating spec file"):
                spec_path = Path(self.cfg.output_directory) / "usb_pd_spec.jsonl"
                spec_counts = self.spec_builder.create_spec_file(spec_path)

            # Build results
            results = {
                "toc_entries": len(toc_entries),
                "toc_path": str(Path(self.cfg.output_directory) / "usb_pd_toc.jsonl"),
                "content_items": content_count,
                "content_path": str(
                    Path(self.cfg.output_directory) / "usb_pd_content.jsonl"
                ),
                "spec_path": str(spec_path),
                "spec_counts": spec_counts,
            }

            # Record metrics
            monitor.record("toc_entries", len(toc_entries))
            monitor.record("content_items", content_count)

            self.logger.info(f"Pipeline completed successfully")
            self.logger.info(f"TOC entries: {len(toc_entries)}")
            self.logger.info(f"Content items: {content_count}")
            self.logger.info(f"Spec file counts: {spec_counts}")
            monitor.report()

            return results

        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}")
            raise USBPDParserError(f"Pipeline execution failed: {e}") from e

    def run_toc_only(self) -> List[TOCEntry]:
        """Extract only TOC entries."""
        try:
            pdf_path = Path(self.cfg.pdf_input_file)
            return self.toc_pipeline.extract_toc(pdf_path)
        except Exception as e:
            self.logger.error(f"TOC extraction failed: {e}")
            raise USBPDParserError(f"TOC extraction failed: {e}") from e

    def run_content_only(self) -> int:
        """Extract only content (paragraphs, images, tables)."""
        try:
            pdf_path = Path(self.cfg.pdf_input_file)
            return self.content_pipeline.extract_content(pdf_path)
        except Exception as e:
            self.logger.error(f"Content extraction failed: {e}")
            raise USBPDParserError(f"Content extraction failed: {e}") from e
