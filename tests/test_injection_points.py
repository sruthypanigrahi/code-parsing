"""Tests covering dependency injection points introduced for OOP design."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from src.core.orchestrator.pipeline_coordinator import PipelineCoordinator
from src.support.search.search_app import (
    CoordinatorFactory,
    SearchApp,
    SearchDisplayProtocol,
    SearchStateProtocol,
)


class DummyExtractor:
    """Test double that mimics the DataExtractor interface."""

    def __init__(self, *_: Any, **__: Any) -> None:
        self.extract_data_called = False
        self.toc_only_called = False
        self.content_only_called = False

    def extract_data(self, max_pages: int | None) -> tuple[list[str], list[str]]:
        self.extract_data_called = True
        assert max_pages is None
        return (["toc-entry"], ["content-block"])

    def extract_toc_only(self) -> list[str]:
        self.toc_only_called = True
        return ["toc-only"]

    def extract_content_only(self) -> int:
        self.content_only_called = True
        return 7


class DummyFileManager:
    """Test double that records written artefacts."""

    def __init__(self, *_: Any, **__: Any) -> None:
        self.written: tuple[list[Any], list[Any]] | None = None

    def write_files(self, toc: list[Any], content: list[Any]) -> None:
        self.written = (toc, content)


class DummyReportManager:
    """Test double that records report generation calls."""

    def __init__(self, *_: Any, **__: Any) -> None:
        self.generated_with: tuple[list[Any], list[Any]] | None = None

    def generate_reports(self, toc: list[Any], content: list[Any]) -> dict[str, Any]:
        self.generated_with = (toc, content)
        return {"content_items": len(content)}


def test_pipeline_coordinator_uses_injected_factories() -> None:
    extractor_instances: list[DummyExtractor] = []
    file_manager_instances: list[DummyFileManager] = []
    report_manager_instances: list[DummyReportManager] = []

    def extractor_factory(*args: Any) -> DummyExtractor:
        extractor = DummyExtractor(*args)
        extractor_instances.append(extractor)
        return extractor

    def file_manager_factory(*args: Any) -> DummyFileManager:
        manager = DummyFileManager(*args)
        file_manager_instances.append(manager)
        return manager

    def report_manager_factory(*args: Any) -> DummyReportManager:
        manager = DummyReportManager(*args)
        report_manager_instances.append(manager)
        return manager

    config_path = Path("application.yml")
    pipeline = PipelineCoordinator(
        str(config_path),
        data_extractor_factory=extractor_factory,
        file_manager_factory=file_manager_factory,
        report_manager_factory=report_manager_factory,
    )

    result = pipeline.run()

    extractor = extractor_instances[0]
    file_manager = file_manager_instances[0]
    report_manager = report_manager_instances[0]

    assert extractor.extract_data_called
    assert file_manager.written == (["toc-entry"], ["content-block"])
    assert report_manager.generated_with == (["toc-entry"], ["content-block"])
    assert result == {"toc_entries": 1, "spec_counts": {"content_items": 1}}

    pipeline.run_toc_only()
    pipeline.run_content_only()
    assert extractor.toc_only_called
    assert extractor.content_only_called


class StubSearcher:
    """Simple searcher used purely for tests."""

    def search(self, term: str) -> list[dict[str, Any]]:
        return [{"page": 1, "type": "stub", "content": term}]


class StubState(SearchStateProtocol):
    """In-memory implementation of the search state protocol for tests."""

    def __init__(self) -> None:
        self._history: list[str] = []
        self._cache: dict[str, list[Any]] = {}

    def remember(self, term: str) -> None:
        self._history.append(term)

    def cache(self, term: str, results: list[Any]) -> None:
        self._cache[term] = results

    def fetch(self, term: str) -> list[Any] | None:
        return self._cache.get(term)

    def clear_cache(self) -> None:
        self._cache.clear()

    def clear_history(self) -> None:
        self._history.clear()

    @property
    def history(self) -> list[str]:
        return list(self._history)

    @property
    def cache_size(self) -> int:
        return len(self._cache)


class StubDisplay(SearchDisplayProtocol):
    """Presenter capturing invocations for assertions."""

    def __init__(self) -> None:
        self.presented_terms: list[str] = []
        self.presented_matches: list[list[dict[str, Any]]] = []

    def show(self, matches: list[dict[str, Any]], term: str) -> None:
        self.presented_terms.append(term)
        self.presented_matches.append(matches)


def test_search_app_uses_injected_state_and_display() -> None:
    state = StubState()
    display = StubDisplay()
    searcher = StubSearcher()

    app = SearchApp(searcher, display=display, state=state)

    term = "USB PD"
    app.run(term)

    assert state.history == [term]
    assert display.presented_terms == [term]
    assert display.presented_matches[0][0]["content"] == term
