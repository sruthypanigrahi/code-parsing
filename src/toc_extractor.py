"""Table of Contents extraction class."""

import re
from typing import List, Iterator
from .models import TOCEntry


class TOCExtractor:
    """Handles TOC extraction from PDF content."""
    
    def __init__(self, doc_title: str):
        self.doc_title = doc_title
        self.patterns = [
            # Pattern for "Section Title ... Page"
            r'^([A-Z][^.]*?)\s*\.{3,}\s*(\d+)$',
            # Pattern for numbered sections
            r'^(\d+(?:\.\d+)*)\s+([^.]+?)\s*\.{2,}\s*(\d+)$',
            # Pattern for simple "Title Page"
            r'^([A-Z][A-Za-z\s]+)\s+(\d+)$'
        ]
    
    def extract_from_content(self, content: str) -> List[TOCEntry]:
        """Extract TOC entries from text content."""
        entries = []
        lines = content.split('\n')
        section_counter = 1
        
        # Look for TOC section patterns
        in_toc_section = False
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 5:
                continue
            
            # Detect TOC section start
            if 'table of contents' in line.lower() or 'contents' in line.lower():
                in_toc_section = True
                continue
            
            # Skip if not in TOC section and no clear TOC patterns
            if not in_toc_section and not any(pattern in line for pattern in ['...', '  ']):
                continue
            
            entry = self._parse_toc_line(line, section_counter)
            if entry:
                entries.append(entry)
                section_counter += 1
        
        return entries
    
    def _parse_toc_line(self, line: str, section_counter: int) -> TOCEntry:
        """Parse a single TOC line into a TOCEntry."""
        # Enhanced patterns for USB PD spec
        enhanced_patterns = [
            r'^([A-Z][^.]*?)\s*\.{3,}\s*(\d+)$',  # Title ... Page
            r'^(\d+(?:\.\d+)*)\s+([^.]+?)\s*\.{2,}\s*(\d+)$',  # Section Title ... Page
            r'^([A-Z][A-Za-z\s&(),-]+)\s+(\d+)$',  # Title Page (no dots)
            r'^([A-Z][^\d]*?)\s*(\d+)$'  # Simple Title Page
        ]
        
        for pattern in enhanced_patterns:
            match = re.match(pattern, line)
            if match:
                groups = match.groups()
                
                if len(groups) == 2:  # Title and page
                    title, page_str = groups
                    section_id = f"S{section_counter}"
                elif len(groups) == 3:  # Section, title, page
                    section_id, title, page_str = groups
                else:
                    continue
                
                try:
                    page = int(page_str)
                    # Filter out invalid entries
                    if page < 1 or page > 2000 or len(title.strip()) < 3:
                        continue
                        
                    return TOCEntry(
                        doc_title=self.doc_title,
                        section_id=section_id,
                        title=title.strip(),
                        full_path=title.strip(),
                        page=page,
                        level=self._determine_level(section_id),
                        parent_id=None,
                        tags=[]
                    )
                except ValueError:
                    continue
        
        return None
    
    def _determine_level(self, section_id: str) -> int:
        """Determine hierarchy level from section ID."""
        if section_id.startswith('S'):
            return 1
        
        dots = section_id.count('.')
        return dots + 1
    
    def _get_existing_entries(self) -> List:
        """Get existing entries count (placeholder)."""
        return []