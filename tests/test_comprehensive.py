"""Comprehensive tests with OOP principles."""

# import pytest
from pathlib import Path
from typing import Union
from src.config import Config
from src.models import TOCEntry, BaseContent, PageContent


class TestConfig:  # Encapsulation
    """Test config class (Encapsulation, Abstraction)."""
    
    def test_config_creation(self):  # Encapsulation
        config = Config("application.yml")  # Abstraction
        
        # Test encapsulated properties (Encapsulation)
        assert config.pdf_input_file is not None
        assert config.output_directory is not None
        assert config.max_pages is None
    
    def test_config_with_file(self, tmp_path: Path):  # Encapsulation
        config_file: Path = tmp_path / "test.yml"
        config_file.write_text("pdf_input_file: test.pdf\nmax_pages: 100")
        
        config = Config(str(config_file))
        assert config.max_pages == 100


class TestModels:  # Encapsulation
    """Test data models (Encapsulation, Abstraction)."""
    
    def test_base_content_abstraction(self):  # Abstraction
        content = BaseContent(page=1, content="test")
        assert content.page == 1
        assert content.content == "test"
    
    def test_page_content_inheritance(self):  # Inheritance
        page_content = PageContent(
            page=1, content="test", text="sample", 
            image_count=2, table_count=1
        )
        
        # Test inherited properties (Inheritance)
        assert isinstance(page_content, BaseContent)
        assert page_content.page == 1
        assert page_content.image_count == 2
    
    def test_toc_entry_validation(self):  # Encapsulation
        entry = TOCEntry(
            doc_title="Test Doc",
            section_id="1.2",
            title="Test Section",
            full_path="1.2 Test Section",
            page=10,
            level=2
        )
        
        # Test computed properties (Abstraction)
        assert entry.level == 2
        assert entry.section_id == "1.2"
    
    def test_polymorphism_in_models(self):  # Polymorphism
        models: list[Union[BaseContent, PageContent]] = [
            BaseContent(page=1, content="base"),
            PageContent(page=2, content="page", text="text", image_count=0, table_count=0)
        ]
        
        for model in models:
            # Same interface, different implementations (Polymorphism)
            assert hasattr(model, 'page')
            assert hasattr(model, 'content')
            assert model.page > 0