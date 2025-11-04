"""Shared base classes for orchestrator components."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.config.config import Config


class PipelineComponent:
    """Base class that encapsulates shared orchestrator dependencies."""

    def __init__(self, config: Config, logger: Any) -> None:
        if logger is None:
            raise ValueError("Logger cannot be None")

        self._config = config
        self._logger = logger

    @property
    def config(self) -> Config:
        """Shared, read-only access to the configuration object."""
        return self._config

    @property
    def logger(self) -> Any:
        """Shared, read-only access to the component logger."""
        return self._logger

    def _ensure_directory(self, directory: Path) -> Path:
        """Ensure a directory exists before writing to it."""
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise RuntimeError(f"Cannot create directory {directory}: {exc}") from exc
        return directory
