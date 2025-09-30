"""PDF extractor with OOP principles."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional
from .content_analyzer import ContentAnalyzer


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
    """Fast PDF content extractor (Inheritance, Polymorphism)."""
    
    def __init__(self, pdf_path: Path):
        super().__init__(pdf_path)
        self._analyzer = ContentAnalyzer()  # Composition
    
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
        """Fast page content extraction (Encapsulation)."""
        # Fast text extraction
        blocks = page.get_text("dict")["blocks"]  # type: ignore
        for block_num, block in enumerate(blocks):
            if "lines" in block:
                text = self._get_block_text(block)
                if text.strip() and len(text) > 5:
                    content_type = self._analyzer.classify_content(text)
                    yield {
                        "type": content_type,
                        "content": text.strip(),
                        "page": page_num + 1,
                        "block_id": f"{content_type[0]}{page_num + 1}_{block_num}",
                        "bbox": list(block.get("bbox", []))
                    }
        
        # Extract high-value structured content only
        full_text = page.get_text()  # type: ignore
        yield from self._analyzer.extract_structured_items(full_text, page_num)
    
    def _get_block_text(self, block: Dict[str, Any]) -> str:  # Encapsulation
        return "".join(
            str(span["text"]) 
            for line in block["lines"] 
            for span in line["spans"]
        )
    

    

    
    def _extract_tables(self, page: Any, page_num: int) -> Iterator[Dict[str, Any]]:
        """Extract tables using pdfplumber (Encapsulation)."""
        try:
            import pdfplumber  # type: ignore
            with pdfplumber.open(str(self._pdf_path)) as pdf:
                if page_num < len(pdf.pages):
                    plumber_page = pdf.pages[page_num]
                    tables = plumber_page.extract_tables()
                    for table_num, table in enumerate(tables or []):
                        if table and len(table) > 1:
                            table_text = "\n".join(
                                " | ".join(str(cell or "") for cell in row) 
                                for row in table
                            )
                            yield {
                                "type": "table",
                                "content": table_text,
                                "page": page_num + 1,
                                "block_id": f"tbl{page_num + 1}_{table_num}",
                                "bbox": []
                            }
        except Exception:
            pass  # Fallback gracefully if pdfplumber fails