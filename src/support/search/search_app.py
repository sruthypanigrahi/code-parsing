"""Search application that integrates search functionality and display."""

from __future__ import annotations

from typing import Any, Callable, Protocol

from .base_search import BaseSearcher
from .search_display import SearchDisplay


class SearchStateProtocol(Protocol):
    """Protocol for search state management."""

    def remember(self, term: str) -> None:
        ...

    def cache(self, term: str, results: list[Any]) -> None:
        ...

    def fetch(self, term: str) -> list[Any] | None:
        ...

    def clear_cache(self) -> None:
        ...

    def clear_history(self) -> None:
        ...

    @property
    def history(self) -> list[str]:
        ...

    @property
    def cache_size(self) -> int:
        ...


class SearchDisplayProtocol(Protocol):
    """Protocol describing a search results presenter."""

    def show(self, matches: list[dict[str, Any]], term: str) -> None:
        ...


class SearchState:
    """Encapsulate search history and cached results."""

    def __init__(self) -> None:
        self._history: list[str] = []
        self._cache: dict[str, list[Any]] = {}

    def remember(self, term: str) -> None:
        """Record a term in the search history."""
        if term not in self._history:
            self._history.append(term)

    def cache(self, term: str, results: list[Any]) -> None:
        """Persist results for a specific term."""
        self._cache[term] = results

    def fetch(self, term: str) -> list[Any] | None:
        """Return cached results if they exist."""
        return self._cache.get(term)

    def clear_cache(self) -> None:
        """Clear all cached results."""
        self._cache.clear()

    def clear_history(self) -> None:
        """Remove all recorded history."""
        self._history.clear()

    @property
    def history(self) -> list[str]:
        """Return a copy of the recorded history."""
        return self._history.copy()

    @property
    def cache_size(self) -> int:
        """Return the number of cached entries."""
        return len(self._cache)


class SearchCoordinator:
    """Coordinate validation, execution, and presentation of searches."""

    def __init__(
        self,
        searcher: BaseSearcher,
        display: SearchDisplayProtocol,
        state: SearchStateProtocol,
    ) -> None:
        """Store collaborators that perform the search and rendering."""
        self._searcher = searcher
        self._display = display
        self._state = state

    def run(self, term: str, use_cache: bool = True) -> None:
        """Execute a search while honouring the chosen caching strategy."""
        validated_term = self._validate_term(term)
        results = (
            self._get_cached_or_search(validated_term)
            if use_cache
            else self._perform_search(validated_term)
        )
        self._display.show(results, validated_term)
        self._state.remember(validated_term)
        if not use_cache:
            self._state.cache(validated_term, results)

    def _perform_search(self, term: str) -> list[Any]:
        """Delegate to the searcher implementation."""
        return self._searcher.search(term)

    def _get_cached_or_search(self, term: str) -> list[Any]:
        """Either return cached results or perform a fresh search."""
        cached = self._state.fetch(term)
        if cached is not None:
            return cached
        results = self._perform_search(term)
        self._state.cache(term, results)
        return results

    @staticmethod
    def _validate_term(term: str) -> str:
        if not term or not term.strip():
            raise ValueError("Search term cannot be empty")
        return term.strip()

    @property
    def searcher(self) -> BaseSearcher:
        return self._searcher


CoordinatorFactory = Callable[
    [BaseSearcher, SearchDisplayProtocol, SearchStateProtocol], SearchCoordinator
]


class SearchApp:
    """Facade over the coordinator/state trio for backwards compatibility."""

    def __init__(
        self,
        searcher: BaseSearcher,
        display: SearchDisplayProtocol | None = None,
        *,
        state: SearchStateProtocol | None = None,
        coordinator_factory: CoordinatorFactory | None = None,
    ) -> None:
        self.__state = state or SearchState()
        self.__display = display or SearchDisplay()
        factory = coordinator_factory or SearchCoordinator
        self.__coordinator = factory(searcher, self.__display, self.__state)

    def __str__(self) -> str:
        return f"SearchApp(searcher={type(self.__coordinator.searcher).__name__})"

    def __len__(self) -> int:
        return len(self.__state.history)

    def __contains__(self, term: str) -> bool:
        return term in self.__state.history

    def __call__(self, term: str) -> None:
        self.run_cached(term)

    def run(self, term: str) -> None:
        """Run the search using cached results whenever available."""
        self.__coordinator.run(term, use_cache=True)

    def run_cached(self, term: str) -> None:
        cached = self.__state.fetch(term)
        if cached is not None:
            self.__coordinator.run(term, use_cache=True)
        else:
            self.run(term)

    def run_fresh(self, term: str) -> None:
        """Force a fresh search, bypassing the cache."""
        self.__coordinator.run(term, use_cache=False)

    @property
    def search_history(self) -> list[str]:
        return self.__state.history

    @property
    def cache_size(self) -> int:
        return self.__state.cache_size

    def clear_cache(self) -> None:
        """Clear cached search results."""
        self.__state.clear_cache()

    def clear_history(self) -> None:
        """Clear recorded search history."""
        self.__state.clear_history()


class FastSearchApp(SearchApp):
    """Fast search application variant."""

    def run(self, term: str) -> None:
        """Always bypass the cache for fastest results."""
        self.run_fresh(term)


class CachedSearchApp(SearchApp):
    """Cached search application variant."""

    def run(self, term: str) -> None:
        """Always leverage caching for repeated searches."""
        super().run(term)
