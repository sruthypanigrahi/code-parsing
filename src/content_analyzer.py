"""Content analysis with OOP principles."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Iterator


class BaseAnalyzer(ABC):  # Abstraction
    """Abstract content analyzer."""
    
    @abstractmethod
    def analyze(self, text: str) -> str:
        pass


class ContentClassifier(BaseAnalyzer):  # Inheritance
    """Fast content classification (Polymorphism)."""
    
    def __init__(self):
        self._patterns = {  # Encapsulation
            "requirement": ["shall", "must", "required"],
            "recommendation": ["may", "should", "recommended"],
            "note": ["note:", "warning:", "caution:"],
            "heading": ["table", "figure", "section"],
            "technical": ["protocol", "message", "packet"],
            "procedure": ["step", "procedure", "algorithm"]
        }
    
    def analyze(self, text: str) -> str:  # Polymorphism
        text_lower = text.lower().strip()
        
        for content_type, keywords in self._patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return content_type
        
        return "paragraph"


class StructuredExtractor(BaseAnalyzer):  # Inheritance
    """Extract structured content patterns."""
    
    def analyze(self, text: str) -> str:  # Polymorphism
        text = text.strip()
        
        if text.startswith(('1.', '2.', '3.', '4.', '5.')):
            return "numbered_item"
        elif text.startswith(('•', '-', 'a)', 'b)')):
            return "bullet_point"
        elif ':' in text and len(text.split(':')[0]) < 50:
            return "definition"
        elif '|' in text or text.count('\t') >= 2:
            return "table_data"
        
        return "text"


class ContentAnalyzer:  # Composition
    """Main analyzer using multiple strategies."""
    
    def __init__(self):
        self._classifier = ContentClassifier()  # Encapsulation
        self._extractor = StructuredExtractor()
    
    def classify_content(self, text: str) -> str:
        """Fast content classification."""
        # Try structured patterns first (faster)
        struct_type = self._extractor.analyze(text)
        if struct_type != "text":
            return struct_type
        
        # Fall back to semantic classification
        return self._classifier.analyze(text)
    
    def extract_structured_items(self, full_text: str, 
                               page_num: int) -> Iterator[Dict[str, Any]]:
        """Extract only high-value structured content."""
        lines = full_text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if len(line) < 10:  # Skip short lines
                continue
                
            content_type = self.classify_content(line)
            if content_type in ["numbered_item", "bullet_point", "definition"]:
                yield {
                    "type": content_type,
                    "content": line,
                    "page": page_num + 1,
                    "block_id": f"{content_type[0]}{page_num + 1}_{i}",
                    "bbox": []
                }