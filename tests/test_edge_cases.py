"""Edge case tests with OOP principles."""

from pathlib import Path
import pytest
from src.config import Config
from src.models import TOCEntry
from src.pdf_extractor import BaseExtractor


class MockFailingExtractor(BaseExtractor):  # Inheritance
    """Mock failing extractor (Inheritance, Polymorphism)."""
    
    def extract(self):  # Polymorphism
        raise RuntimeError("Mock failure")


class TestEdgeCases:  # Encapsulation
    """Test edge cases (Encapsulation, Abstraction)."""
    
    def test_missing_pdf_file(self):  # Encapsulation
        with pytest.raises(FileNotFoundError):
            MockFailingExtractor(Path("nonexistent.pdf"))
    
    def test_invalid_config_file(self):  # Encapsulation
        config = Config("nonexistent_config.yml")
        
        # Should use defaults (Encapsulation)
        assert config.pdf_input_file is not None
        assert config.output_directory is not None
    
    def test_invalid_toc_entry_data(self):  # Encapsulation
        with pytest.raises(ValueError):
            TOCEntry(
                doc_title="Test",
                section_id="",  # Invalid empty section_id
                title="Test",
                full_path="Test",
                page=1,
                level=1
            )
    
    def test_invalid_section_id_format(self):  # Encapsulation
        with pytest.raises(ValueError):
            TOCEntry(
                doc_title="Test",
                section_id="invalid..format",  # Invalid format
                title="Test",
                full_path="Test",
                page=1,
                level=1
            )
    
    def test_polymorphic_error_handling(self, tmp_path: Path):  # Polymorphism
        test_file: Path = tmp_path / "test.pdf"
        test_file.touch()
        
        extractor = MockFailingExtractor(test_file)  # Polymorphism
        
        with pytest.raises(RuntimeError, match="Mock failure"):
            extractor.extract()
    
    def test_inheritance_error_propagation(self, tmp_path: Path):  # Inheritance
        test_file: Path = tmp_path / "test.pdf"
        test_file.touch()
        
        extractor = MockFailingExtractor(test_file)
        
        # Test inherited behavior (Inheritance)
        assert isinstance(extractor, BaseExtractor)
        assert hasattr(extractor, '_pdf_path')
        assert hasattr(extractor, '_logger')