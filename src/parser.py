import re
from typing import List, Tuple, Optional, Match
from .models import TOCEntry

TOC_PATTERNS = [
    re.compile(r"^\s*(\d+(?:\.\d+)*)\s+(.+?)\s{2,}(\d{1,4})\s*$"),
    re.compile(r"^\s*(\d+(?:\.\d+)*)\s+(.+?)\s+\.{2,}\s*(\d{1,4})\s*$"),
    re.compile(r"^\s*(\d+(?:\.\d+)*)\s+(.+?)\s+(\d{1,4})\s*$")
]


class TOCParser:
    """Parses Table of Contents from PDF text using multiple pattern strategies.
    
    This class implements intelligent TOC parsing with multiple regex patterns
    to handle different formatting styles commonly found in technical specifications.
    
    Attributes:
        doc_title (str): Title of the document being parsed.
        
    Example:
        >>> parser = TOCParser("USB PD Specification")
        >>> entries = parser.parse_toc([(1, "1.1 Introduction  15")])
        >>> print(f"Found {len(entries)} TOC entries")
    """

    def __init__(self, doc_title: str = "USB Power Delivery Specification"):
        """Initialize TOC parser with document title.
        
        Args:
            doc_title (str, optional): Title of the document. 
                Defaults to "USB Power Delivery Specification".
        """
        self._doc_title = doc_title
        self._patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> List[re.Pattern[str]]:
        """Get compiled regex patterns for TOC parsing.
        
        Returns:
            List[re.Pattern[str]]: List of compiled regex patterns for different TOC formats.
        """
        return TOC_PATTERNS
    
    @property
    def doc_title(self) -> str:
        """Get the document title.
        
        Returns:
            str: Document title used for TOC entries.
        """
        return self._doc_title

    def parse_toc(self, pages: List[Tuple[int, str]]) -> List[TOCEntry]:
        """Parse Table of Contents from page text data.
        
        Processes multiple pages of text to extract TOC entries using pattern matching.
        Automatically deduplicates entries and infers hierarchical relationships.
        
        Args:
            pages (List[Tuple[int, str]]): List of (page_number, text_content) tuples.
            
        Returns:
            List[TOCEntry]: Parsed and deduplicated TOC entries with inferred hierarchy.
            
        Example:
            >>> parser = TOCParser()
            >>> pages = [(1, "1.1 Introduction  15\n1.2 Overview  20")]
            >>> entries = parser.parse_toc(pages)
            >>> print(f"Parsed {len(entries)} entries")
        """
        entries: List[TOCEntry] = []
        
        for _, text in pages:
            page_entries = self._parse_page_text(text)
            entries.extend(page_entries)
            
        return self._deduplicate_entries(entries)
    
    def _parse_page_text(self, text: str) -> List[TOCEntry]:
        """Parse entries from page text."""
        entries: List[TOCEntry] = []
        
        for line in text.splitlines():
            line = line.strip()
            if self._is_valid_line(line):
                entry = self._parse_line(line)
                if entry:
                    entries.append(entry)
                    
        return entries
    
    def _is_valid_line(self, line: str) -> bool:
        """Check if line is valid."""
        return bool(line and len(line) >= 5)
    
    def _parse_line(self, line: str) -> Optional[TOCEntry]:
        """Parse single line."""
        for pattern in self._patterns:
            match = pattern.match(line)
            if match:
                return self._create_entry_from_match(match)
        return None
    
    def _create_entry_from_match(self, match: Match[str]) -> Optional[TOCEntry]:
        """Create entry from match."""
        try:
            section_id, title, page_str = match.groups()
            page_num = int(page_str)
            
            return TOCEntry(
                doc_title=self._doc_title,
                section_id=section_id,
                title=title.strip(),
                page=page_num,
                level=1,
                full_path=f"{section_id} {title.strip()}"
            )
        except (ValueError, AttributeError):
            return None
    
    def _deduplicate_entries(self, entries: List[TOCEntry]) -> List[TOCEntry]:
        """Remove duplicates."""
        seen: set[tuple[str, int]] = set()
        unique_entries: List[TOCEntry] = []
        
        for entry in entries:
            key = (entry.section_id, entry.page)
            if key not in seen:
                seen.add(key)
                unique_entries.append(entry)
                
        return unique_entries
