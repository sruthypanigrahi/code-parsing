"""Main orchestrator for PDF processing using OOP principles."""

import time
from pathlib import Path
from typing import Any, Dict, Optional

from .exceptions import PDFProcessingError
from .output_writer import OutputWriter
from .pdf_loader import PDFLoader
from .pdf_parser import PDFParser
from .text_cleaner import TextCleaner


class PDFProcessingOrchestrator:
    """Orchestrates the entire PDF processing workflow using OOP principles."""

    def __init__(self, output_dir: str = "outputs"):
        # Initialize all components following single responsibility principle
        self.pdf_loader = PDFLoader()
        self.pdf_parser = PDFParser()
        self.text_cleaner = TextCleaner()
        self.output_writer = OutputWriter(output_dir)

        # Processing state
        self.processing_stats = {}
        self.extraction_data = {}

    def process_pdf(
        self, pdf_path: str, max_pages: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Main processing method that orchestrates all classes.
        Each class handles its single responsibility.
        """
        start_time = time.time()

        try:
            # Step 1: Load PDF using PDFLoader
            print("Loading PDF document...")
            document = self.pdf_loader.load_pdf(pdf_path)
            document_info = self.pdf_loader.get_document_info()

            # Step 2: Parse PDF using PDFParser
            print("Parsing PDF content...")
            parsed_data = self.pdf_parser.parse_document(Path(pdf_path))

            # Step 3: Clean text using TextCleaner
            print("Cleaning extracted text...")
            cleaned_toc = []
            for entry in parsed_data["toc"]:
                entry.title = self.text_cleaner.clean_toc_entry(entry.title)
                cleaned_toc.append(entry)

            cleaned_content = []
            for item in parsed_data["content"]:
                item.content = self.text_cleaner.clean_text(item.content)
                cleaned_content.append(item)

            # Step 4: Prepare extraction data
            self.extraction_data = {
                "toc": cleaned_toc,
                "content": cleaned_content,
                "total_pages": parsed_data["total_pages"],
                "document_info": document_info,
                "extraction_time": time.time() - start_time,
            }

            # Step 5: Write outputs using OutputWriter
            print("Writing output files...")
            output_files = self.output_writer.write_all_formats(self.extraction_data)

            # Step 6: Generate processing statistics
            self.processing_stats = {
                "success": True,
                "total_pages_processed": parsed_data["total_pages"],
                "toc_entries_extracted": len(cleaned_toc),
                "content_items_extracted": len(cleaned_content),
                "processing_time_seconds": time.time() - start_time,
                "output_files": output_files,
                "document_info": document_info,
            }

            return self.processing_stats

        except Exception as e:
            error_stats = {
                "success": False,
                "error": str(e),
                "processing_time_seconds": time.time() - start_time,
            }
            raise PDFProcessingError(f"PDF processing failed: {str(e)}") from e

        finally:
            # Clean up resources
            self.cleanup()

    def get_processing_summary(self) -> Dict[str, Any]:
        """Get summary of the processing results."""
        if not self.processing_stats:
            return {"status": "No processing completed yet"}

        return {
            "processing_status": (
                "Success" if self.processing_stats.get("success") else "Failed"
            ),
            "document_pages": self.processing_stats.get("total_pages_processed", 0),
            "toc_entries": self.processing_stats.get("toc_entries_extracted", 0),
            "content_items": self.processing_stats.get("content_items_extracted", 0),
            "processing_time": f"{self.processing_stats.get('processing_time_seconds', 0):.2f}s",
            "output_files_created": len(self.processing_stats.get("output_files", {})),
        }

    def configure_text_cleaning(self, **cleaning_rules):
        """Configure text cleaning rules."""
        self.text_cleaner.configure_cleaning(**cleaning_rules)

    def cleanup(self):
        """Clean up all resources."""
        try:
            self.pdf_loader.close()
            self.pdf_parser.close()
        except Exception:
            pass  # Ignore cleanup errors
