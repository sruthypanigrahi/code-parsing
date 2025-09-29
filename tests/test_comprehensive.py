"""Comprehensive test suite for improved coverage."""

import tempfile
from pathlib import Path

import pytest

from src.async_processor import AsyncProcessor
from src.base import BaseValidator
from src.exceptions import InvalidInputError, PDFNotFoundError
from src.input_validator import InputValidator
from src.progress_tracker import ProgressBar, StepTracker


class TestInputValidator:
    """Test input validation functionality."""

    def test_validate_search_term_valid(self):
        """Test valid search term validation."""
        result = InputValidator.validate_search_term("USB Power Delivery")
        assert result == "USB Power Delivery"

    def test_validate_search_term_empty(self):
        """Test empty search term validation."""
        with pytest.raises(InvalidInputError, match="cannot be empty"):
            InputValidator.validate_search_term("")

    def test_validate_search_term_too_long(self):
        """Test overly long search term."""
        long_term = "x" * 1001
        with pytest.raises(InvalidInputError, match="too long"):
            InputValidator.validate_search_term(long_term)

    def test_validate_search_term_dangerous_chars(self):
        """Test search term with dangerous characters."""
        result = InputValidator.validate_search_term("USB<script>alert()</script>")
        assert "<script>" not in result
        assert "USB" in result

    def test_validate_page_range_valid(self):
        """Test valid page range."""
        result = InputValidator.validate_page_range(1, 10)
        assert result == (1, 10)

    def test_validate_page_range_invalid_start(self):
        """Test invalid start page."""
        with pytest.raises(InvalidInputError, match="positive integer"):
            InputValidator.validate_page_range(0)

    def test_validate_page_range_invalid_end(self):
        """Test invalid end page."""
        with pytest.raises(InvalidInputError, match=">= start page"):
            InputValidator.validate_page_range(10, 5)

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        result = InputValidator.sanitize_filename("file<>name?.txt")
        assert result == "file__name_.txt"

    def test_sanitize_filename_empty(self):
        """Test empty filename sanitization."""
        result = InputValidator.sanitize_filename("")
        assert result == "output"


class TestProgressTracker:
    """Test progress tracking functionality."""

    def test_progress_bar_creation(self):
        """Test progress bar creation."""
        pbar = ProgressBar(100, "Test")
        assert pbar.total == 100
        assert pbar.current == 0
        assert pbar.description == "Test"

    def test_progress_bar_update(self):
        """Test progress bar updates."""
        pbar = ProgressBar(10, "Test")
        pbar.update(5)
        assert pbar.current == 5

        pbar.update(10)  # Should cap at total
        assert pbar.current == 10

    def test_progress_bar_set_progress(self):
        """Test setting absolute progress."""
        pbar = ProgressBar(100, "Test")
        pbar.set_progress(50)
        assert pbar.current == 50

        pbar.set_progress(-10)  # Should cap at 0
        assert pbar.current == 0

        pbar.set_progress(150)  # Should cap at total
        assert pbar.current == 100

    def test_step_tracker(self):
        """Test step tracker functionality."""
        steps = ["Step 1", "Step 2", "Step 3"]
        tracker = StepTracker(steps, "Test Process")

        assert tracker.current_step == 0

        tracker.next_step()
        assert tracker.current_step == 1

        tracker.next_step("Custom message")
        assert tracker.current_step == 2


class MockValidator(BaseValidator):
    """Mock validator for testing base class."""

    def _validate_line(self, line: str, line_num: int) -> bool:
        return line.strip() != "invalid"

    def _display_summary(self) -> None:
        print(f"Mock validation: {self.valid_count} valid, {self.error_count} errors")


class TestBaseValidator:
    """Test base validator functionality."""

    def test_base_validator_with_valid_file(self):
        """Test base validator with valid content."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("valid line 1\nvalid line 2\n")
            temp_path = Path(f.name)

        try:
            validator = MockValidator(temp_path)
            result = validator.validate()

            assert result is True
            assert validator.valid_count == 2
            assert validator.error_count == 0
        finally:
            temp_path.unlink()

    def test_base_validator_with_invalid_content(self):
        """Test base validator with invalid content."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("valid line\ninvalid\nvalid line 2\n")
            temp_path = Path(f.name)

        try:
            validator = MockValidator(temp_path)
            result = validator.validate()

            assert result is False
            assert validator.valid_count == 2
            assert validator.error_count == 1
        finally:
            temp_path.unlink()

    def test_base_validator_file_not_found(self):
        """Test base validator with non-existent file."""
        validator = MockValidator(Path("nonexistent.txt"))
        result = validator.validate()
        assert result is False


class TestAsyncProcessor:
    """Test async processing functionality."""

    @pytest.mark.asyncio
    async def test_async_processor_creation(self):
        """Test async processor creation."""
        processor = AsyncProcessor(max_workers=2)
        assert processor.max_workers == 2
        processor.executor.shutdown(wait=True)

    @pytest.mark.asyncio
    async def test_process_batch_async(self):
        """Test async batch processing."""

        def square(x):
            return x * x

        with AsyncProcessor(max_workers=2) as processor:
            items = [1, 2, 3, 4, 5]
            results = await processor.process_batch_async(square, items, batch_size=2)

            assert results == [1, 4, 9, 16, 25]


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_input_handling(self):
        """Test handling of empty inputs."""
        # Test empty search term
        with pytest.raises(InvalidInputError):
            InputValidator.validate_search_term("")

        # Test empty filename
        result = InputValidator.sanitize_filename("")
        assert result == "output"

    def test_large_input_handling(self):
        """Test handling of large inputs."""
        # Test very long search term
        long_term = "x" * 1001
        with pytest.raises(InvalidInputError):
            InputValidator.validate_search_term(long_term)

    def test_special_character_handling(self):
        """Test handling of special characters."""
        # Test filename with special chars
        result = InputValidator.sanitize_filename('file<>:"/\\|?*name.txt')
        assert all(char not in result for char in '<>:"/\\|?*')

    def test_unicode_handling(self):
        """Test handling of unicode characters."""
        # Test search term with unicode
        result = InputValidator.validate_search_term("USB 电源传输")
        assert "USB" in result
        assert "电源传输" in result


@pytest.fixture
def temp_pdf_file():
    """Create a temporary PDF-like file for testing."""
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".pdf") as f:
        f.write(b"%PDF-1.4\n")  # PDF header
        f.write(b"Some PDF content here")
        temp_path = Path(f.name)

    yield temp_path
    temp_path.unlink()


class TestFileValidation:
    """Test file validation with real files."""

    def test_validate_pdf_path_valid(self, temp_pdf_file):
        """Test PDF validation with valid file."""
        result = InputValidator.validate_pdf_path(temp_pdf_file)
        assert result == temp_pdf_file.resolve()

    def test_validate_pdf_path_not_found(self):
        """Test PDF validation with non-existent file."""
        with pytest.raises(PDFNotFoundError):
            InputValidator.validate_pdf_path("nonexistent.pdf")

    def test_validate_pdf_path_wrong_extension(self, temp_pdf_file):
        """Test PDF validation with wrong extension."""
        # Rename to wrong extension
        wrong_ext = temp_pdf_file.with_suffix(".txt")
        temp_pdf_file.rename(wrong_ext)

        try:
            with pytest.raises(InvalidInputError, match="Invalid file extension"):
                InputValidator.validate_pdf_path(wrong_ext)
        finally:
            wrong_ext.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
