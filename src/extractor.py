import fitz  # type: ignore # PyMuPDF
import pdfplumber
from pathlib import Path
from typing import List, Any
from .models import PageContent


class PDFExtractor:
    """Extracts content from PDF files efficiently."""

    def __init__(self, pdf_path: str, output_dir: Path, ocr_fallback: bool = True, max_pages: int | None = None):
        self._pdf_path = pdf_path
        self._output_dir = output_dir
        self._ocr_fallback = ocr_fallback
        self._max_pages = max_pages
        self._validate_inputs()
    
    def _validate_inputs(self) -> None:
        """Validate inputs."""
        if not Path(self._pdf_path).exists():
            raise FileNotFoundError(f"PDF not found: {self._pdf_path}")
    
    @property
    def pdf_path(self) -> str:
        return self._pdf_path

    def extract_full_content(self) -> List[PageContent]:
        """Extract content from all pages efficiently."""
        doc: Any = fitz.open(self._pdf_path)  # type: ignore
        all_pages: List[PageContent] = []

        with pdfplumber.open(self._pdf_path) as plumber_pdf:
            total_pages = min(len(doc), self._max_pages or len(doc))  # type: ignore
            
            for i in range(total_pages):
                page_data = self._extract_page_content(doc[i], plumber_pdf, i)
                all_pages.append(page_data)

        doc.close()  # type: ignore
        return all_pages
    
    def _extract_page_content(self, page: Any, plumber_pdf: Any, page_index: int) -> PageContent:
        """Extract content from single page."""
        text = page.get_text("text") or ""
        image_count = len(page.get_images(full=True))
        table_count = self._count_tables(plumber_pdf, page_index)
        
        return PageContent(
            page=page_index + 1,
            text=text,
            image_count=image_count,
            table_count=table_count
        )
    
    def _count_tables(self, plumber_pdf: Any, page_index: int) -> int:
        """Count tables on page."""
        if page_index >= len(plumber_pdf.pages):
            return 0
            
        try:
            tables = plumber_pdf.pages[page_index].extract_tables()
            return len(tables or [])
        except Exception:
            return 0
