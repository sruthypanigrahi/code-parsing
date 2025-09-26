"""PDF content extraction class."""

from pathlib import Path
from typing import Iterator, Optional, List, Dict, Any
import logging
import fitz  # type: ignore
from .exceptions import PDFNotFoundError


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
            doc = fitz.open(str(self.pdf_path))
            try:
                metadata = doc.metadata
                title = metadata.get("title")
                return title if title else "USB Power Delivery Specification"
            finally:
                doc.close()
        except Exception as e:
            self.logger.warning(f"Cannot read PDF metadata: {e}")
            return "USB Power Delivery Specification"
    
    def extract_pages(self, max_pages: Optional[int] = None) -> List[str]:
        """Extract text from PDF pages."""
        try:
            doc = fitz.open(str(self.pdf_path))
        except Exception as e:
            raise RuntimeError(f"Cannot open PDF {self.pdf_path}: {e}") from e

        try:
            total_pages = len(doc) if max_pages is None else min(max_pages, len(doc))
            self.logger.info(f"Extracting {total_pages} pages from {self.pdf_path}")

            pages = []
            for i in range(total_pages):
                page = doc[i]
                text = page.get_text("text") or ""
                pages.append(text)
            
            return pages
        finally:
            doc.close()
    
    def extract_structured_content(self, max_pages: Optional[int] = None) -> Iterator[Dict[str, Any]]:
        """Extract structured content including paragraphs, images, and tables."""
        try:
            doc = fitz.open(str(self.pdf_path))
        except Exception as e:
            raise RuntimeError(f"Cannot open PDF {self.pdf_path}: {e}") from e

        try:
            total_pages = len(doc) if max_pages is None else min(max_pages, len(doc))
            
            for page_num in range(total_pages):
                page = doc[page_num]
                
                # Extract text blocks (paragraphs)
                blocks = page.get_text("dict")["blocks"]
                
                for block_num, block in enumerate(blocks):
                    if "lines" in block:  # Text block
                        text_content = ""
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text_content += span["text"]
                        
                        if text_content.strip():
                            yield {
                                "type": "paragraph",
                                "content": text_content.strip(),
                                "page": page_num + 1,
                                "block_id": f"p{page_num + 1}_{block_num}",
                                "bbox": block.get("bbox", [])
                            }
                    
                    elif "image" in block:  # Image block
                        # Filter out very small images (likely icons/decorations)
                        bbox = block.get("bbox", [0, 0, 0, 0])
                        width = bbox[2] - bbox[0] if len(bbox) >= 4 else 0
                        height = bbox[3] - bbox[1] if len(bbox) >= 4 else 0
                        
                        # Include images larger than 10x10 pixels
                        if width > 10 and height > 10:
                            yield {
                                "type": "image",
                                "content": f"[Image {width:.0f}x{height:.0f} on page {page_num + 1}]",
                                "page": page_num + 1,
                                "block_id": f"img{page_num + 1}_{block_num}",
                                "bbox": bbox
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
                            "bbox": []
                        }
        
        finally:
            doc.close()
    
    def _detect_tables(self, page) -> List[str]:
        """Enhanced table detection."""
        text = page.get_text()
        tables = []
        lines = text.split('\n')
        
        # Look for table patterns
        table_indicators = ['Table', 'Figure', '|', '\t']
        potential_tables = []
        current_table = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if len(current_table) >= 3:
                    potential_tables.append('\n'.join(current_table))
                current_table = []
                continue
            
            # Check for table-like content
            if (any(indicator in line for indicator in table_indicators) or
                line.count('  ') >= 3 or  # Multiple spaces
                line.count('\t') >= 2 or  # Tab characters
                (len(line) > 30 and line.count(' ') > 10)):  # Long lines with many spaces
                current_table.append(line)
            else:
                if len(current_table) >= 3:
                    potential_tables.append('\n'.join(current_table))
                current_table = []
        
        # Add final table if exists
        if len(current_table) >= 3:
            potential_tables.append('\n'.join(current_table))
        
        return potential_tables