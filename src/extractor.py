"""PDF content extraction utilities."""

from pathlib import Path
from typing import Iterator, Optional
import logging

try:
    import fitz  # type: ignore # PyMuPDF
except ImportError as e:
    raise ImportError("PyMuPDF is required: pip install PyMuPDF") from e

from .exceptions import PDFNotFoundError

logger = logging.getLogger(__name__)


def extract_front_pages(pdf_path: Path, max_pages: Optional[int] = 10) -> Iterator[str]:
    """Extract text from front pages of PDF.

    Args:
        pdf_path: Path to PDF file
        max_pages: Maximum number of pages to extract (None for all pages, default: 10)

    Yields:
        str: Text content of each page

    Raises:
        PDFNotFoundError: If PDF file doesn't exist
        RuntimeError: If PDF cannot be opened
    """
    if not pdf_path.exists():
        raise PDFNotFoundError(f"PDF not found: {pdf_path}")

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as e:
        raise RuntimeError(f"Cannot open PDF {pdf_path}: {e}") from e

    try:
        total_pages = len(doc) if max_pages is None else min(max_pages, len(doc))
        logger.debug(f"Extracting {total_pages} pages from {pdf_path}")

        for i in range(total_pages):
            page = doc[i]
            text = page.get_text("text") or ""
            yield text
    finally:
        doc.close()


def get_doc_title(pdf_path: Path) -> str:
    """Extract document title from PDF metadata.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Document title or default if not found

    Raises:
        PDFNotFoundError: If PDF file doesn't exist
    """
    if not pdf_path.exists():
        raise PDFNotFoundError(f"PDF not found: {pdf_path}")

    try:
        doc = fitz.open(str(pdf_path))
        try:
            metadata = doc.metadata
            title = metadata.get("title")
            return title if title else "USB Power Delivery Specification"
        finally:
            doc.close()
    except Exception as e:
        logger.warning(f"Cannot read PDF metadata: {e}")
        return "USB Power Delivery Specification"
