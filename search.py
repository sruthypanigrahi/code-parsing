#!/usr/bin/env python3
"""Search entry point with OOP principles."""

import logging
import sys
from abc import ABC, abstractmethod
from src.search_content import JSONLSearcher, SearchDisplay, SearchApp


class BaseRunner(ABC):  # Abstraction
    """Abstract runner (Abstraction, Encapsulation)."""
    
    def __init__(self):
        self._app = None  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod  # Abstraction
    def create_app(self, file_path: str) -> SearchApp:
        pass
    
    def run(self, term: str, file_path: str) -> None:  # Template method
        self._app = self.create_app(file_path)  # Encapsulation
        self._app.run(term)  # Polymorphism


class SearchRunner(BaseRunner):  # Inheritance
    """Search runner (Inheritance, Polymorphism)."""
    
    def create_app(self, file_path: str) -> SearchApp:  # Polymorphism
        searcher = JSONLSearcher(file_path)  # Factory pattern
        display = SearchDisplay()
        return SearchApp(searcher, display)


class RunnerFactory:  # Abstraction
    """Runner factory (Abstraction, Encapsulation)."""
    
    @staticmethod  # Encapsulation
    def create_runner(runner_type: str = "search") -> BaseRunner:
        if runner_type == "search":
            return SearchRunner()  # Polymorphism
        else:
            return SearchRunner()  # Default


def main():
    """Main entry point using OOP principles."""
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) < 2:
        logger.error("Usage: python search.py <search_term> [jsonl_file]")
        sys.exit(1)
    
    term = sys.argv[1]
    file_path = sys.argv[2] if len(sys.argv) > 2 else "outputs/usb_pd_spec.jsonl"
    
    # Factory pattern (Abstraction)
    runner = RunnerFactory.create_runner("search")  # Polymorphism
    runner.run(term, file_path)  # Polymorphism


if __name__ == "__main__":
    main()