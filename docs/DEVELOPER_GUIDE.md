# Developer Guide

Complete guide for developers working on USB PD Specification Parser.

## Quick Start for Developers

```bash
# Clone and setup development environment
git clone https://github.com/username/usb-pd-parser.git
cd usb-pd-parser
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install all dependencies (including dev and async)
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-async.txt

# Run quality checks
black . && ruff check . && mypy src --ignore-missing-imports

# Run comprehensive tests
pytest tests/ -v --cov=src --cov-report=html
```

## Architecture Overview

### Core Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLIInterface  │───▶│PipelineOrchest- │───▶│   PDFExtractor  │
│                 │    │      rator      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  TOCExtractor   │◀───│  TOCPipeline    │    │ContentPipeline  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  SpecBuilder    │◀───│ContentProcessor │    │ContentSearcher  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow

1. **Input**: PDF file + Configuration
2. **Processing**: TOC extraction → Content extraction → Processing
3. **Output**: JSONL files (TOC, Content, Spec)
4. **Search**: ContentSearcher queries processed data

## Development Workflow

### 1. Adding New Features

```python
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Implement with proper OOP
class NewFeature:
    def __init__(self, config: Config):
        self.config = config
    
    def process(self) -> Any:
        # Implementation with error handling
        try:
            result = self._do_work()
            return result
        except Exception as e:
            raise NewFeatureError(f"Processing failed: {e}") from e
    
    def _do_work(self) -> Any:
        # Private implementation
        pass

# 3. Add comprehensive tests
class TestNewFeature:
    def test_feature_success(self):
        feature = NewFeature(mock_config)
        result = feature.process()
        assert result is not None
    
    def test_feature_error_handling(self):
        with pytest.raises(NewFeatureError):
            feature = NewFeature(invalid_config)
            feature.process()

# 4. Update documentation
# - Add to API.md
# - Update README.md
# - Add usage examples
```

### 2. Code Quality Standards

#### Type Annotations
```python
# ✅ Good - Comprehensive typing
def process_content(
    items: List[Dict[str, Any]], 
    max_items: Optional[int] = None
) -> Iterator[ProcessedItem]:
    for item in items[:max_items]:
        yield ProcessedItem.from_dict(item)

# ❌ Bad - Missing types
def process_content(items, max_items=None):
    for item in items[:max_items]:
        yield item
```

#### Error Handling
```python
# ✅ Good - Specific exceptions
try:
    result = risky_operation()
except FileNotFoundError as e:
    raise PDFNotFoundError(f"PDF file missing: {e}") from e
except PermissionError as e:
    raise InvalidInputError(f"Cannot access file: {e}") from e

# ❌ Bad - Bare except
try:
    result = risky_operation()
except:
    pass
```

#### Class Design
```python
# ✅ Good - Proper OOP with protocols
class ContentProcessor(BaseProcessor):
    def __init__(self, config: Config):
        super().__init__(config)
        self._cache: Dict[str, Any] = {}
    
    def process(self, content: str) -> ProcessedContent:
        if content in self._cache:
            return self._cache[content]
        
        result = self._do_process(content)
        self._cache[content] = result
        return result
    
    def _do_process(self, content: str) -> ProcessedContent:
        # Private implementation
        pass

# ❌ Bad - Procedural approach
def process_content(content, config):
    # Global state and no encapsulation
    pass
```

### 3. Testing Guidelines

#### Test Structure
```python
class TestFeatureName:
    """Test suite for FeatureName class."""
    
    @pytest.fixture
    def feature(self):
        """Create feature instance for testing."""
        return FeatureName(mock_config)
    
    def test_happy_path(self, feature):
        """Test normal operation."""
        result = feature.process("valid input")
        assert result.is_valid()
    
    def test_edge_cases(self, feature):
        """Test edge cases."""
        # Empty input
        result = feature.process("")
        assert result.is_empty()
        
        # Large input
        large_input = "x" * 10000
        result = feature.process(large_input)
        assert result.is_valid()
    
    def test_error_conditions(self, feature):
        """Test error handling."""
        with pytest.raises(InvalidInputError):
            feature.process(None)
    
    @pytest.mark.asyncio
    async def test_async_operation(self, feature):
        """Test async functionality."""
        result = await feature.process_async("input")
        assert result is not None
```

#### Coverage Requirements
- **Minimum**: 90% line coverage
- **Target**: 95% line coverage
- **Include**: Edge cases, error conditions, async operations

### 4. Performance Guidelines

#### Async Processing
```python
# ✅ Good - Async for I/O bound operations
async def process_files_async(file_paths: List[Path]) -> List[Result]:
    with AsyncProcessor(max_workers=4) as processor:
        return await processor.process_files_async(
            process_single_file, file_paths
        )

# ✅ Good - Progress tracking for long operations
def process_large_dataset(items: List[Any]) -> List[Result]:
    results = []
    with ProgressBar(len(items), "Processing items") as pbar:
        for item in items:
            result = process_item(item)
            results.append(result)
            pbar.update(1)
    return results
```

#### Memory Management
```python
# ✅ Good - Generator for large datasets
def process_pages(pdf_path: Path) -> Iterator[ProcessedPage]:
    with PDFExtractor(pdf_path) as extractor:
        for page in extractor.extract_pages():
            yield process_page(page)

# ❌ Bad - Loading everything into memory
def process_pages(pdf_path: Path) -> List[ProcessedPage]:
    extractor = PDFExtractor(pdf_path)
    all_pages = extractor.extract_pages()  # Memory intensive
    return [process_page(page) for page in all_pages]
```

