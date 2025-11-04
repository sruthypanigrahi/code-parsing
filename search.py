"""Search entry point with OOP principles."""

from __future__ import annotations

import logging
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Optional

from src.config.constants import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SEARCH_FILE,
    MAX_TERM_LENGTH,
    MIN_ARGS_COUNT,
)
from src.loggers.logger import get_logger
from src.support.search.jsonl_search import JSONLSearcher
from src.support.search.search_app import SearchApp
from src.support.search.search_display import SearchDisplay
from src.utils.decorators import timing

AppFactory = Callable[[str], SearchApp]
RunnerBuilder = Callable[[], "BaseRunner"]


class BaseRunner(ABC):  # Abstraction
    """Abstract runner that coordinates app execution."""

    def __init__(self) -> None:
        self._app: Optional[SearchApp] = None  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod  # Abstraction
    def create_app(self, file_path: str) -> SearchApp:
        """Build the SearchApp that will execute."""

    @timing
    def run(self, term: str, file_path: str) -> None:  # Template method
        """Run search with sanitized inputs."""
        safe_term = self._sanitize_input(term)
        self._app = self.create_app(file_path)  # Encapsulation
        self._app.run(safe_term)  # Polymorphism

    def _sanitize_input(self, term: str) -> str:  # Encapsulation
        """Sanitize search term to prevent command injection."""
        safe_chars = "".join(c for c in term if c.isalnum() or c in " -_")
        return safe_chars[:MAX_TERM_LENGTH]


class SearchRunner(BaseRunner):  # Inheritance
    """Search runner with injectable collaborators."""

    def __init__(
        self,
        searcher_factory: Callable[[str], JSONLSearcher] | None = None,
        display_factory: Callable[[], SearchDisplay] | None = None,
    ) -> None:
        super().__init__()
        self._searcher_factory = searcher_factory or JSONLSearcher
        self._display_factory = display_factory or SearchDisplay

    def create_app(self, file_path: str) -> SearchApp:  # Polymorphism
        """Create search application."""
        searcher = self._searcher_factory(file_path)
        display = self._display_factory()
        return SearchApp(searcher, display)


class RunnerFactory:
    """Registry-backed factory for runner instances."""

    _BUILDERS: dict[str, RunnerBuilder] = {}

    @classmethod
    def register(cls, runner_type: str, builder: RunnerBuilder) -> None:
        """Register a runner builder."""
        cls._BUILDERS[runner_type.lower()] = builder

    @classmethod
    def create_runner(cls, runner_type: str = "search") -> BaseRunner:
        """Create runner instance."""
        key = runner_type.lower()
        try:
            builder = cls._BUILDERS[key]
        except KeyError as exc:
            available = ", ".join(sorted(cls._BUILDERS))
            raise ValueError(
                f"Invalid runner type: {runner_type}. Available: {available}"
            ) from exc
        return builder()


# Register default runner
RunnerFactory.register("search", SearchRunner)


@timing
def main() -> None:
    """Main entry point using OOP principles."""
    logger = get_logger(__name__, Path(DEFAULT_OUTPUT_DIR))

    if len(sys.argv) < MIN_ARGS_COUNT:
        logger.error("Usage: python search.py <search_term> [jsonl_file]")
        sys.exit(1)

    term = sys.argv[1]
    file_path = sys.argv[2] if len(sys.argv) > MIN_ARGS_COUNT else DEFAULT_SEARCH_FILE

    try:
        runner = RunnerFactory.create_runner("search")  # Polymorphism
        runner.run(term, file_path)  # Polymorphism
    except Exception as e:
        logger.error(f"Search failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
