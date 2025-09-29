"""Tests for extractors with OOP principles."""

from pathlib import Path
import pytest
from src.pdf_extractor import BaseExtractor


class MockExtractor(BaseExtractor):  # Inheritance
    """Mock extractor (Inheritance, Polymorphism)."""
    
    def extract(self):  # Polymorphism
        return ["mock_data"]


class TestBaseExtractor:  # Encapsulation
    """Test base extractor (Encapsulation, Abstraction)."""
    
    def test_file_validation(self):  # Encapsulation
        """Test file validation (Abstraction)."""
        with pytest.raises(FileNotFoundError):
            MockExtractor(Path("nonexistent.pdf"))
    
    def test_valid_file(self, tmp_path: Path):  # Encapsulation
        """Test with valid file."""
        test_file: Path = tmp_path / "test.pdf"
        test_file.touch()
        
        extractor = MockExtractor(test_file)  # Polymorphism
        assert extractor.extract() == ["mock_data"]
    
    def test_protected_attributes(self, tmp_path: Path):  # Encapsulation
        """Test protected attributes."""
        test_file: Path = tmp_path / "test.pdf"
        test_file.touch()
        
        extractor = MockExtractor(test_file)
        
        # Test protected attributes (Encapsulation)
        assert hasattr(extractor, '_pdf_path')
        assert hasattr(extractor, '_logger')
        assert getattr(extractor, '_pdf_path') == test_file  # type: ignore
    
    def test_inheritance_structure(self, tmp_path: Path):  # Inheritance
        """Test inheritance structure."""
        test_file: Path = tmp_path / "test.pdf"
        test_file.touch()
        
        extractor = MockExtractor(test_file)
        
        # Test inheritance (Inheritance)
        assert isinstance(extractor, BaseExtractor)
        assert hasattr(extractor, '_get_fitz')
    
    def test_polymorphism(self, tmp_path: Path):  # Polymorphism
        """Test polymorphic behavior."""
        test_file: Path = tmp_path / "test.pdf"
        test_file.touch()
        
        # Different implementations (Polymorphism)
        extractors = [MockExtractor(test_file)]
        
        for extractor in extractors:
            result = extractor.extract()  # Same interface
            assert isinstance(result, list)
    
    def test_abstraction(self):  # Abstraction
        """Test abstract base class."""
        with pytest.raises(TypeError):
            # Cannot instantiate abstract class (Abstraction)
            BaseExtractor(Path("test.pdf"))  # type: ignore