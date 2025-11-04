"""Module for displaying search result with logging and encapsulation."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Any, Optional, Protocol


class SearchResultPresenter(Protocol):
    """Interface for presenting search results."""

    def present(
        self, matches: Sequence[dict[str, Any]], term: str, max_results: int
    ) -> None:
        """Render search matches for the given term."""


class ConsoleSearchPresenter:
    """Default presenter that writes results to stdout."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(self.__class__.__name__)

    def present(
        self, matches: Sequence[dict[str, Any]], term: str, max_results: int
    ) -> None:
        display_count = min(len(matches), max_results)
        total_count = len(matches)
        self._logger.info(
            "Displaying %s of %s matches for '%s'", display_count, total_count, term
        )
        print(f"Found {total_count} matches for '{term}':")
        for match in matches[:max_results]:
            print(self._format_match(match))
        if total_count > max_results:
            remaining = total_count - max_results
            print(f"... and {remaining} more matches")
            self._logger.info(
                "Truncated display: showing %s of %s total matches",
                max_results,
                total_count,
            )

    def _format_match(self, match: dict[str, Any]) -> str:
        page = match.get("page", "N/A")
        match_type = match.get("type", "N/A")
        content = match.get("content", "")
        return f"Page {page} ({match_type}): {content}"


class SearchDisplay:
    """Facade that delegates rendering to a presenter strategy."""

    def __init__(
        self,
        presenter: SearchResultPresenter | None = None,
        max_results: int = 10,
    ):
        self._max_results = max_results
        self._presenter = presenter or ConsoleSearchPresenter()

    def show(self, matches: list[dict[str, Any]], term: str) -> None:
        """Display search results using the configured presenter."""
        self._presenter.present(matches, term, self._max_results)
