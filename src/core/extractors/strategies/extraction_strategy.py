"""Extraction strategies with polymorphism."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, ClassVar

# Constants
DOC_TITLE = "USB PD Specification"


class ExtractionStrategy(ABC):
    """Abstract extraction strategy."""

    strategy_name: ClassVar[str] = "base"

    @abstractmethod
    def extract_pages(
        self, pdf_path: Path, max_pages: int | None
    ) -> Iterator[dict[str, Any]]:
        """Extract content using specific strategy."""

    def get_strategy_name(self) -> str:
        """Return the identifier for this strategy."""
        return self.strategy_name

    def __call__(
        self, pdf_path: Path, max_pages: int | None = None
    ) -> Iterator[dict[str, Any]]:
        """Make strategy callable."""
        return self.extract_pages(pdf_path, max_pages)

    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}()"

    @staticmethod
    def _combine_block_text(block: dict[str, Any]) -> str:
        """Flatten block spans into a single text string."""
        return "".join(
            str(span["text"])
            for line in block.get("lines", [])
            for span in line.get("spans", [])
        )


class _FitzBackedStrategy(ExtractionStrategy):
    """Helper mixin that manages the fitz document lifecycle."""

    @contextmanager
    def _open_document(self, pdf_path: Path) -> Iterator[Any]:
        import fitz

        doc = fitz.open(str(pdf_path))
        try:
            yield doc
        finally:
            doc.close()

    def _iter_pages(
        self, pdf_path: Path, max_pages: int | None
    ) -> Iterator[tuple[int, Any]]:
        with self._open_document(pdf_path) as doc:
            doc_len = len(doc)
            total_pages = doc_len if max_pages is None else min(max_pages, doc_len)
            for page_num in range(total_pages):
                yield page_num, doc[page_num]


class ComprehensiveStrategy(_FitzBackedStrategy):
    """Strategy for maximum page coverage."""

    strategy_name: ClassVar[str] = "comprehensive"

    def extract_pages(
        self, pdf_path: Path, max_pages: int | None
    ) -> Iterator[dict[str, Any]]:
        """Extract all pages with comprehensive coverage."""
        for page_num, page in self._iter_pages(pdf_path, None):
            blocks = page.get_text("dict")["blocks"]
            for block_num, block in enumerate(blocks):
                if "lines" not in block:
                    continue
                text = self._combine_block_text(block)
                if not text.strip():
                    continue
                yield {
                    "doc_title": DOC_TITLE,
                    "section_id": f"p{page_num + 1}_{block_num}",
                    "title": text[:50],
                    "content": text.strip(),
                    "page": page_num + 1,
                    "level": 1,
                    "parent_id": None,
                    "full_path": text[:50],
                    "type": "paragraph",
                    "block_id": f"p{page_num + 1}_{block_num}",
                    "bbox": list(block.get("bbox", [])),
                }


class StandardStrategy(ExtractionStrategy):
    """Standard extraction strategy."""

    strategy_name: ClassVar[str] = "standard"

    def extract_pages(
        self, pdf_path: Path, max_pages: int | None
    ) -> Iterator[dict[str, Any]]:
        """Extract pages using standard PDF extractor."""
        from src.core.extractors.pdfextractor.pdf_extractor import PDFExtractor

        extractor = PDFExtractor(pdf_path)
        yield from extractor.extract_content(max_pages)


class FastStrategy(_FitzBackedStrategy):
    """Fast extraction strategy with minimal processing."""

    strategy_name: ClassVar[str] = "fast"

    def extract_pages(
        self, pdf_path: Path, max_pages: int | None
    ) -> Iterator[dict[str, Any]]:
        """Fast extraction - text only, no detailed processing."""
        for page_num, page in self._iter_pages(pdf_path, max_pages):
            text = page.get_text()
            if not text.strip():
                continue
            yield {
                "doc_title": DOC_TITLE,
                "section_id": f"fast_{page_num + 1}",
                "title": text[:30],
                "content": text.strip(),
                "page": page_num + 1,
                "level": 1,
                "parent_id": None,
                "full_path": text[:30],
                "type": "text",
                "block_id": f"fast_{page_num + 1}",
                "bbox": [],
            }


class DetailedStrategy(_FitzBackedStrategy):
    """Detailed extraction with enhanced metadata."""

    strategy_name: ClassVar[str] = "detailed"

    def extract_pages(
        self, pdf_path: Path, max_pages: int | None
    ) -> Iterator[dict[str, Any]]:
        """Detailed extraction with font and formatting info."""
        for page_num, page in self._iter_pages(pdf_path, max_pages):
            blocks = page.get_text("dict")["blocks"]
            for block_num, block in enumerate(blocks):
                if "lines" not in block or not block["lines"]:
                    continue
                text = self._combine_block_text(block)
                if not text.strip():
                    continue
                yield {
                    "doc_title": DOC_TITLE,
                    "section_id": f"det_{page_num + 1}_{block_num}",
                    "title": text[:40],
                    "content": text.strip(),
                    "page": page_num + 1,
                    "level": 1,
                    "parent_id": None,
                    "full_path": text[:40],
                    "type": "detailed",
                    "block_id": f"det_{page_num + 1}_{block_num}",
                    "bbox": list(block.get("bbox", [])),
                }


class StrategyFactory:
    """Factory to create extraction strategies."""

    _STRATEGIES: dict[str, type[ExtractionStrategy]] = {
        "comprehensive": ComprehensiveStrategy,
        "standard": StandardStrategy,
        "fast": FastStrategy,
        "detailed": DetailedStrategy,
    }

    @staticmethod
    def create(strategy_type: str) -> ExtractionStrategy:
        """Create strategy - runtime polymorphism."""
        try:
            strategy_cls = StrategyFactory._STRATEGIES[strategy_type]
        except KeyError as exc:
            available = ", ".join(sorted(StrategyFactory._STRATEGIES))
            raise ValueError(
                f"Unknown strategy: {strategy_type}. Available: {available}"
            ) from exc
        return strategy_cls()
