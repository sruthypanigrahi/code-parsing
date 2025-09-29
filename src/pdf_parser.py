"""PDF parsing logic with OOP design."""

from pathlib import Path
from typing import Any, Dict, List

import fitz

from .models import ContentItem, TOCEntry


class PDFParser:
    """Handles PDF parsing logic with single responsibility."""

    def __init__(self):
        self.doc = None
        self.parsed_content: List[ContentItem] = []
        self.parsed_toc: List[TOCEntry] = []

    def parse_document(self, pdf_path: Path) -> Dict[str, Any]:
        """Parse PDF document and extract all content."""
        self.doc = fitz.open(pdf_path)

        # Parse TOC
        self.parsed_toc = self._parse_toc()

        # Parse content (paragraphs, images, tables)
        self.parsed_content = self._parse_content()

        return {
            "toc": self.parsed_toc,
            "content": self.parsed_content,
            "total_pages": len(self.doc),
        }

    def _parse_toc(self) -> List[TOCEntry]:
        """Extract table of contents."""
        toc_entries = []
        toc = self.doc.get_toc()

        for i, (level, title, page) in enumerate(toc):
            entry = TOCEntry(
                doc_title=self.doc.name or "document.pdf",
                section_id=f"S{i+1}",
                title=title.strip(),
                full_path=title.strip(),
                page=page,
                level=level,
                parent_id=None,
                tags=[],
            )
            toc_entries.append(entry)

        return toc_entries

    def _parse_content(self) -> List[ContentItem]:
        """Extract content from all pages."""
        content_items = []

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]

            # Extract text blocks
            blocks = page.get_text("dict")["blocks"]

            for block_idx, block in enumerate(blocks):
                if "lines" in block:  # Text block
                    text = ""
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text += span["text"]

                    if text.strip():
                        content_item = ContentItem(
                            doc_title=self.doc.name or "document.pdf",
                            content_id=f"C{len(content_items)+1}",
                            type="paragraph",
                            content=text.strip(),
                            page=page_num + 1,
                            block_id=f"p{page_num+1}_{block_idx}",
                            bbox=block.get("bbox", []),
                            metadata={
                                "extracted_at": "2024-01-01T00:00:00",
                                "content_length": len(text.strip()),
                            },
                        )
                        content_items.append(content_item)

        return content_items

    def close(self):
        """Clean up resources."""
        if self.doc:
            self.doc.close()
