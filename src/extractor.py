"""PDF extraction with OOP principles."""

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional

try:
    import fitz  # type: ignore
except ImportError as e:
    raise ImportError("PyMuPDF required") from e


class PDFNotFoundError(Exception):  # Encapsulation
    pass


class BaseExtractor:  # Abstraction
    """Base extractor (Abstraction, Encapsulation)."""
    
    def __init__(self, pdf_path: Path):
        self._pdf_path = pdf_path  # Encapsulation
        self._logger = logging.getLogger(__name__)  # Encapsulation
        if not pdf_path.exists():
            raise PDFNotFoundError(f"PDF not found: {pdf_path}")


class FrontPageExtractor(BaseExtractor):  # Inheritance
    """Front page extractor (Inheritance, Polymorphism)."""
    
    def extract_pages(self, max_pages: Optional[int] = 10) -> Iterator[str]:  # Polymorphism
        try:
            doc: Any = fitz.open(str(self._pdf_path))  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Cannot open PDF: {e}") from e
        
        try:
            doc_length: int = len(doc)  # type: ignore
            total_pages = (doc_length if max_pages is None 
                          else min(max_pages, doc_length))
            for i in range(total_pages):
                yield str(doc[i].get_text("text") or "")  # type: ignore
        finally:
            doc.close()  # type: ignore


class TitleExtractor(BaseExtractor):  # Inheritance
    """Title extractor (Inheritance, Polymorphism)."""
    
    def get_title(self) -> str:  # Polymorphism
        try:
            doc: Any = fitz.open(str(self._pdf_path))  # type: ignore
            try:
                metadata = doc.metadata  # type: ignore
                title = metadata.get("title") if metadata else None  # type: ignore
                return title if isinstance(title, str) else "USB Power Delivery Specification"
            finally:
                doc.close()  # type: ignore
        except Exception as e:
            self._logger.warning(f"Cannot read metadata: {e}")
            return "USB Power Delivery Specification"


# Factory functions (Abstraction)
def extract_front_pages(pdf_path: Path, max_pages: Optional[int] = 10) -> Iterator[str]:
    return FrontPageExtractor(pdf_path).extract_pages(max_pages)


def get_doc_title(pdf_path: Path) -> str:
    return TitleExtractor(pdf_path).get_title()