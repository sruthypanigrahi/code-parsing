"""PDF content extraction class."""

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Dict, List, Optional

# Create PDFNotFoundError if not imported from exceptions
class PDFNotFoundError(Exception):
    """Raised when PDF file is not found."""
    pass

# Lazy import for heavy library
def _get_fitz():
    import fitz  # type: ignore
    return fitz


class PDFExtractor:
    """Handles PDF content extraction with different modes."""

    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.logger = logging.getLogger(__name__)

        if not pdf_path.exists():
            raise PDFNotFoundError(f"PDF not found: {pdf_path}")

    def get_doc_title(self) -> str:
        """Extract document title from PDF metadata."""
        try:
            fitz = _get_fitz()
            doc: Any = fitz.open(str(self.pdf_path))  # type: ignore
            try:
                metadata: Any = doc.metadata  # type: ignore
                title: Optional[str] = metadata.get("title") if metadata else None  # type: ignore
                return title if title and isinstance(title, str) else "USB Power Delivery Specification"
            finally:
                doc.close()  # type: ignore
        except Exception as e:
            self.logger.warning(f"Cannot read PDF metadata: {e}")
            return "USB Power Delivery Specification"

    def extract_pages(self, max_pages: Optional[int] = None) -> List[str]:
        """Extract text from PDF pages."""
        try:
            fitz = _get_fitz()
            doc: Any = fitz.open(str(self.pdf_path))  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Cannot open PDF {self.pdf_path}: {e}") from e

        try:
            total_pages = len(doc) if max_pages is None else min(max_pages, len(doc))  # type: ignore
            self.logger.info(f"Extracting {total_pages} pages from {self.pdf_path}")

            pages: List[str] = []
            for i in range(total_pages):
                page: Any = doc[i]  # type: ignore
                text: str = str(page.get_text("text") or "")  # type: ignore
                pages.append(text)

            return pages
        finally:
            doc.close()  # type: ignore

    def extract_structured_content(
        self, max_pages: Optional[int] = None
    ) -> Iterator[Dict[str, Any]]:
        """Extract structured content including paragraphs, images, and tables."""
        try:
            fitz = _get_fitz()
            doc: Any = fitz.open(str(self.pdf_path))  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Cannot open PDF {self.pdf_path}: {e}") from e

        try:
            total_pages = len(doc) if max_pages is None else min(max_pages, len(doc))  # type: ignore

            for page_num in range(total_pages):
                page: Any = doc[page_num]  # type: ignore

                # Extract text blocks (paragraphs)
                blocks = page.get_text("dict")["blocks"]  # type: ignore

                for block_num, block in enumerate(blocks):  # type: ignore
                    if "lines" in block:  # Text block
                        text_content: str = ""
                        for line in block["lines"]:  # type: ignore
                            for span in line["spans"]:  # type: ignore
                                text_content += str(span["text"])  # type: ignore

                        if text_content.strip():
                            yield {
                                "type": "paragraph",
                                "content": text_content.strip(),
                                "page": page_num + 1,
                                "block_id": f"p{page_num + 1}_{block_num}",
                                "bbox": list(block.get("bbox", [])),  # type: ignore
                            }

                    elif "image" in block:  # Image block
                        # Filter out very small images (likely icons/decorations)
                        bbox: Any = block.get("bbox", [0, 0, 0, 0])  # type: ignore
                        width: float = float(bbox[2] - bbox[0]) if bbox and len(bbox) >= 4 else 0  # type: ignore
                        height: float = float(bbox[3] - bbox[1]) if bbox and len(bbox) >= 4 else 0  # type: ignore

                        # Include images larger than 10x10 pixels
                        if width > 10 and height > 10:
                            yield {
                                "type": "image",
                                "content": f"[Image {width:.0f}x{height:.0f} on page {page_num + 1}]",
                                "page": page_num + 1,
                                "block_id": f"img{page_num + 1}_{block_num}",
                                "bbox": list(bbox) if bbox else [],  # type: ignore
                            }

                # Extract tables with better detection
                tables = self._detect_tables(page)
                for table_num, table in enumerate(tables):
                    if len(table.strip()) > 100:  # Only include substantial tables
                        yield {
                            "type": "table",
                            "content": table,
                            "page": page_num + 1,
                            "block_id": f"tbl{page_num + 1}_{table_num}",
                            "bbox": [],
                        }

        finally:
            doc.close()  # type: ignore

    def _detect_tables(self, page: Any) -> List[str]:
        """Enhanced table detection."""
        text: str = page.get_text()  # type: ignore
        # tables: List[str] = []  # Unused variable
        lines = text.split("\n")

        # Look for table patterns
        table_indicators = ["Table", "Figure", "|", "\t"]
        potential_tables: List[str] = []
        current_table: List[str] = []

        for line in lines:
            line = line.strip()
            if not line:
                if len(current_table) >= 3:
                    potential_tables.append("\n".join(current_table))
                current_table = []
                continue

            # Check for table-like content
            if (
                any(indicator in line for indicator in table_indicators)
                or line.count("  ") >= 3  # Multiple spaces
                or line.count("\t") >= 2  # Tab characters
                or (len(line) > 30 and line.count(" ") > 10)
            ):  # Long lines with many spaces
                current_table.append(line)
            else:
                if len(current_table) >= 3:
                    potential_tables.append("\n".join(current_table))
                current_table = []

        # Add final table if exists
        if len(current_table) >= 3:
            potential_tables.append("\n".join(current_table))

        return potential_tables
