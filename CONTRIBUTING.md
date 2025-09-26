# Contributing Guide

## Quick Start for Contributors

```bash
# Fork and clone
git clone https://github.com/yourusername/usb-pd-parser.git
cd usb-pd-parser

# Setup development environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest -v

# Check code quality
black . && ruff check . && mypy src --ignore-missing-imports
```

## Development Setup

### Prerequisites

- Python 3.9+
- Git
- Virtual environment tool

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/username/usb-pd-parser.git
   cd usb-pd-parser
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   # Core dependencies
   pip install -r requirements.txt
   
   # Development dependencies
   pip install -r requirements-dev.txt
   
   # Async dependencies (optional)
   pip install -r requirements-async.txt
   ```

4. **Verify installation**
   ```bash
   python main.py --mode 3  # Test with small extraction
   pytest tests/ -v         # Run test suite
   ```

## Code Quality Standards

### Formatting and Linting

```bash
# Format code with Black
black .

# Lint with Ruff
ruff check .
ruff check . --fix  # Auto-fix issues

# Type checking with MyPy
mypy src --ignore-missing-imports

# Run all quality checks
black . && ruff check . && mypy src --ignore-missing-imports
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Code Style Guidelines

- **Black formatting**: All code must pass `black --check .`
- **Type annotations**: All functions must have type hints
- **Docstrings**: All public methods must have docstrings
- **Line length**: Maximum 88 characters (Black default)
- **Import sorting**: Use `ruff` for import organization

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest tests/test_comprehensive.py -v
pytest tests/test_edge_cases.py -v
pytest -m asyncio  # Async tests only

# Run performance tests
python tools/benchmark.py
```

### Writing Tests

```python
# Test file: tests/test_new_feature.py
import pytest
from src.new_module import NewClass

class TestNewClass:
    def test_basic_functionality(self):
        """Test basic functionality."""
        instance = NewClass()
        result = instance.process("test input")
        assert result == "expected output"
    
    def test_error_handling(self):
        """Test error handling."""
        instance = NewClass()
        with pytest.raises(ValueError):
            instance.process(None)
```

### Test Coverage Requirements

- **Minimum coverage**: 90%
- **New features**: Must include tests
- **Bug fixes**: Must include regression tests
- **Edge cases**: Must be covered

## Architecture Guidelines

### Object-Oriented Design

- **Single Responsibility**: Each class has one clear purpose
- **Encapsulation**: Use private methods for internal logic
- **Inheritance**: Use base classes for common functionality
- **Type Safety**: Full type annotations throughout

### Class Structure Example

```python
from typing import Optional, List
from pathlib import Path
from .base import BaseProcessor

class NewProcessor(BaseProcessor):
    """Process new type of content.
    
    Args:
        config: Configuration object
        logger: Logger instance
    """
    
    def __init__(self, config: Config, logger: Logger):
        super().__init__(config, logger)
        self._internal_state: dict[str, Any] = {}
    
    def process(self, input_data: str) -> List[dict[str, Any]]:
        """Process input data and return results.
        
        Args:
            input_data: Raw input to process
            
        Returns:
            List of processed items
            
        Raises:
            ProcessingError: If processing fails
        """
        try:
            return self._internal_process(input_data)
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            raise ProcessingError(f"Failed to process: {e}") from e
    
    def _internal_process(self, data: str) -> List[dict[str, Any]]:
        """Internal processing logic."""
        # Implementation here
        pass
```

## Contribution Workflow

### 1. Issue Creation

- **Bug reports**: Use bug report template
- **Feature requests**: Use feature request template
- **Questions**: Use discussion forum

### 2. Branch Strategy

```bash
# Create feature branch
git checkout -b feature/amazing-feature

# Create bugfix branch
git checkout -b bugfix/fix-parsing-issue

