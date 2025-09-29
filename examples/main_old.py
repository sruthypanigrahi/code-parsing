"""Main entry point demonstrating OOP principles with specific classes."""

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
            print("PDF Processing Application - OOP Implementation")
            print("=" * 50)

            # Validate input file
            if not Path(pdf_path).exists():
                print(f"Error: PDF file not found: {pdf_path}")
                return

            print(f"Processing PDF: {pdf_path}")
            print("\nUsing OOP classes:")
            print("- PDFLoader: for file loading")
            print("- PDFParser: for parsing logic")
            print("- TextCleaner: for text preprocessing")
            print("- OutputWriter: for saving results")
            print("- PDFProcessingOrchestrator: for orchestration")
            print()

            # Process PDF using the orchestrator
            results = self.orchestrator.process_pdf(pdf_path)

            # Display results
            self._display_results(results)

        except PDFProcessingError as e:
            print(f"Processing Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected Error: {e}")
            sys.exit(1)

    def _display_results(self, results: dict) -> None:
        """Display processing results."""
        print("\nProcessing Results:")
        print("-" * 30)
        print(f"Success: {results['success']}")
        print(f"Pages Processed: {results['total_pages_processed']}")
        print(f"TOC Entries: {results['toc_entries_extracted']}")
        print(f"Content Items: {results['content_items_extracted']}")
        print(f"Processing Time: {results['processing_time_seconds']:.2f}s")

        print("\nOutput Files Created:")
        for file_type, file_path in results["output_files"].items():
            print(f"  {file_type}: {file_path}")

        # Get summary using orchestrator
        summary = self.orchestrator.get_processing_summary()
        print("\nProcessing Summary:")
        for key, value in summary.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")


def main() -> None:
    """Main entry point using OOP classes as requested in feedback."""
    # Create application instance (demonstrates class instantiation)
    app = PDFProcessingApplication()

    # Run the application (demonstrates class method usage)
    app.run()


if __name__ == "__main__":
    main()
