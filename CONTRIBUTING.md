# Contributing to USB PD Specification Parser

Thank you for your interest in contributing to the USB PD Specification Parser! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/usb-pd-parser.git
   cd usb-pd-parser
   ```
3. **Set up development environment**:
   ```bash
   python setup_dev.py
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

### Prerequisites
- Python 3.9 or higher
- Git
- Optional: Docker for containerized development

### Environment Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
python run_tests.py
```

## 📝 Code Style and Standards

### Code Formatting
We use automated code formatting tools:
- **Black** for code formatting
- **isort** for import sorting
- **Ruff** for linting
- **mypy** for type checking

Run before committing:
```bash
black .
isort .
ruff check .
mypy src --ignore-missing-imports
```

### Code Quality Requirements
- **Type hints**: All functions must have type annotations
- **Docstrings**: All public functions and classes must have docstrings
- **Test coverage**: Minimum 85% test coverage required
- **No print statements**: Use logging instead
- **Pydantic models**: Use for data validation and serialization

### Pre-commit Hooks
Pre-commit hooks automatically run code quality checks:
```bash
# Install hooks (done automatically by setup_dev.py)
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests with coverage
python run_tests.py

# Run specific test categories
pytest tests/test_parser.py -v
pytest tests/test_end_to_end.py -v

# Run with specific markers
pytest -m "not slow" -v
```

### Writing Tests
- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test component interactions
- **Edge cases**: Test error conditions and boundary cases
- **Performance tests**: For large file processing

Example test structure:
```python
class TestYourFeature:
    def setup_method(self):
        """Setup test fixtures."""
        pass
    
    def test_basic_functionality(self):
        """Test basic feature functionality."""
        assert True
    
    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        with pytest.raises(ValueError):
            # Test error condition
            pass
```

## 📋 Pull Request Process

### Before Submitting
1. **Run all tests**: Ensure all tests pass
2. **Check code quality**: Run pre-commit hooks
3. **Update documentation**: Add/update docstrings and README if needed
4. **Add tests**: Include tests for new functionality
5. **Update changelog**: Add entry to CHANGELOG.md

### Pull Request Guidelines
- **Clear title**: Describe what the PR does
- **Detailed description**: Explain the changes and why they're needed
- **Link issues**: Reference related issues with "Fixes #123"
- **Small PRs**: Keep changes focused and reviewable
- **Update tests**: Include tests for new features or bug fixes

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated existing tests if needed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Changelog updated
```

## 🐛 Bug Reports

### Before Reporting
1. **Search existing issues** to avoid duplicates
2. **Try latest version** to see if bug is already fixed
3. **Minimal reproduction** case if possible

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
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- Package version: [e.g., 1.0.0]

**Additional Context**
Any other context about the problem
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other approaches you've considered

**Additional Context**
Any other context or screenshots
```

## 🏗️ Architecture Guidelines

### Project Structure
```
usb-pd-parser/
├── src/                 # Core application code
│   ├── app.py          # Main orchestrator
│   ├── extractor.py    # PDF extraction
│   ├── parser.py       # TOC parsing
│   ├── writer.py       # Output writing
│   ├── validator.py    # Data validation
│   └── models.py       # Pydantic models
├── tests/              # Test suite
├── assets/             # Sample files
└── outputs/            # Generated files (gitignored)
```

### Design Principles
- **Single Responsibility**: Each module has one clear purpose
- **Dependency Injection**: Pass dependencies explicitly
- **Type Safety**: Use type hints and Pydantic models
- **Error Handling**: Graceful error handling with logging
- **Performance**: Memory-efficient processing for large files

## 📚 Documentation

### Docstring Format
Use Google-style docstrings:
```python
def parse_toc(self, pages: List[Tuple[int, str]]) -> List[TOCEntry]:
    """Parse Table of Contents from page text data.
    
    Args:
        pages: List of (page_number, text_content) tuples.
        
    Returns:
        List of parsed and deduplicated TOC entries.
        
    Raises:
        ValueError: If pages list is invalid.
        
    Example:
        >>> parser = TOCParser()
        >>> entries = parser.parse_toc([(1, "1.1 Introduction  15")])
        >>> print(f"Found {len(entries)} entries")
    """
```

### README Updates
When adding features, update:
- Feature list in README
- Usage examples
- Configuration options
- Performance characteristics

## 🤝 Community Guidelines

### Code of Conduct
This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Please read and follow it.

### Communication
- **Be respectful** and constructive in discussions
- **Ask questions** if anything is unclear
- **Help others** when you can
- **Share knowledge** and best practices

### Recognition
Contributors are recognized in:
- GitHub contributors list
- Release notes for significant contributions
- Special thanks in documentation

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Code Review**: Request reviews on pull requests

## 🏷️ Release Process

### Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist
1. Update version in relevant files
2. Update CHANGELOG.md
3. Create GitHub release with tag
4. Update documentation if needed

Thank you for contributing to USB PD Specification Parser! 🎉