# Create documentation branch
git checkout -b docs/update-readme
```

### 3. Development Process

1. **Write tests first** (TDD approach)
2. **Implement feature**
3. **Update documentation**
4. **Run quality checks**
5. **Commit changes**

### 4. Commit Guidelines

```bash
# Good commit messages
git commit -m "feat: add table extraction for complex layouts"
git commit -m "fix: handle empty PDF pages correctly"
git commit -m "docs: update API documentation for new methods"
git commit -m "test: add edge cases for TOC parsing"

# Commit message format
<type>: <description>

Types: feat, fix, docs, test, refactor, style, chore
```

### 5. Pull Request Process

1. **Create PR** with descriptive title
2. **Fill PR template** completely
3. **Link related issues**
4. **Request review** from maintainers
5. **Address feedback**
6. **Merge after approval**

## Adding New Features

### 1. New Extractor Class

```python
# src/new_extractor.py
from typing import Iterator, Dict, Any
from .base import BaseExtractor

class NewExtractor(BaseExtractor):
    """Extract new type of content from PDFs."""
    
    def extract(self, pdf_path: Path) -> Iterator[Dict[str, Any]]:
        """Extract content from PDF."""
        # Implementation
        pass
```

### 2. Update Pipeline

```python
# src/pipeline_orchestrator.py
def run_full_pipeline(self, mode: int = 1) -> dict[str, Any]:
    # Add new extractor to pipeline
    new_extractor = NewExtractor(self.cfg, self.logger)
    new_results = new_extractor.extract(pdf_path)
```

### 3. Add Tests

```python
# tests/test_new_extractor.py
class TestNewExtractor:
    def test_extraction(self):
        extractor = NewExtractor(config, logger)
        results = list(extractor.extract(sample_pdf))
        assert len(results) > 0
```

### 4. Update Documentation

- Add to README.md features list
- Update USAGE.md with examples
- Add to API documentation

## Bug Fixes

### 1. Reproduce the Bug

```python
# tests/test_bug_reproduction.py
def test_bug_reproduction():
    """Reproduce the reported bug."""
    # Setup that causes the bug
    # Assert the bug occurs
    pass
```

### 2. Fix the Issue

- Identify root cause
- Implement minimal fix
- Ensure no regressions

### 3. Add Regression Test

```python
def test_bug_fix():
    """Ensure bug is fixed and doesn't regress."""
    # Test the fix works
    # Test edge cases
    pass
```

## Documentation

### Code Documentation

```python
def complex_function(param1: str, param2: Optional[int] = None) -> List[str]:
    """Process complex data with multiple parameters.
    
    This function handles complex processing logic and returns
    a list of processed strings.
    
    Args:
        param1: Primary input string to process
        param2: Optional integer parameter for processing mode
        
    Returns:
        List of processed strings
        
    Raises:
        ValueError: If param1 is empty
        ProcessingError: If processing fails
        
    Example:
        >>> result = complex_function("test", 42)
        >>> len(result)
        1
    """
```

### README Updates

- Keep quickstart section current
- Update feature list for new capabilities
- Add performance benchmarks
- Update installation instructions

## Release Process

### Version Numbering

- **Major**: Breaking changes (1.0.0 → 2.0.0)
- **Minor**: New features (1.0.0 → 1.1.0)
- **Patch**: Bug fixes (1.0.0 → 1.0.1)

### Release Checklist

1. **Update version** in `__init__.py`
2. **Update CHANGELOG.md**
3. **Run full test suite**
4. **Update documentation**
5. **Create release tag**
6. **Publish release**

## Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Code Review**: Pull request comments

### Maintainer Response Time

- **Bug reports**: 2-3 business days
- **Feature requests**: 1 week
- **Pull requests**: 3-5 business days

## Recognition

Contributors are recognized in:
- **README.md**: Contributors section
- **CHANGELOG.md**: Release notes
- **GitHub**: Contributor graphs

Thank you for contributing to USB PD Parser! 🚀