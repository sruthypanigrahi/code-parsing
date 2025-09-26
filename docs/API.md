# API Reference

Complete API documentation for USB PD Specification Parser.

## Core Classes

### CLIInterface

Main command-line interface class.

```python
from src.app import CLIInterface

cli = CLIInterface()
cli.run()
```

#### Methods

##### `__init__()`
Initialize CLI interface with argument parser.

**Returns:** `None`

##### `run()`
Execute the CLI application with user arguments.

**Returns:** `None`  
**Raises:** `SystemExit` on error

---

### PipelineOrchestrator

Coordinates the complete PDF processing pipeline.

```python
from src.pipeline_orchestrator import PipelineOrchestrator

orchestrator = PipelineOrchestrator("config.yml", debug=True)
results = orchestrator.run_full_pipeline(mode=1)
```

#### Constructor

##### `__init__(config_path: str = "application.yml", debug: bool = False)`

**Parameters:**
- `config_path` (str): Path to configuration file
- `debug` (bool): Enable debug logging

#### Methods

##### `run_full_pipeline(mode: int = 1) -> Dict[str, Any]`
Run complete pipeline with TOC and content extraction.

**Parameters:**
- `mode` (int): Extraction mode (1=all pages, 2=600 pages, 3=200 pages)

**Returns:** `Dict[str, Any]` - Results with counts and file paths

**Example:**
```python
results = orchestrator.run_full_pipeline(mode=1)
print(f"TOC entries: {results['toc_entries']}")
print(f"Content items: {results['content_items']}")
```

##### `run_toc_only() -> List[TOCEntry]`
Extract only TOC entries.

**Returns:** `List[TOCEntry]` - List of TOC entries

##### `run_content_only() -> int`
Extract only content (paragraphs, images, tables).

**Returns:** `int` - Number of content items extracted

---

### PDFExtractor

Handles PDF content extraction with different modes.

```python
from src.pdf_extractor import PDFExtractor
from pathlib import Path

extractor = PDFExtractor(Path("document.pdf"))
pages = extractor.extract_pages(max_pages=10)
```

#### Constructor

##### `__init__(pdf_path: Path)`

**Parameters:**
- `pdf_path` (Path): Path to PDF file

**Raises:** `PDFNotFoundError` if file doesn't exist

#### Methods

##### `get_doc_title() -> str`
Extract document title from PDF metadata.

**Returns:** `str` - Document title or default

##### `extract_pages(max_pages: Optional[int] = None) -> List[str]`
Extract text from PDF pages.

**Parameters:**
- `max_pages` (Optional[int]): Maximum pages to extract (None for all)

**Returns:** `List[str]` - List of page text content

##### `extract_structured_content(max_pages: Optional[int] = None) -> Iterator[Dict[str, Any]]`
Extract structured content including paragraphs, images, and tables.

**Parameters:**
- `max_pages` (Optional[int]): Maximum pages to extract

**Returns:** `Iterator[Dict[str, Any]]` - Iterator of content items

**Content Item Structure:**
```python
{
    "type": "paragraph|image|table",
    "content": "text content or description",
    "page": 1,
    "block_id": "p1_0",
    "bbox": [x1, y1, x2, y2]
}
```

---

### TOCExtractor

Handles TOC extraction from PDF content.

```python
from src.toc_extractor import TOCExtractor

extractor = TOCExtractor("Document Title")
entries = extractor.extract_from_content(content)
```

#### Constructor

##### `__init__(doc_title: str)`

**Parameters:**
- `doc_title` (str): Document title for TOC entries

#### Methods

##### `extract_from_content(content: str) -> List[TOCEntry]`
Extract TOC entries from text content.

**Parameters:**
- `content` (str): Text content to parse

**Returns:** `List[TOCEntry]` - List of extracted TOC entries

---

### ContentSearcher

Search functionality for JSONL content files.

```python
from search_content import ContentSearcher

searcher = ContentSearcher("outputs/content.jsonl")
matches = searcher.search("USB Power Delivery")
searcher.display_results("USB Power Delivery")
```

#### Constructor

##### `__init__(jsonl_file: str = "outputs/usb_pd_spec.jsonl")`

**Parameters:**
- `jsonl_file` (str): Path to JSONL file to search

#### Methods

##### `search(search_term: str) -> List[Dict[str, Any]]`
Search for term in JSONL content.

**Parameters:**
- `search_term` (str): Text to search for

**Returns:** `List[Dict[str, Any]]` - List of matching items

##### `display_results(search_term: str, max_results: int = 10) -> None`
Display search results to console.

**Parameters:**
- `search_term` (str): Search term used
- `max_results` (int): Maximum results to display

---

### InputValidator

Validates user inputs for security and correctness.

```python
from src.input_validator import InputValidator

# Validate PDF file
pdf_path = InputValidator.validate_pdf_path("document.pdf")

# Validate search term
clean_term = InputValidator.validate_search_term("USB<script>")
```

#### Static Methods

##### `validate_pdf_path(pdf_path: Union[str, Path]) -> Path`
Validate PDF file path and properties.

**Parameters:**
- `pdf_path` (Union[str, Path]): Path to PDF file

