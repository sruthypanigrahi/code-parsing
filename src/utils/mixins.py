"""Reusable mixin helpers for shared behaviours."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class StatsMixin:
    """Provide common statistics bookkeeping helpers."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._stats: dict[str, int] = {}

    @property
    def stats(self) -> dict[str, int]:
        """Return a defensive copy of current statistics."""
        return self._stats.copy()

    def _update_stat(self, key: str, delta: int = 1) -> None:
        """Increment a statistic value."""
        self._stats[key] = self._stats.get(key, 0) + delta

    def _set_stat(self, key: str, value: int) -> None:
        """Set a statistic value explicitly."""
        self._stats[key] = value

    def reset_stats(self) -> None:
        """Reset all recorded statistics."""
        self._stats.clear()


class OutputDirMixin:
    """Provide consistent handling of output directories."""

    def __init__(self, output_dir: Path, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._output_dir = output_dir
        self._prepare_output_dir()

    @property
    def output_dir(self) -> Path:
        """Get the configured output directory."""
        return self._output_dir

    def _prepare_output_dir(self) -> None:
        """Ensure the output directory exists."""
        try:
            self._output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise RuntimeError(
                f"Cannot create directory {self._output_dir}: {exc}"
            ) from exc


class OutputPathMixin:
    """Shared validation logic for classes that write to file paths."""

    def __init__(self, output_path: Path, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._output_path = self._prepare_output_path(output_path)

    @property
    def output_path(self) -> Path:
        """Return the resolved output path."""
        return self._output_path

    @property
    def output_directory(self) -> Path:
        """Return the directory that contains the output path."""
        return self._output_path.parent

    def _prepare_output_path(self, path: Path) -> Path:
        """Validate and create the parent directory if needed."""
        safe_path = path.resolve()
        try:
            safe_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise RuntimeError(
                f"Cannot create directory {safe_path.parent}: {exc}"
            ) from exc
        return safe_path


class ExtractionTrackerMixin:
    """Track extraction successes and failures for extractor classes."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._extraction_count: int = 0
        self._error_count: int = 0

    @property
    def extraction_count(self) -> int:
        """Number of successful extraction attempts."""
        return self._extraction_count

    @property
    def error_count(self) -> int:
        """Number of extraction errors."""
        return self._error_count

    def _record_extraction(self) -> None:
        """Record a successful extraction."""
        self._extraction_count += 1

    def _record_error(self) -> None:
        """Record an extraction error."""
        self._error_count += 1
