# Contributing

## Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/usb-pd-parser.git`
3. Create virtual environment: `python -m venv .venv`
4. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/macOS)
5. Install dependencies: `pip install -r requirements.txt`

## Running Tests

```bash
# All tests
pytest -q

# Single test file
pytest tests/test_toc.py -q

# With coverage
pytest --cov=src
```

## Code Quality

```bash
# Format code
black .

# Lint
ruff check src --fix

# Type check
mypy src --ignore-missing-imports
```

## Pull Request Process

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Make changes and add tests
3. Run tests: `pytest -q`
4. Format code: `black .`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open Pull Request

## PR Template

- [ ] Tests pass
- [ ] Code formatted with Black
- [ ] New tests added for new features
- [ ] Documentation updated if needed