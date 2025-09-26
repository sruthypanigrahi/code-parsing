# Contributing to USB PD Parser

Thank you for your interest in contributing to the USB PD Parser! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of PDF processing and text parsing

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/usb-pd-parser.git
   cd usb-pd-parser
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

5. **Verify Setup**
   ```bash
   python main.py --help
   pytest tests/ -v
   ```

## 🏗️ Project Structure

```
src/
├── app.py              # Main orchestrator
├── extractor.py        # PDF extraction
├── parsing_strategies.py # TOC parsing
├── writer.py           # Output writing
├── validator.py        # Data validation
├── models.py           # Data models
├── factory.py          # Component factories
├── hierarchy.py        # Hierarchy assignment
├── performance.py      # Performance monitoring
├── cache.py            # Caching utilities
├── exceptions.py       # Custom exceptions
├── interfaces.py       # Protocol definitions
└── logger.py           # Logging setup
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_extractor.py -v

# Run tests matching pattern
pytest -k "test_parse" -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test names: `test_extract_front_pages_success`
- Include both positive and negative test cases
- Mock external dependencies (PDF files, network calls)

Example test:
```python
def test_extract_front_pages_success():
    """Test successful page extraction."""
    # Arrange
    test_file = Path("test.pdf")
    test_file.touch()
    
    # Act
    pages = list(extract_front_pages(test_file, max_pages=2))
    
    # Assert
    assert len(pages) == 2
    
    # Cleanup
    test_file.unlink()
```

## 🎨 Code Style

### Formatting and Linting

We use several tools to maintain code quality:

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy src --ignore-missing-imports

# Run all checks
black . && ruff check . && mypy src --ignore-missing-imports
```

### Code Standards

- **Line Length**: 88 characters (Black default)
- **Type Hints**: Required for all public functions
- **Docstrings**: Google style for all public functions and classes
- **Imports**: Sorted with isort (handled by ruff)
- **Naming**: 
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`

### Example Function

```python
def extract_front_pages(pdf_path: Path, max_pages: int = 10) -> Iterator[str]:
    """Extract text from front pages of PDF.
    
    Args:
        pdf_path: Path to PDF file
        max_pages: Maximum number of pages to extract (default: 10)
        
    Yields:
        str: Text content of each page
        
    Raises:
        PDFNotFoundError: If PDF file doesn't exist
        RuntimeError: If PDF cannot be opened
    """
    # Implementation here
```

## 🔧 Architecture Guidelines

### Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Dependency Injection**: Use protocols and factories
3. **Streaming Processing**: Use generators for memory efficiency
4. **Error Handling**: Proper exception hierarchy and logging
5. **Type Safety**: Full type hints and mypy compliance

### Adding New Features

#### New Parser Strategy

1. Implement `BaseTOCParser` protocol:
   ```python
   class MyTOCParser(BaseTOCParser):
       def parse_lines(self, lines: Iterator[str]) -> Iterator[TOCEntry]:
           # Implementation
   ```

2. Register with factory:
   ```python
   ParserFactory.register_parser("my_parser", MyTOCParser)
   ```

3. Add tests:
   ```python
   def test_my_parser_success():
       parser = MyTOCParser("Test Doc")
       # Test implementation
   ```

#### New Output Format

1. Implement `OutputWriter` protocol
2. Update factory or configuration
3. Maintain streaming interface
4. Add comprehensive tests

### Performance Considerations

- Use generators for large data processing
- Implement caching for expensive operations
- Add performance monitoring with `@timer` decorator
- Profile memory usage for large PDFs

## 📝 Documentation

### Code Documentation

- All public functions must have docstrings
- Use Google docstring format
- Include type hints for all parameters and return values
- Document exceptions that can be raised

### User Documentation

- Update README.md for new features
- Add examples for new functionality
- Update configuration documentation
- Include performance benchmarks

## 🐛 Bug Reports

### Before Submitting

1. Check existing issues
2. Verify the bug with latest version
3. Create minimal reproduction case

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. With input file '...'
3. See error

**Expected Behavior**
What you expected to happen

**Environment**
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- Package version: [e.g., 1.0.0]

**Additional Context**
Any other context about the problem
```

## 💡 Feature Requests

### Before Submitting

1. Check if feature already exists
2. Consider if it fits project scope
3. Think about implementation approach

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other approaches you've considered

**Additional Context**
Any other context or screenshots
```

## 🔄 Pull Request Process

### Before Submitting

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes with proper tests
3. Run all quality checks: `black . && ruff check . && mypy src && pytest`
4. Update documentation if needed
5. Commit with descriptive messages

### PR Guidelines

- **Title**: Clear, descriptive title
- **Description**: Explain what and why
- **Tests**: Include tests for new functionality
- **Documentation**: Update docs if needed
- **Breaking Changes**: Clearly mark and explain

### PR Template

```markdown
**Description**
Brief description of changes

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

**Testing**
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

**Checklist**
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## 🏷️ Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version in `__init__.py`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Create release PR
5. Tag release: `git tag v1.0.0`
6. Push tags: `git push --tags`

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

### Getting Help

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For security issues or private matters

## 📚 Resources

### Learning Resources

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Development Tools

- [Black](https://black.readthedocs.io/) - Code formatting
- [Ruff](https://docs.astral.sh/ruff/) - Linting
- [MyPy](https://mypy.readthedocs.io/) - Type checking
- [Pytest](https://docs.pytest.org/) - Testing

Thank you for contributing to USB PD Parser! 🚀