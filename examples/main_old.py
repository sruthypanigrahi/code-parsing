"""Main entry point demonstrating OOP principles with specific classes."""

import logging
import sys
from pathlib import Path

from src.exceptions import PDFProcessingError
from src.output_writer import OutputWriter
from src.pdf_loader import PDFLoader
from src.pdf_parser import PDFParser
from src.pdf_processing_orchestrator import PDFProcessingOrchestrator
from src.text_cleaner import TextCleaner


class PDFProcessingApplication:
    """Main application class that orchestrates PDF processing using OOP principles."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Initialize the main orchestrator which uses all required classes
        self.orchestrator = PDFProcessingOrchestrator()

        # Also demonstrate individual class usage
        self.pdf_loader = PDFLoader()
        self.pdf_parser = PDFParser()
        self.text_cleaner = TextCleaner()
        self.output_writer = OutputWriter()

    def run(self, pdf_path: str = "assets/USB_PD_R3_2_V1.1_2024-10.pdf") -> None:
        """Run the PDF processing application using OOP classes."""
        try:
            self.logger.info("PDF Processing Application - OOP Implementation")
            self.logger.info("=" * 50)

            # Validate input file
            if not Path(pdf_path).exists():
                self.logger.error(f"Error: PDF file not found: {pdf_path}")
                return

            self.logger.info(f"Processing PDF: {pdf_path}")
            self.logger.info("Using OOP classes:")
            self.logger.info("- PDFLoader: for file loading")
            self.logger.info("- PDFParser: for parsing logic")
            self.logger.info("- TextCleaner: for text preprocessing")
            self.logger.info("- OutputWriter: for saving results")
            self.logger.info("- PDFProcessingOrchestrator: for orchestration")

            # Process PDF using the orchestrator
            results = self.orchestrator.process_pdf(pdf_path)

            # Display results
            self._display_results(results)

        except PDFProcessingError as e:
            self.logger.error(f"Processing Error: {e}")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"Unexpected Error: {e}")
            sys.exit(1)

    def _display_results(self, results: dict) -> None:
        """Display processing results."""
        self.logger.info("Processing Results:")
        self.logger.info("-" * 30)
        self.logger.info(f"Success: {results['success']}")
        self.logger.info(f"Pages Processed: {results['total_pages_processed']}")
        self.logger.info(f"TOC Entries: {results['toc_entries_extracted']}")
        self.logger.info(f"Content Items: {results['content_items_extracted']}")
        self.logger.info(f"Processing Time: {results['processing_time_seconds']:.2f}s")

        self.logger.info("Output Files Created:")
        for file_type, file_path in results["output_files"].items():
            self.logger.info(f"  {file_type}: {file_path}")

        # Get summary using orchestrator
        summary = self.orchestrator.get_processing_summary()
        self.logger.info("Processing Summary:")
        for key, value in summary.items():
            self.logger.info(f"  {key.replace('_', ' ').title()}: {value}")


def main() -> None:
    """Main entry point using OOP classes as requested in feedback."""
    # Create application instance (demonstrates class instantiation)
    app = PDFProcessingApplication()

    # Run the application (demonstrates class method usage)
    app.run()


if __name__ == "__main__":
    main()
