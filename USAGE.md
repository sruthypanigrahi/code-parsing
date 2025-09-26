# Usage Guide

## Command Line Interface

### Basic Usage

```bash
# Extract all content (recommended)
python main.py --mode 1

# Extract first 600 pages (balanced)
python main.py --mode 2

# Extract first 200 pages (memory-safe)
python main.py --mode 3

# Interactive mode (prompts for choice)
python main.py
```

### Extraction Options

```bash
# Extract only Table of Contents
python main.py --toc-only

# Extract only content (paragraphs, images, tables)
python main.py --content-only

# Enable debug logging
python main.py --debug --mode 1

# Use custom config file
python main.py --config my-config.yml --mode 1
```

### Search Content

```bash
# Search all content
python search_content.py "USB"
python search_content.py "Power Delivery"
python search_content.py "voltage"

# Search specific file
python search_content.py "connector" outputs/usb_pd_content.jsonl
python search_content.py "table" outputs/usb_pd_toc.jsonl
```

## Python API Usage

### Basic PDF Extraction

```python
from src.pipeline_orchestrator import PipelineOrchestrator

# Initialize orchestrator
orchestrator = PipelineOrchestrator("application.yml")

# Run full pipeline
results = orchestrator.run_full_pipeline(mode=1)
print(f"Extracted {results['content_items']} content items")
print(f"Found {results['toc_entries']} TOC entries")
```

### Extract Specific Content

```python
# Extract only TOC
toc_entries = orchestrator.run_toc_only()
for entry in toc_entries[:5]:
    print(f"{entry.title} (Page {entry.page})")

# Extract only content
content_count = orchestrator.run_content_only()
print(f"Extracted {content_count} content items")
```

### Direct PDF Processing

```python
from src.pdf_extractor import PDFExtractor
from pathlib import Path

# Initialize extractor
pdf_path = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
extractor = PDFExtractor(pdf_path)

# Extract pages as text
pages = extractor.extract_pages(max_pages=10)
print(f"Extracted {len(pages)} pages")

# Extract structured content
for item in extractor.extract_structured_content(max_pages=5):
    print(f"{item['type']}: {item['content'][:50]}...")
```

### Content Search

```python
from search_content import ContentSearcher

# Initialize searcher
searcher = ContentSearcher("outputs/usb_pd_spec.jsonl")

# Search for content
matches = searcher.search("USB Power Delivery")
print(f"Found {len(matches)} matches")

# Display results
searcher.display_results("USB Power Delivery")
```

### Configuration

```python
from src.config import Config

# Load configuration
config = Config("application.yml")
print(f"PDF file: {config.pdf_input_file}")
print(f"Output directory: {config.output_directory}")

# Access parser settings
print(f"Min line length: {config.parser['min_line_length']}")
```

## Output Formats

### TOC Output (`usb_pd_toc.jsonl`)

```json
{
  "doc_title": "USB_PD_R3_2 V1.1 2024-10.pdf",
  "section_id": "S1",
  "title": "Overview",
  "full_path": "Overview",
  "page": 34,
  "level": 1,
  "parent_id": null,
  "tags": []
}
```

### Content Output (`usb_pd_content.jsonl`)

```json
{
  "doc_title": "USB_PD_R3_2 V1.1 2024-10.pdf",
  "content_id": "C1",
  "type": "paragraph",
  "content": "Universal Serial Bus",
  "page": 1,
  "block_id": "p1_0",
  "bbox": [171.33, 62.91, 423.95, 95.74],
  "metadata": {
    "extracted_at": "2025-09-27T01:28:59.335084",
    "content_length": 20
  }
}
```

### Image Content

```json
{
  "content_id": "C2",
  "type": "image",
  "content": "[Image 469x72 on page 1032]",
  "page": 1032,
  "block_id": "img1032_8",
  "bbox": [71.74, 260.98, 540.26, 332.54]
}
```

### Table Content

```json
{
  "content_id": "C3",
  "type": "table",
  "content": "Table 2.1 Fixed Supply Power Ranges...",
  "page": 27,
  "block_id": "tbl27_0",
  "bbox": []
}
```

## Configuration Options

### Basic Configuration (`application.yml`)