### 5. Security Guidelines

#### Input Validation
```python
# ✅ Good - Comprehensive validation
def process_user_input(user_input: str) -> str:
    # Validate input
    validated = InputValidator.validate_search_term(user_input)
    
    # Sanitize for safety
    sanitized = InputValidator.sanitize_filename(validated)
    
    return sanitized

# ✅ Good - File validation
def load_pdf(pdf_path: str) -> PDFExtractor:
    # Validate path and file
    safe_path = InputValidator.validate_pdf_path(pdf_path)
    
    return PDFExtractor(safe_path)
```

## Adding New Components

### 1. New Extractor Class

```python
# 1. Define protocol compliance
class NewExtractor(BaseExtractor):
    def __init__(self, config: Config):
        super().__init__(config)
        self._setup_extractor()
    
    def extract(self, source: Any) -> Iterator[ExtractedItem]:
        # Implement extraction logic
        pass
    
    def _setup_extractor(self) -> None:
        # Private setup logic
        pass

# 2. Add comprehensive tests
class TestNewExtractor:
    def test_extraction_success(self):
        extractor = NewExtractor(mock_config)
        items = list(extractor.extract(mock_source))
        assert len(items) > 0
    
    def test_extraction_empty_source(self):
        extractor = NewExtractor(mock_config)
        items = list(extractor.extract(empty_source))
        assert len(items) == 0

# 3. Update documentation
# - Add to API.md
# - Update architecture diagrams
# - Add usage examples
```

### 2. New Validator Class

```python
# 1. Inherit from BaseValidator
class NewValidator(BaseValidator):
    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.custom_rules = self._load_rules()
    
    def _validate_line(self, line: str, line_num: int) -> bool:
        # Custom validation logic
        return self._check_custom_rules(line)
    
    def _display_summary(self) -> None:
        print(f"Custom validation: {self.valid_count} valid, {self.error_count} errors")
    
    def _check_custom_rules(self, line: str) -> bool:
        # Implementation
        pass

# 2. Add to validation tools
# tools/validate_new_format.py
```

## Debugging and Troubleshooting

### 1. Enable Debug Logging

```python
# Enable debug mode
python main.py --debug --mode 1

# Or programmatically
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Performance Profiling

```python
# Use built-in performance monitoring
from src.performance import timer, monitor

@timer
def slow_function():
    # Function implementation
    pass

# Check metrics
monitor.report()
```

### 3. Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler main.py --mode 3
```

### 4. Async Debugging

```python
# Enable async debugging
import asyncio
asyncio.get_event_loop().set_debug(True)

# Use async timer
from src.async_processor import async_timer

@async_timer
async def async_function():
    # Async implementation
    pass
```

## Release Process

### 1. Version Management

```bash
# Update version in setup.py, __init__.py
# Update CHANGELOG.md with new features
# Create release branch
git checkout -b release/v1.1.0

# Run full test suite
pytest tests/ -v --cov=src --cov-report=html

# Build and test package
python setup.py sdist bdist_wheel
```

### 2. Documentation Updates

```bash
# Update all documentation
# - README.md
# - API.md
# - DEVELOPER_GUIDE.md
# - CHANGELOG.md

# Generate API docs
python scripts/generate_docs.py

# Verify documentation
python scripts/verify_docs.py
```

### 3. Quality Checks

```bash
# Run all quality checks
black . && ruff check . && mypy src --ignore-missing-imports

# Security scan
bandit -r src/

# Dependency check
safety check

# Performance benchmark
python tools/benchmark.py assets/USB_PD_R3_2\ V1.1\ 2024-10.pdf
```

## Contributing Guidelines

### 1. Code Review Checklist

- [ ] Follows OOP principles with proper encapsulation
- [ ] Comprehensive type annotations
- [ ] Proper error handling with specific exceptions
- [ ] Input validation and sanitization
- [ ] Comprehensive tests (>90% coverage)
- [ ] Documentation updated
- [ ] Performance considerations addressed
- [ ] Security implications reviewed

### 2. Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Documentation
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] CHANGELOG updated

## Performance
- [ ] Performance impact assessed
- [ ] Memory usage considered
- [ ] Async capabilities utilized where appropriate
```

### 3. Issue Templates

```markdown
## Bug Report
**Description:** Clear description of the bug
**Steps to Reproduce:** 1. 2. 3.
**Expected Behavior:** What should happen
**Actual Behavior:** What actually happens
**Environment:** OS, Python version, dependencies

## Feature Request
**Description:** Clear description of the feature
**Use Case:** Why is this feature needed
**Proposed Solution:** How should it work
**Alternatives:** Other solutions considered
```

## Best Practices Summary

1. **OOP First**: Use classes and proper encapsulation
2. **Type Everything**: Comprehensive type annotations
3. **Test Thoroughly**: >90% coverage with edge cases
4. **Handle Errors**: Specific exceptions with proper handling
5. **Validate Input**: Security-first approach
6. **Document Everything**: Keep docs current with code
7. **Performance Matters**: Use async and progress tracking
8. **Security Always**: Validate, sanitize, protect