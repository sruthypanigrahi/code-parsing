"""Test core OOP classes."""

from pathlib import Path

import pytest

from src.core.cleaner import TextCleaner
from src.core.config import ConfigManager
from src.core.loader import PDFLoader
from src.core.parser import PDFParser
from src.core.writer import OutputWriter


class TestPDFLoader:
    """Test PDFLoader class."""

    def test_init(self):
        loader = PDFLoader("assets")
        assert loader.input_dir == Path("assets")

    def test_load_file_exists(self):
        loader = PDFLoader()
        # Test with existing PDF
        if Path("assets/USB_PD_R3_2_V1.1_2024-10.pdf").exists():
            result = loader.load_file("assets/USB_PD_R3_2_V1.1_2024-10.pdf")
            assert isinstance(result, Path)

    def test_load_file_not_exists(self):
        loader = PDFLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_file("nonexistent.pdf")


class TestPDFParser:
    """Test PDFParser class."""

    def test_init(self):
        cfg = {"max_pages": 10}
        parser = PDFParser(cfg)
        assert parser.cfg == cfg

    def test_extract_paragraphs(self):
        cfg = {}
        parser = PDFParser(cfg)
        lines = ["Line 1", "", "Line 2", "Line 3", ""]
        result = parser._extract_paragraphs(lines)
        assert len(result) == 2


class TestTextCleaner:
    """Test TextCleaner class."""

    def test_clean_text(self):
        cleaner = TextCleaner()
        dirty_text = "  Hello   world  \n\n  "
        clean_text = cleaner.clean_text(dirty_text)
        assert clean_text == "Hello world"

    def test_clean_paragraphs(self):
        cleaner = TextCleaner()
        paragraphs = ["  Para 1  ", "", "Para 2"]
        result = cleaner.clean_paragraphs(paragraphs)
        assert result == ["Para 1", "Para 2"]


class TestOutputWriter:
    """Test OutputWriter class."""

    def test_init(self):
        writer = OutputWriter("test_output")
        assert writer.output_dir == Path("test_output")

    def test_write_json(self, tmp_path):
        writer = OutputWriter(str(tmp_path))
        data = {"test": "data"}
        result = writer.write_json(data, "test.json")
        assert result.exists()
        assert result.name == "test.json"


class TestConfigManager:
    """Test ConfigManager class."""

    def test_init_default(self):
        config = ConfigManager("nonexistent.yml")
        assert "pdf_input_file" in config.config

    def test_get_set(self):
        config = ConfigManager("nonexistent.yml")
        config.set("test_key", "test_value")
        assert config.get("test_key") == "test_value"
        assert config.get("nonexistent", "default") == "default"
