"""Unit tests covering new OOP mixins and factories."""

from pathlib import Path

import pytest

from src.support.validation_generator import (
    BaseValidator,
    ValidationStrategySelector,
)
from src.utils.mixins import ExtractionTrackerMixin, OutputPathMixin


class _TrackerStub(ExtractionTrackerMixin):
    """Minimal concrete class for exercising ExtractionTrackerMixin."""

    def __init__(self) -> None:
        super().__init__()


class _OutputPathStub(OutputPathMixin):
    """Minimal concrete class for exercising OutputPathMixin."""

    def __init__(self, output_path: Path) -> None:
        super().__init__(output_path)


def test_extraction_tracker_mixin_counts() -> None:
    """ExtractionTrackerMixin should record extraction/error metrics."""
    tracker = _TrackerStub()
    tracker._record_extraction()  # Protected for subclass use
    tracker._record_error()
    assert tracker.extraction_count == 1
    assert tracker.error_count == 1


def test_output_path_mixin_prepares_directory(tmp_path: Path) -> None:
    """OutputPathMixin should resolve the path and create the parent directory."""
    target = tmp_path / "nested" / "file.txt"
    stub = _OutputPathStub(target)
    assert stub.output_path == target.resolve()
    assert stub.output_directory == target.parent.resolve()
    assert target.parent.exists()


def test_validation_selector_falls_back_to_available_type(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Validation selector should fallback when the preferred generator fails."""
    created_calls: list[str] = []

    def fake_create(validator_type: str, output_dir: Path) -> BaseValidator:
        created_calls.append(validator_type)
        if validator_type == "excel":
            raise RuntimeError("Excel unavailable")

        class DummyValidator(BaseValidator):
            def generate_validation(
                self, toc_data: list[dict], spec_data: list[dict]
            ) -> Path:
                return output_dir / "validation_report.json"

        return DummyValidator(output_dir)

    monkeypatch.setattr(
        "src.support.validation_generator.ValidationGeneratorFactory.create",
        fake_create,
    )

    validator = ValidationStrategySelector.select(tmp_path, None)
    assert created_calls == ["excel", "json"]
    result = validator.generate_validation([], [])
    assert result == tmp_path / "validation_report.json"
