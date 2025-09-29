"""Search content module with OOP principles."""

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class BaseSearcher(ABC):  # Abstraction
    """Abstract searcher (Abstraction, Encapsulation)."""
    
    def __init__(self, file_path: str):
        self._file_path = Path(file_path)  # Encapsulation
        self._matches: List[Dict[str, Any]] = []  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod  # Abstraction
    def search(self, term: str) -> List[Dict[str, Any]]:
        pass
    
    def _validate_file(self) -> None:  # Encapsulation
        if not self._file_path.exists():
            raise FileNotFoundError(f"File not found: {self._file_path}")


class JSONLSearcher(BaseSearcher):  # Inheritance
    """JSONL searcher (Inheritance, Polymorphism)."""
    
    def search(self, term: str) -> List[Dict[str, Any]]:  # Polymorphism
        self._validate_file()
        self._matches = []
        with open(self._file_path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                self._process_line(line, line_num, term)
        return self._matches
    
    def _process_line(self, line: str, line_num: int, term: str) -> None:
        """Process single line for matches (Encapsulation)."""
        try:
            item: Dict[str, Any] = json.loads(line)
            content: str = item.get("content", "")
            if term.lower() in content.lower():
                self._matches.append({
                    "line": line_num, "page": item.get("page", "N/A"), 
                    "type": item.get("type", "N/A"), 
                    "content": self._truncate(content)
                })
        except json.JSONDecodeError:
            pass
    
    def _truncate(self, content: str, max_len: int = 100) -> str:
        """Truncate content to specified length (Encapsulation)."""
        return content[:max_len] + "..." if len(content) > max_len else content


class SearchDisplay:  # Encapsulation
    """Display handler (Encapsulation, Abstraction)."""
    
    def __init__(self, max_results: int = 10):
        self._max_results = max_results  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def show(self, matches: List[Dict[str, Any]], term: str) -> None:
        """Display search results (Abstraction)."""
        self._logger.info(f"Found {len(matches)} matches for '{term}':")
        for match in matches[:self._max_results]:
            self._print_match(match)
        if len(matches) > self._max_results:
            self._logger.info(f"... and {len(matches) - self._max_results} more matches")
    
    def _print_match(self, match: Dict[str, Any]) -> None:  # Encapsulation
        try:
            self._logger.info(f"Page {match['page']} ({match['type']}): {match['content']}")
        except UnicodeEncodeError:
            self._logger.info(f"Page {match['page']} ({match['type']}): [Special characters]")


class SearchApp:  # Abstraction
    """Search application (Abstraction, Encapsulation)."""
    
    def __init__(self, searcher: BaseSearcher, display: SearchDisplay):
        self._searcher = searcher  # Encapsulation
        self._display = display  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def run(self, term: str) -> None:  # Polymorphism
        try:
            matches = self._searcher.search(term)  # Polymorphism
            self._display.show(matches, term)
        except FileNotFoundError as e:
            self._logger.error(f"Error: {e}")