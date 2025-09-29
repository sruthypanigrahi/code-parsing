"""Test configuration with OOP principles."""

import pytest
from pathlib import Path
from typing import Any, Dict
from src.config import Config


class TestConfig:  # Encapsulation
    """Test config helper (Encapsulation, Abstraction)."""
    
    def __init__(self, test_data: Dict[str, Any]):
        self._test_data = test_data  # Encapsulation
    
    def create_config_file(self, tmp_path: Path, filename: str = "test_config.yml") -> Path:
        config_file = tmp_path / filename
        config_content = "\n".join([f"{k}: {v}" for k, v in self._test_data.items()])
        config_file.write_text(config_content)
        return config_file
    
    def get_test_data(self) -> Dict[str, Any]:  # Encapsulation
        return self._test_data.copy()


class MockPDFFile:  # Abstraction
    """Mock PDF file helper (Abstraction, Encapsulation)."""
    
    def __init__(self, content: str = "Mock PDF content"):
        self._content = content  # Encapsulation
    
    def create_file(self, tmp_path: Path, filename: str = "test.pdf") -> Path:
        pdf_file = tmp_path / filename
        pdf_file.write_text(self._content)
        return pdf_file
    
    @property  # Encapsulation
    def content(self) -> str:
        return self._content


@pytest.fixture  # Factory pattern (Abstraction)
def test_config_helper():
    return TestConfig({
        "pdf_input_file": "assets/test.pdf",
        "output_directory": "test_outputs",
        "max_pages": 50
    })


@pytest.fixture  # Factory pattern (Abstraction)
def mock_pdf_helper():
    return MockPDFFile("Sample PDF content for testing")


@pytest.fixture  # Factory pattern (Abstraction)
def sample_config(tmp_path: Path):
    config_helper = TestConfig({
        "pdf_input_file": "test.pdf",
        "output_directory": "outputs",
        "max_pages": 100
    })
    config_file = config_helper.create_config_file(tmp_path)
    return Config(str(config_file))


@pytest.fixture  # Factory pattern (Abstraction)
def sample_pdf_file(tmp_path: Path):
    pdf_helper = MockPDFFile("Test PDF content")
    return pdf_helper.create_file(tmp_path)