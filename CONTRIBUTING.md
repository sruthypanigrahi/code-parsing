# Contributing to USB PD Specification Parser

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/usb-pd-parser.git
   cd usb-pd-parser
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Code Standards

### Code Formatting
- Use **Black** for code formatting: `black .`
- Use **Ruff** for linting: `ruff check .`
- Use **MyPy** for type checking: `mypy src`

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions and methods
- Keep functions under 50 lines when possible
- Use descriptive variable and function names

### Documentation
- Add Google-style docstrings to all functions and classes
- Update README.md for new features
- Include examples in docstrings

## Testing

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_parser.py -v
```

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names
- Include edge cases and error conditions
- Aim for >90% code coverage

## Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following the style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Run Quality Checks**
   ```bash
   black .
   ruff check .
   mypy src --ignore-missing-imports
   pytest tests/ -v
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Commit Message Format

Use conventional commits format:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `test:` adding tests
- `refactor:` code refactoring
- `perf:` performance improvements

## Issue Reporting

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Sample files (if applicable)

## Questions?

Feel free to open an issue for questions or join our discussions!