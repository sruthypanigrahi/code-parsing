"""PDFParser class for text extraction and data structuring."""

from pathlib import Path
from typing import Dict, List
import fitz


class PDFParser:
    """Extracts text, structures data."""
    
    def __init__(self, cfg: Dict):
        self.cfg = cfg
    
    def parse_file(self, path: str) -> Dict:
        """Parse PDF file and return structured data."""
        text = self._extract_text(path)
        return self._structure(text, path)
    
    def _extract_text(self, path: str) -> str:
        """Extract text from PDF file."""
        doc = fitz.open(path)
        text = ""
        max_pages = self.cfg.get("max_pages", None)
        
        for page_num in range(min(len(doc), max_pages or len(doc))):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        return text
    
    def _structure(self, text: str, path: str) -> Dict:
        """Structure extracted text into organized data."""
        lines = text.split('\n')
        
        return {
            "source_file": Path(path).name,
            "total_lines": len(lines),
            "content": text,
            "paragraphs": self._extract_paragraphs(lines),
            "toc": self._extract_toc(lines)
        }
    
    def _extract_paragraphs(self, lines: List[str]) -> List[str]:
        """Extract paragraphs from text lines."""
        paragraphs = []
        current_para = ""
        
        for line in lines:
            line = line.strip()
            if line:
                current_para += line + " "
            elif current_para:
                paragraphs.append(current_para.strip())
                current_para = ""
        
        if current_para:
            paragraphs.append(current_para.strip())
        
        return paragraphs
    
    def _extract_toc(self, lines: List[str]) -> List[Dict]:
        """Extract table of contents entries."""
        toc_entries = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            # Simple TOC detection
            if len(line) > 10 and line.count('.') >= 2:
                toc_entries.append({
                    "title": line,
                    "line_number": i + 1
                })
        
        return toc_entries