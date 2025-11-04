"""Search application that integrates search functionality and display."""

from typing import Any

from .base_search import BaseSearcher
from .search_display import SearchDisplay


class SearchState:
    """Encapsulate search history and cached results."""

    def __init__(self) -> None:
        self._history: list[str] = []
        self._cache: dict[str, list[Any]] = {}

    def remember(self, term: str) -> None:
        """Store a search term in history."""
        if term not in self._history:
            self._history.append(term)

    def cache(self, term: str, results: list[Any]) -> None:
        """Persist results for a term."""
        self._cache[term] = results

    def fetch(self, term: str) -> list[Any] | None:
        """Retrieve cached results if available."""
        return self._cache.get(term)

    def clear_cache(self) -> None:
        """Drop cached search results."""
        self._cache.clear()

    def clear_history(self) -> None:
        """Drop recorded search history."""
        self._history.clear()

    @property
    def history(self) -> list[str]:
        """Read-only access to history."""
        return self._history.copy()

    @property
    def cache_size(self) -> int:
        """Current cache size."""
        return len(self._cache)


class SearchCoordinator:
    """Coordinate validation, execution, and presentation of searches."""

    def __init__(
        self,
        searcher: BaseSearcher,
        display: SearchDisplay,
        state: SearchState,
    ) -> None:
        self._searcher = searcher
        self._display = display
        self._state = state

    def run(self, term: str, use_cache: bool = True) -> None:
        """Execute a search, optionally consulting the cache."""
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
        """Delegate to the injected searcher."""
        return self._searcher.search(term)

    def _get_cached_or_search(self, term: str) -> list[Any]:
        """Return cached results when present."""
        cached = self._state.fetch(term)
        if cached is not None:
            return cached
        results = self._perform_search(term)
        self._state.cache(term, results)
        return results

    @staticmethod
    def _validate_term(term: str) -> str:
        """Strip and validate incoming search terms."""
        if not term or not term.strip():
            raise ValueError("Search term cannot be empty")
        return term.strip()

    @property
    def searcher(self) -> BaseSearcher:
        """Expose the composed searcher for introspection."""
        return self._searcher


class SearchApp:  # Composition
    """Facade over the coordinator/state trio for backwards compatibility."""

    def __init__(self, searcher: BaseSearcher, display: SearchDisplay):
        self.__state = SearchState()
        self.__coordinator = SearchCoordinator(searcher, display, self.__state)

    def __str__(self) -> str:  # Magic Method
        return f"SearchApp(searcher={type(self.__coordinator.searcher).__name__})"

    def __len__(self) -> int:  # Magic Method
        """Return number of searches performed."""
        return len(self.__state.history)

    def __contains__(self, term: str) -> bool:  # Magic Method
        """Check if term was searched before."""
        return term in self.__state.history

    def __call__(self, term: str) -> None:  # Magic Method
        self.run_cached(term)

    def run(self, term: str) -> None:  # Polymorphism
        self.__coordinator.run(term, use_cache=True)

    def run_cached(self, term: str) -> None:  # Polymorphism
        """Run search with caching enabled."""
        cached = self.__state.fetch(term)
        if cached is not None:
            self.__coordinator.run(term, use_cache=True)
        else:
            self.run(term)

    def run_fresh(self, term: str) -> None:  # Polymorphism
        """Run search without using cache."""
        self.__coordinator.run(term, use_cache=False)

    @property
    def search_history(self) -> list[str]:
        """Get search history (read-only)."""
        return self.__state.history

    @property
    def cache_size(self) -> int:
        """Get current cache size."""
        return self.__state.cache_size

    def clear_cache(self) -> None:
        """Clear search result cache."""
        self.__state.clear_cache()

    def clear_history(self) -> None:
        """Clear search history."""
        self.__state.clear_history()


class FastSearchApp(SearchApp):  # Inheritance + Polymorphism
    """Fast search application variant."""

    def run(self, term: str) -> None:  # Method override
        """Fast search execution."""
        self.run_fresh(term)  # Skip cache for speed


class CachedSearchApp(SearchApp):  # Inheritance + Polymorphism
    """Cached search application variant."""

    def run(self, term: str) -> None:  # Method override
        """Cached search execution."""
        super().run(term)  # Always use cache
