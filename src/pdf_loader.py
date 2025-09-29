"""PDF file loading with validation."""

from pathlib import Path
from typing import Optional

import fitz

from .exceptions import PDFProcessingError


class PDFLoader:
    """Handles PDF file loading and validation with single responsibility."""

    def __init__(self):
        self.pdf_path: Optional[Path] = None
        self.document = None

    def load_pdf(self, pdf_path: str) -> fitz.Document:
        """Load and validate PDF file."""
        self.pdf_path = Path(pdf_path)

        # Validate file exists
        if not self.pdf_path.exists():
            raise PDFProcessingError(f"PDF file not found: {pdf_path}")

        # Validate file extension
        if self.pdf_path.suffix.lower() != ".pdf":
            raise PDFProcessingError(
                f"Invalid file type. Expected PDF, got: {self.pdf_path.suffix}"
            )

        try:
            # Load PDF document
            self.document = fitz.open(self.pdf_path)

            # Validate document is readable
            if len(self.document) == 0:
                raise PDFProcessingError("PDF document is empty or corrupted")

            return self.document

        except Exception as e:
            raise PDFProcessingError(f"Failed to load PDF: {str(e)}")

    def get_document_info(self) -> dict:
        """Get basic document information."""
        if not self.document:
            raise PDFProcessingError("No document loaded")

        return {
            "title": self.document.metadata.get("title", ""),
            "author": self.document.metadata.get("author", ""),
            "subject": self.document.metadata.get("subject", ""),
            "creator": self.document.metadata.get("creator", ""),
            "producer": self.document.metadata.get("producer", ""),
            "total_pages": len(self.document),
            "file_size": self.pdf_path.stat().st_size if self.pdf_path else 0,
        }

    def close(self):
        """Clean up resources."""
        if self.document:
            self.document.close()
            self.document = None