**Returns:** `Path` - Validated path object

**Raises:** 
- `PDFNotFoundError` if file not found
- `InvalidInputError` if file invalid

##### `validate_search_term(search_term: str) -> str`
Validate and sanitize search term.

**Parameters:**
- `search_term` (str): Search term to validate

**Returns:** `str` - Sanitized search term

**Raises:** `InvalidInputError` if term invalid

##### `validate_page_range(start_page: int, end_page: Optional[int] = None) -> tuple`
Validate page range parameters.

**Parameters:**
- `start_page` (int): Starting page number
- `end_page` (Optional[int]): Ending page number

**Returns:** `tuple` - Validated page range

##### `sanitize_filename(filename: str) -> str`
Sanitize filename for safe file operations.

**Parameters:**
- `filename` (str): Filename to sanitize

**Returns:** `str` - Safe filename

---

### ProgressBar

Simple progress bar for console output.

```python
from src.progress_tracker import ProgressBar

with ProgressBar(100, "Processing") as pbar:
    for i in range(100):
        # Do work
        pbar.update(1)
```

#### Constructor

##### `__init__(total: int, description: str = "Processing", width: int = 50)`

**Parameters:**
- `total` (int): Total number of items
- `description` (str): Progress description
- `width` (int): Progress bar width

#### Methods

##### `update(increment: int = 1) -> None`
Update progress by increment.

##### `set_progress(value: int) -> None`
Set absolute progress value.

##### `finish() -> None`
Mark progress as complete.

---

### AsyncProcessor

Async processor for CPU and I/O bound tasks.

```python
from src.async_processor import AsyncProcessor
import asyncio

async def main():
    with AsyncProcessor(max_workers=4) as processor:
        results = await processor.process_batch_async(func, items)

asyncio.run(main())
```

#### Constructor

##### `__init__(max_workers: Optional[int] = None)`

**Parameters:**
- `max_workers` (Optional[int]): Maximum worker threads

#### Methods

##### `async process_batch_async(func: Callable, items: List, batch_size: int = 10) -> List`
Process items in batches asynchronously.

**Parameters:**
- `func` (Callable): Function to apply to each item
- `items` (List): Items to process
- `batch_size` (int): Batch size for processing

**Returns:** `List` - Processed results

---

## Data Models

### TOCEntry

Pydantic model for Table of Contents entries.

```python
from src.models import TOCEntry

entry = TOCEntry(
    doc_title="Document",
    section_id="1.1",
    title="Introduction",
    full_path="Introduction",
    page=15,
    level=1,
    parent_id=None,
    tags=[]
)
```

#### Fields

- `doc_title` (str): Document title
- `section_id` (str): Section identifier
- `title` (str): Section title
- `full_path` (str): Full hierarchical path
- `page` (int): Page number
- `level` (int): Hierarchy level
- `parent_id` (Optional[str]): Parent section ID
- `tags` (List[str]): Associated tags

---

## Exception Hierarchy

### Base Exceptions

- `USBPDParserError` - Base exception for all parser errors
- `PDFProcessingError` - PDF processing failures
- `TOCExtractionError` - TOC extraction failures
- `ContentProcessingError` - Content processing failures
- `ValidationError` - Data validation failures
- `ConfigurationError` - Configuration issues
- `PDFNotFoundError` - PDF file not found
- `InvalidInputError` - Invalid input data
- `ProcessingTimeoutError` - Processing timeout
- `MemoryLimitError` - Memory limit exceeded
- `OutputWriteError` - Output writing failure

### Usage Example

```python
from src.exceptions import PDFNotFoundError, InvalidInputError

try:
    extractor = PDFExtractor(Path("missing.pdf"))
except PDFNotFoundError as e:
    print(f"PDF not found: {e}")
except InvalidInputError as e:
    print(f"Invalid input: {e}")
```

---

## Configuration

### Configuration File Structure

```yaml
# Input PDF file path
pdf_input_file: "assets/USB_PD_R3_2 V1.1 2024-10.pdf"

# Output settings
output_directory: "outputs"
toc_file: "outputs/usb_pd_toc.jsonl"

# Processing options
ocr_fallback: true
max_pages: null

# Parser settings
parser:
  min_line_length: 5
  deduplicate: true
```

### Config Class

```python
from src.config import Config

config = Config("application.yml")
print(config.pdf_input_file)
print(config.output_directory)
```

---

## Protocols and Interfaces

### ExtractorProtocol

```python
from src.base import ExtractorProtocol

class MyExtractor:
    def extract_pages(self, max_pages: Optional[int] = None) -> List[str]:
        # Implementation
        pass
    
    def get_doc_title(self) -> str:
        # Implementation
        pass
```

### ValidatorProtocol

```python
from src.base import ValidatorProtocol

class MyValidator:
    def validate(self) -> bool:
        # Implementation
        pass
```

### SearcherProtocol

```python
from src.base import SearcherProtocol

class MySearcher:
    def search(self, search_term: str) -> List[Dict[str, Any]]:
        # Implementation
        pass
    
    def display_results(self, search_term: str, max_results: int = 10) -> None:
        # Implementation
        pass
```