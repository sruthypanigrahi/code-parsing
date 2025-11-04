"""Module for extracting Table of Contents from USB PD documents."""

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from src.config.constants import (
    MAX_PAGE_NUMBER,
    MAX_TOC_GROUPS,
    MIN_TITLE_LENGTH,
    MIN_TOC_GROUPS,
)
from src.core.models import TOCEntry


class BaseTOCExtractor(ABC):  # Abstraction
    """Abstract TOC extractor (Abstraction, Encapsulation)."""

    def __init__(self, doc_title: str = "USB PD Specification"):
        self._doc_title = doc_title  # Encapsulation
        # Encapsulation: protected patterns
        self._patterns = [
            r"^([A-Z][^.]*?)\s*\.{3,}\s*(\d+)$",
            r"^(\d+(?:\.\d+)*)\s+([^.]+?)\s*\.{2,}\s*(\d+)$",
            r"^([A-Z][A-Za-z\s&(),-]+)\s+(\d+)$",
        ]

    @abstractmethod  # Abstraction
    def extract_toc(self, source: Path) -> list[TOCEntry]:
        pass

    def _parse_line(self, line: str, counter: int) -> Optional[TOCEntry]:
        """Parse line for TOC entry (Encapsulation)."""
        for pattern in self._patterns:
            match = re.match(pattern, line)
            if match:
                entry = self._process_match(match, counter)
                if entry:
                    return entry
        return None

    def _process_match(
        self, match: re.Match[str], counter: int
    ) -> Optional[TOCEntry]:
        """Process regex match (Encapsulation)."""
        groups = match.groups()
        section_id, title, page_str = self._extract_groups(groups, counter)

        if not section_id:
            return None

        return self._create_toc_entry(section_id, title, page_str)

    def _extract_groups(
        self, groups: tuple[str, ...], counter: int
    ) -> tuple[str, str, str]:
        """Extract section_id, title, page_str from groups (Encapsulation)."""
        if len(groups) == MIN_TOC_GROUPS:
            title, page_str = groups
            return f"S{counter}", title, page_str
        if len(groups) == MAX_TOC_GROUPS:
            section_id, title, page_str = groups
            return section_id, title, page_str
        return "", "", ""

    def _create_toc_entry(
        self, section_id: str, title: str, page_str: str
    ) -> Optional[TOCEntry]:
        """Create TOC entry if valid (Encapsulation)."""
        try:
            page = int(page_str)
        except ValueError:
            return None

        if not self._is_valid_entry(page, title):
            return None

        level = self._calculate_level(section_id)
        return self._build_entry(
            section_id=section_id,
            title=title.strip(),
            page=page,
            level=level,
            parent_id=None,
        )

    def _is_valid_entry(self, page: int, title: str) -> bool:
        """Check if entry is valid (Encapsulation)."""
        page_valid = 1 <= page <= MAX_PAGE_NUMBER
        title_valid = len(title.strip()) >= MIN_TITLE_LENGTH
        return page_valid and title_valid

    def _calculate_level(self, section_id: str) -> int:
        """Calculate hierarchy level (Encapsulation)."""
        return section_id.count(".") + 1 if "." in section_id else 1

    def _build_entry(
        self,
        *,
        section_id: str,
        title: str,
        page: int,
        level: int,
        parent_id: Optional[str],
        full_path: Optional[str] = None,
    ) -> TOCEntry:
        """Construct a TOCEntry instance with shared defaults."""
        resolved_title = title.strip()
        resolved_full_path = full_path.strip() if full_path else resolved_title
        return TOCEntry(
            doc_title=self._doc_title,
            section_id=section_id,
            title=resolved_title,
            full_path=resolved_full_path,
            page=page,
            level=level,
            parent_id=parent_id,
            tags=[],
        )
