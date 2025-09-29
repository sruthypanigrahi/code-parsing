"""PDF content extraction class."""

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Optional


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
                return (
                    title
                    if title and isinstance(title, str)
                    else "USB Power Delivery Specification"
                )
            finally:
                doc.close()  # type: ignore
        except Exception as e:
            self.logger.warning(f"Cannot read PDF metadata: {e}")
            return "USB Power Delivery Specification"

    def extract_pages(self, max_pages: Optional[int] = None) -> list[str]:
        """Extract text from PDF pages."""
        try:
            fitz = _get_fitz()
            doc: Any = fitz.open(str(self.pdf_path))  # type: ignore
        except Exception as e:
            raise RuntimeError(f"Cannot open PDF {self.pdf_path}: {e}") from e

        try:
            total_pages = len(doc) if max_pages is None else min(max_pages, len(doc))  # type: ignore
            self.logger.info(f"Extracting {total_pages} pages from {self.pdf_path}")

            pages: list[str] = []
            for i in range(total_pages):
                page: Any = doc[i]  # type: ignore
                text: str = str(page.get_text("text") or "")  # type: ignore
                pages.append(text)

            return pages
        finally:
            doc.close()  # type: ignore

    def extract_structured_content(
        self, max_pages: Optional[int] = None
    ) -> Iterator[dict[str, Any]]:
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
                yield from self._extract_page_content(page, page_num)

        finally:
            doc.close()  # type: ignore

    def _extract_page_content(
        self, page: Any, page_num: int
    ) -> Iterator[dict[str, Any]]:
        """Extract content from a single page."""
        # Extract text blocks
        yield from self._extract_text_blocks(page, page_num)

        # Extract images
        yield from self._extract_images(page, page_num)

        # Extract tables
        yield from self._extract_tables(page, page_num)

    def _extract_text_blocks(
        self, page: Any, page_num: int
    ) -> Iterator[dict[str, Any]]:
        """Extract text blocks from page."""
        blocks = page.get_text("dict")["blocks"]  # type: ignore

        for block_num, block in enumerate(blocks):  # type: ignore
            if "lines" not in block:
                continue

            text_content = self._extract_block_text(block)
            if text_content.strip():
                yield {
                    "type": "paragraph",
                    "content": text_content.strip(),
                    "page": page_num + 1,
                    "block_id": f"p{page_num + 1}_{block_num}",
                    "bbox": list(block.get("bbox", [])),  # type: ignore
                }

    def _extract_block_text(self, block: dict) -> str:
        """Extract text from a text block."""
        text_content = ""
        for line in block["lines"]:  # type: ignore
            for span in line["spans"]:  # type: ignore
                text_content += str(span["text"])  # type: ignore
        return text_content

    def _extract_images(self, page: Any, page_num: int) -> Iterator[dict[str, Any]]:
        """Extract images from page."""
        blocks = page.get_text("dict")["blocks"]  # type: ignore

        for block_num, block in enumerate(blocks):  # type: ignore
            if "image" not in block:
                continue

            bbox: Any = block.get("bbox", [0, 0, 0, 0])  # type: ignore
            width, height = self._get_image_dimensions(bbox)

            # Include images larger than 10x10 pixels
            if width > 10 and height > 10:
                yield {
                    "type": "image",
                    "content": f"[Image {width:.0f}x{height:.0f} on page {page_num + 1}]",
                    "page": page_num + 1,
                    "block_id": f"img{page_num + 1}_{block_num}",
                    "bbox": list(bbox) if bbox else [],  # type: ignore
                }

    def _get_image_dimensions(self, bbox: Any) -> tuple[float, float]:
        """Get image width and height from bounding box."""
        if not bbox or len(bbox) < 4:
            return 0.0, 0.0
        width = float(bbox[2] - bbox[0])
        height = float(bbox[3] - bbox[1])
        return width, height

    def _extract_tables(self, page: Any, page_num: int) -> Iterator[dict[str, Any]]:
        """Extract tables from page."""
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

    def _detect_tables(self, page: Any) -> list[str]:
        """Enhanced table detection."""
        text: str = page.get_text()  # type: ignore
        lines = text.split("\n")

        table_indicators = ["Table", "Figure", "|", "\t"]
        potential_tables: list[str] = []
        current_table: list[str] = []

        for line in lines:
            line = line.strip()
            if not line:
                if len(current_table) >= 3:
                    potential_tables.append("\n".join(current_table))
                current_table = []
                continue

            if self._is_table_line(line, table_indicators):
                current_table.append(line)
            else:
                if len(current_table) >= 3:
                    potential_tables.append("\n".join(current_table))
                current_table = []

        # Add final table if exists
        if len(current_table) >= 3:
            potential_tables.append("\n".join(current_table))

        return potential_tables

    def _is_table_line(self, line: str, indicators: list[str]) -> bool:
        """Check if line looks like part of a table."""
        return (
            any(indicator in line for indicator in indicators)
            or line.count("  ") >= 3  # Multiple spaces
            or line.count("\t") >= 2  # Tab characters
            or (len(line) > 30 and line.count(" ") > 10)  # Long lines with many spaces
        )
