"""PDF extractor with OOP principles."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional


class BaseExtractor(ABC):  # Abstraction
    """Abstract PDF extractor (Abstraction, Encapsulation)."""
    
    def __init__(self, pdf_path: Path):
        self._pdf_path = pdf_path  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    @abstractmethod  # Abstraction
    def extract(self) -> Any:
        pass
    
    def _get_fitz(self):  # Encapsulation
        import fitz  # type: ignore
        return fitz


class PDFExtractor(BaseExtractor):  # Inheritance
    """PDF content extractor (Inheritance, Polymorphism)."""
    
    def extract(self) -> List[Dict[str, Any]]:  # Polymorphism
        return list(self.extract_structured_content())
    
    def extract_content(self, pdf_path: Path, 
                       max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        self._pdf_path = pdf_path
        return list(self.extract_structured_content(max_pages))
    
    def extract_structured_content(self, 
                                 max_pages: Optional[int] = None
                                 ) -> Iterator[Dict[str, Any]]:
        fitz = self._get_fitz()
        doc = fitz.open(str(self._pdf_path))  # type: ignore
        try:
            doc_length: int = len(doc)  # type: ignore
            total_pages = (doc_length if max_pages is None 
                          else min(max_pages, doc_length))
            for page_num in range(total_pages):
                yield from self._extract_page_content(doc[page_num], page_num)
        finally:
            doc.close()  # type: ignore
    
    def _extract_page_content(self, page: Any, 
                            page_num: int) -> Iterator[Dict[str, Any]]:
        """Extract content from page (Encapsulation)."""
        blocks = page.get_text("dict")["blocks"]  # type: ignore
        for block_num, block in enumerate(blocks):
            if "lines" in block:
                text = self._get_block_text(block)
                if text.strip():
                    yield {
                        "type": "paragraph",
                        "content": text.strip(),
                        "page": page_num + 1,
                        "block_id": f"p{page_num + 1}_{block_num}",
                        "bbox": list(block.get("bbox", []))
                    }
            elif "image" in block:
                bbox = block.get("bbox", [0, 0, 0, 0])
                width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                if width > 10 and height > 10:
                    yield {
                        "type": "image",
                        "content": f"[Image {width:.0f}x{height:.0f}]",
                        "page": page_num + 1,
                        "block_id": f"img{page_num + 1}_{block_num}",
                        "bbox": list(bbox)
                    }
    
    def _get_block_text(self, block: Dict[str, Any]) -> str:  # Encapsulation
        text = ""
        for line in block["lines"]:  # type: ignore
            for span in line["spans"]:  # type: ignore
                text += str(span["text"])  # type: ignore
        return text
    
    def _is_table_line(self, line: str) -> bool:  # Encapsulation
        return ("Table" in line or "|" in line or line.count("  ") >= 3)