```yaml
# Input PDF file path
pdf_input_file: "assets/USB_PD_R3_2 V1.1 2024-10.pdf"

# Output settings
output_directory: "outputs"
toc_file: "outputs/usb_pd_spec.jsonl"

# Processing options
ocr_fallback: true        # Enable OCR for scanned PDFs
max_pages: null          # Process all pages (or set limit)

# Parser settings
parser:
  min_line_length: 5     # Minimum line length for TOC parsing
  deduplicate: true      # Remove duplicate entries
```

### Advanced Configuration

```yaml
# Logging settings
logging:
  level: "INFO"          # DEBUG, INFO, WARNING, ERROR
  file: "outputs/parser.log"

# Performance settings
performance:
  batch_size: 100        # Items per batch
  max_workers: 4         # Parallel workers
  memory_limit: "2GB"    # Memory limit

# Content extraction settings
content:
  min_image_size: 100    # Minimum image size (pixels)
  extract_tables: true   # Extract table content
  extract_images: true   # Extract image descriptions
```

## Performance Tips

### Memory Management

```bash
# For large PDFs (>1000 pages)
python main.py --mode 2  # 600 pages

# For memory-constrained systems
python main.py --mode 3  # 200 pages

# Monitor memory usage
python main.py --debug --mode 1
```

### Parallel Processing

```python
from src.parallel import parallel_map_io

# Process multiple files
pdf_files = ["file1.pdf", "file2.pdf", "file3.pdf"]
results = parallel_map_io(process_pdf, pdf_files, workers=4)
```

### Async Processing

```python
import asyncio
from src.async_processor import AsyncProcessor

async def process_multiple():
    async with AsyncProcessor(max_workers=4) as processor:
        results = await processor.process_batch_async(func, items)
    return results

# Run async processing
results = asyncio.run(process_multiple())
```

## Error Handling

### Common Errors

```python
from src.exceptions import PDFNotFoundError, USBPDParserError

try:
    orchestrator = PipelineOrchestrator("application.yml")
    results = orchestrator.run_full_pipeline(mode=1)
except PDFNotFoundError as e:
    print(f"PDF file not found: {e}")
except USBPDParserError as e:
    print(f"Parser error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Validation

```python
from tools.validate_content import ContentValidator
from pathlib import Path

# Validate output files
validator = ContentValidator(Path("outputs/usb_pd_content.jsonl"))
is_valid = validator.validate()

if not is_valid:
    print("Validation failed - check output files")
```

## Integration Examples

### Jupyter Notebook

```python
# Install in notebook
!pip install -r requirements.txt

# Import and use
from src.pipeline_orchestrator import PipelineOrchestrator
orchestrator = PipelineOrchestrator()
results = orchestrator.run_full_pipeline(mode=3)  # Small batch for notebook

# Display results
import pandas as pd
df = pd.read_json("outputs/usb_pd_content.jsonl", lines=True)
df.head()
```

### Web API Integration

```python
from flask import Flask, jsonify
from src.pipeline_orchestrator import PipelineOrchestrator

app = Flask(__name__)

@app.route('/extract/<int:mode>')
def extract_pdf(mode):
    orchestrator = PipelineOrchestrator()
    results = orchestrator.run_full_pipeline(mode=mode)
    return jsonify(results)

@app.route('/search/<term>')
def search_content(term):
    searcher = ContentSearcher("outputs/usb_pd_spec.jsonl")
    matches = searcher.search(term)
    return jsonify({"matches": len(matches), "results": matches[:10]})
```

### Database Integration

```python
import sqlite3
import json

# Store results in database
def store_results(jsonl_file, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id TEXT PRIMARY KEY,
            type TEXT,
            content TEXT,
            page INTEGER,
            metadata TEXT
        )
    ''')
    
    # Insert data
    with open(jsonl_file) as f:
        for line in f:
            item = json.loads(line)
            cursor.execute('''
                INSERT OR REPLACE INTO content 
                (id, type, content, page, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                item['content_id'],
                item['type'],
                item['content'],
                item['page'],
                json.dumps(item.get('metadata', {}))
            ))
    
    conn.commit()
    conn.close()

# Usage
store_results("outputs/usb_pd_content.jsonl", "usb_pd.db")
```