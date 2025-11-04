"""PDF extractions with OOP principles."""

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Optional

try:
    import fitz
except ImportError as e:
    msg = "PyMuPDF required. Install: pip install PyMuPDF==1.24.9"
    raise ImportError(msg) from e


from src.config.constants import DEFAULT_DOC_TITLE
from src.core.extractors.pdfextractor.base_extractor import BaseExtractor
from src.utils.mixins import ExtractionTrackerMixin


class PDFNotFoundError(Exception):
    """PDF file not found error."""


class AssetScopedExtractor(ExtractionTrackerMixin, BaseExtractor):
    """Base extractor scoped to project asset directory."""

    def __init__(self, pdf_path: Path):
        safe_path = self._validate_assets_path(pdf_path)
        super().__init__(safe_path)

    def _validate_assets_path(self, path: Path) -> Path:
        """Ensure PDF resides within assets directory."""
        if not path.exists():
            raise PDFNotFoundError(f"PDF not found: {path}")
        safe_path = path.resolve()
        assets_dir = Path.cwd().resolve() / "assets"
        try:
            safe_path.relative_to(assets_dir)
        except ValueError as exc:
            msg = f"Path outside assets: {path}"
            raise PDFNotFoundError(msg) from exc
        return safe_path


class FrontPageExtractor(AssetScopedExtractor):
    """Front page extractor."""

    def extract(self) -> list[str]:
        """Extract content from PDF."""
        return list(self.extract_pages())

    def extract_pages(self, max_pages: Optional[int] = 10) -> Iterator[str]:
        """Extract pages from PDF."""
        doc = None
        try:
            doc = fitz.open(str(self.pdf_path))
            if doc is not None:
                total_pages = self._get_total_pages(doc, max_pages)
                yield from self._extract_page_texts(doc, total_pages)

        except (fitz.FileDataError, fitz.FileNotFoundError, OSError) as e:
            self._record_error()
            self.logger.error("Cannot open PDF file: %s", e)
        finally:
            if doc:
                doc.close()

    def _get_total_pages(self, doc: fitz.Document, max_pages: Optional[int]) -> int:
        """Calculate total pages to process."""
        doc_len = len(doc)
        return doc_len if max_pages is None else min(max_pages, doc_len)

    def _extract_page_texts(self, doc: fitz.Document, total_pages: int) -> Iterator[str]:
        """Extract text from pages."""
        for i in range(total_pages):
            try:
                self._record_extraction()
                yield str(doc[i].get_text("text") or "")
            except (fitz.FileDataError, fitz.FileNotFoundError) as e:
                self._record_error()
                self.logger.warning("PDF error on page %s: %s", i, e)
                yield ""


class TitleExtractor(AssetScopedExtractor):
    """Title extractor."""

    def extract(self) -> list[str]:
        """Extract content from PDF."""
        return [self.get_title()]

    def get_title(self) -> str:
        """Get PDF title from metadata."""
        try:
            with fitz.open(str(self.pdf_path)) as doc:
                self._record_extraction()
                metadata = doc.metadata
                title = metadata.get("title") if metadata else None
                if isinstance(title, str):
                    return title
                return DEFAULT_DOC_TITLE
        except (fitz.FileDataError, fitz.FileNotFoundError, OSError) as e:
            self._record_error()
            self.logger.warning("Cannot read PDF metadata: %s", e)
            return DEFAULT_DOC_TITLE


def extract_front_pages(pdf_path: Path, max_pages: Optional[int] = 10) -> Iterator[str]:
    """Extract front pages from PDF."""
    return FrontPageExtractor(pdf_path).extract_pages(max_pages)


def get_doc_title(pdf_path: Path) -> str:
    """Get document title from PDF."""
    try:
        return TitleExtractor(pdf_path).get_title()
    except (PDFNotFoundError, OSError, ValueError) as e:
        logging.getLogger(__name__).error("Cannot extract title: %s", e)
        return DEFAULT_DOC_TITLE
