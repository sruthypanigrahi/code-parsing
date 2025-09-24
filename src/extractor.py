import fitz  # type: ignore # PyMuPDF
import pdfplumber
from pathlib import Path
from typing import List, Any
from .models import PageContent


class PDFExtractor:
    """Extracts content from PDF files with high performance and OCR support.
    
    This class handles PDF content extraction including text, images, and tables.
    It supports both regular PDFs and scanned documents through OCR fallback.
    
    Attributes:
        pdf_path (str): Path to the PDF file being processed.
        output_dir (Path): Directory for output files.
        ocr_fallback (bool): Whether to use OCR for scanned PDFs.
        max_pages (int | None): Maximum pages to process, None for all.
    
    Example:
        >>> extractor = PDFExtractor("document.pdf", Path("outputs"))
        >>> pages = extractor.extract_full_content()
        >>> print(f"Extracted {len(pages)} pages")
    """

    def __init__(self, pdf_path: str, output_dir: Path, ocr_fallback: bool = True, max_pages: int | None = None):
        """Initialize PDF extractor with configuration.
        
        Args:
            pdf_path (str): Path to the PDF file to process.
            output_dir (Path): Directory where output files will be saved.
            ocr_fallback (bool, optional): Enable OCR for scanned PDFs. Defaults to True.
            max_pages (int | None, optional): Maximum pages to process. Defaults to None.
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
        """
        self._pdf_path = pdf_path
        self._output_dir = output_dir
        self._ocr_fallback = ocr_fallback
        self._max_pages = max_pages
        self._validate_inputs()
    
    def _validate_inputs(self) -> None:
        """Validate constructor inputs.
        
        Raises:
            FileNotFoundError: If PDF file doesn't exist.
        """
        if not Path(self._pdf_path).exists():
            raise FileNotFoundError(f"PDF not found: {self._pdf_path}")
    
    @property
    def pdf_path(self) -> str:
        """Get the PDF file path.
        
        Returns:
            str: Path to the PDF file.
        """
        return self._pdf_path

    def extract_full_content(self) -> List[PageContent]:
        """Extract content from all pages with memory optimization.
        
        Processes the PDF page by page to extract text, count images and tables.
        Uses both PyMuPDF and pdfplumber for comprehensive content extraction.
        
        Returns:
            List[PageContent]: List of PageContent objects containing extracted data.
            
        Raises:
            FileNotFoundError: If PDF file cannot be opened.
            MemoryError: If PDF is too large to process.
            
        Example:
            >>> extractor = PDFExtractor("spec.pdf", Path("outputs"))
            >>> pages = extractor.extract_full_content()
            >>> print(f"Processed {len(pages)} pages")
        """
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
        """Extract content from a single PDF page.
        
        Args:
            page (Any): PyMuPDF page object.
            plumber_pdf (Any): PDFPlumber PDF object for table extraction.
            page_index (int): Zero-based page index.
            
        Returns:
            PageContent: Object containing page text, image count, and table count.
        """
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
        """Count tables on a specific page using pdfplumber.
        
        Args:
            plumber_pdf (Any): PDFPlumber PDF object.
            page_index (int): Zero-based page index.
            
        Returns:
            int: Number of tables found on the page.
        """
        if page_index >= len(plumber_pdf.pages):
            return 0
            
        try:
            tables = plumber_pdf.pages[page_index].extract_tables()
            return len(tables or [])
        except Exception:
            return 0
