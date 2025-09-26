# Usage Examples

Comprehensive examples for all USB PD Parser functionality.

## Basic Usage Examples

### 1. Simple PDF Extraction

```python
from pathlib import Path
from src.pdf_extractor import PDFExtractor

# Extract first 10 pages
pdf_path = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
extractor = PDFExtractor(pdf_path)

# Get document title
title = extractor.get_doc_title()
print(f"Document: {title}")

# Extract pages
pages = extractor.extract_pages(max_pages=10)
print(f"Extracted {len(pages)} pages")

# Extract structured content
for item in extractor.extract_structured_content(max_pages=5):
    print(f"Page {item['page']}: {item['type']} - {item['content'][:50]}...")
```

### 2. TOC Extraction

```python
from src.toc_extractor import TOCExtractor

# Create TOC extractor
extractor = TOCExtractor("USB Power Delivery Specification")

# Extract from content
content = """
Table of Contents
1.1 Introduction ........................... 15
1.2 Overview .............................. 16
2.1 Technical Specifications .............. 25
"""

entries = extractor.extract_from_content(content)
for entry in entries:
    print(f"{entry.section_id}: {entry.title} (page {entry.page})")
```

### 3. Content Search

```python
from search_content import ContentSearcher

# Create searcher
searcher = ContentSearcher("outputs/usb_pd_spec.jsonl")

# Search for terms
matches = searcher.search("USB Power Delivery")
print(f"Found {len(matches)} matches")

# Display results
searcher.display_results("USB Power Delivery", max_results=5)

# Search in specific file
searcher = ContentSearcher("outputs/usb_pd_content.jsonl")
matches = searcher.search("voltage")
print(f"Found {len(matches)} voltage references")
```

## Advanced Usage Examples

### 4. Full Pipeline with Progress Tracking

```python
from src.pipeline_orchestrator import PipelineOrchestrator
from src.progress_tracker import StepTracker

# Set up progress tracking
steps = ["Initialize", "Extract TOC", "Extract Content", "Build Spec", "Save Results"]
tracker = StepTracker(steps, "USB PD Processing")

# Initialize pipeline
tracker.next_step("Initializing pipeline...")
orchestrator = PipelineOrchestrator("application.yml", debug=True)

# Run full pipeline with progress
tracker.next_step("Extracting TOC entries...")
tracker.next_step("Extracting content...")
tracker.next_step("Building specification...")
results = orchestrator.run_full_pipeline(mode=1)

tracker.next_step("Saving results...")
print(f"Completed! TOC: {results['toc_entries']}, Content: {results['content_items']}")
tracker.finish()
```

### 5. Async Processing

```python
import asyncio
from src.async_processor import AsyncProcessor
from pathlib import Path

async def process_multiple_pdfs():
    """Process multiple PDFs asynchronously."""
    
    def extract_from_pdf(pdf_path):
        from src.pdf_extractor import PDFExtractor
        extractor = PDFExtractor(pdf_path)
        return len(extractor.extract_pages(max_pages=10))
    
    # List of PDF files
    pdf_files = [
        Path("doc1.pdf"),
        Path("doc2.pdf"),
        Path("doc3.pdf")
    ]
    
    # Process asynchronously
    with AsyncProcessor(max_workers=3) as processor:
        results = await processor.process_files_async(extract_from_pdf, pdf_files)
    
    print(f"Processed {len(results)} files")
    return results

# Run async processing
results = asyncio.run(process_multiple_pdfs())
```

### 6. Custom Validation

```python
from pathlib import Path
from src.base import BaseValidator
import json

class CustomValidator(BaseValidator):
    """Custom validator for specific format."""
    
    def _validate_line(self, line: str, line_num: int) -> bool:
        if not line.strip():
            return True
        
        try:
            data = json.loads(line)
            # Custom validation rules
            required_fields = {"id", "content", "timestamp"}
            return all(field in data for field in required_fields)
        except json.JSONDecodeError:
            print(f"Line {line_num}: Invalid JSON")
            return False
    
    def _display_summary(self) -> None:
        print(f"Custom validation: {self.valid_count} valid, {self.error_count} errors")

# Use custom validator
validator = CustomValidator(Path("custom_output.jsonl"))
is_valid = validator.validate()
print(f"Validation result: {is_valid}")
```

### 7. Input Validation and Security

```python
from src.input_validator import InputValidator
from src.exceptions import InvalidInputError, PDFNotFoundError

def safe_pdf_processing(user_pdf_path: str, user_search_term: str):
    """Safely process user inputs."""
    
    try:
        # Validate PDF path
        safe_pdf_path = InputValidator.validate_pdf_path(user_pdf_path)
        print(f"PDF validated: {safe_pdf_path}")
        
        # Validate search term
        safe_search_term = InputValidator.validate_search_term(user_search_term)
        print(f"Search term sanitized: '{safe_search_term}'")
        
        # Validate page range
        start_page, end_page = InputValidator.validate_page_range(1, 100)
        print(f"Page range: {start_page}-{end_page}")
        
        # Sanitize output filename
        safe_filename = InputValidator.sanitize_filename("output<script>.jsonl")
        print(f"Safe filename: {safe_filename}")
        
        return safe_pdf_path, safe_search_term
        
    except PDFNotFoundError as e:
        print(f"PDF not found: {e}")
    except InvalidInputError as e:
        print(f"Invalid input: {e}")

# Example usage
safe_pdf_processing("../../../etc/passwd", "<script>alert('xss')</script>")
```

### 8. Progress Bars for Long Operations

```python
from src.progress_tracker import ProgressBar, with_progress
import time

def process_with_progress():
    """Demonstrate progress tracking."""
    
    # Manual progress bar
    items = list(range(100))
    with ProgressBar(len(items), "Processing items") as pbar:
        for item in items:
            # Simulate work
            time.sleep(0.01)
            pbar.update(1)
    
    # Automatic progress wrapper
    def slow_operation(item):
        time.sleep(0.01)
        return item * 2
    
    results = []
    for item in with_progress(range(50), "Auto progress"):
        result = slow_operation(item)
        results.append(result)
    
    print(f"Processed {len(results)} items")

process_with_progress()
```

## CLI Usage Examples

### 9. Command Line Interface

```bash
# Interactive mode (recommended for beginners)
python main.py

# Direct mode selection
python main.py --mode 1  # All pages
python main.py --mode 2  # 600 pages
python main.py --mode 3  # 200 pages

# Extract specific content
python main.py --toc-only
python main.py --content-only

# Debug mode
python main.py --debug --mode 1

# Custom configuration
python main.py --config custom.yml --mode 1
```

### 10. Search Operations

```bash
# Basic search
python search_content.py "USB"
python search_content.py "Power Delivery"
python search_content.py "voltage"

# Search in specific file
python search_content.py "connector" outputs/usb_pd_content.jsonl
python search_content.py "protocol" outputs/usb_pd_toc.jsonl

# Complex search terms
python search_content.py "USB Power Delivery Protocol"
```

### 11. Validation Tools

```bash
# Validate TOC output
python tools/validate_toc.py outputs/usb_pd_toc.jsonl

# Validate content output
python tools/validate_content.py outputs/usb_pd_content.jsonl

# Validate general JSONL
python tools/validate_output.py outputs/usb_pd_spec.jsonl

# Benchmark performance
python tools/benchmark.py "assets/USB_PD_R3_2 V1.1 2024-10.pdf"
```

## Integration Examples

### 12. Web API Integration

```python
from flask import Flask, request, jsonify
from src.pipeline_orchestrator import PipelineOrchestrator
from src.input_validator import InputValidator
import tempfile
import os

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_pdf():
    """API endpoint for PDF extraction."""
    
    try:
        # Get uploaded file
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file provided'}), 400
        
        pdf_file = request.files['pdf']
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf_file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            # Validate PDF
            safe_path = InputValidator.validate_pdf_path(tmp_path)
            
            # Process PDF
            orchestrator = PipelineOrchestrator()
            results = orchestrator.run_full_pipeline(mode=3)  # Memory-safe mode
            
            return jsonify({
                'success': True,
                'toc_entries': results['toc_entries'],
                'content_items': results['content_items'],
                'files': {
                    'toc': results['toc_path'],
                    'content': results['content_path'],
                    'spec': results['spec_path']
                }
            })
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search_content():
    """API endpoint for content search."""
    
    try:
        data = request.get_json()
        search_term = data.get('term', '')
        
        # Validate search term
        safe_term = InputValidator.validate_search_term(search_term)
        
        # Perform search
        from search_content import ContentSearcher
        searcher = ContentSearcher()
        matches = searcher.search(safe_term)
        
        return jsonify({
            'success': True,
            'term': safe_term,
            'matches': len(matches),
            'results': matches[:10]  # Return first 10 matches
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### 13. Database Integration

```python
import sqlite3
from src.models import TOCEntry
from search_content import ContentSearcher
import json

class DatabaseIntegration:
    """Integrate parser results with database."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._setup_database()
    
    def _setup_database(self):
        """Create database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # TOC entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS toc_entries (
                id INTEGER PRIMARY KEY,
                doc_title TEXT,
                section_id TEXT,
                title TEXT,
                page INTEGER,
                level INTEGER,
                parent_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Content items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_items (
                id INTEGER PRIMARY KEY,
                doc_title TEXT,
                content_type TEXT,
                content TEXT,
                page INTEGER,
                block_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def import_toc_entries(self, jsonl_file: str):
        """Import TOC entries from JSONL file."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    entry_data = json.loads(line)
                    entry = TOCEntry(**entry_data)
                    
                    cursor.execute('''
                        INSERT INTO toc_entries 
                        (doc_title, section_id, title, page, level, parent_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        entry.doc_title,
                        entry.section_id,
                        entry.title,
                        entry.page,
                        entry.level,
                        entry.parent_id
                    ))
        
        conn.commit()
        conn.close()
    
    def search_database(self, search_term: str) -> list:
        """Search content in database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM content_items 
            WHERE content LIKE ? 
            ORDER BY page, id
        ''', (f'%{search_term}%',))
        
        results = cursor.fetchall()
        conn.close()
        
        return results

# Usage example
db = DatabaseIntegration("usb_pd_parser.db")
db.import_toc_entries("outputs/usb_pd_toc.jsonl")
results = db.search_database("USB Power Delivery")
print(f"Found {len(results)} database matches")
```

### 14. Batch Processing

```python
from pathlib import Path
from src.pipeline_orchestrator import PipelineOrchestrator
from src.progress_tracker import ProgressBar
import json

def batch_process_pdfs(pdf_directory: str, output_directory: str):
    """Process multiple PDFs in batch."""
    
    pdf_dir = Path(pdf_directory)
    output_dir = Path(output_directory)
    output_dir.mkdir(exist_ok=True)
    
    # Find all PDF files
    pdf_files = list(pdf_dir.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")
    
    results = []
    
    with ProgressBar(len(pdf_files), "Processing PDFs") as pbar:
        for pdf_file in pdf_files:
            try:
                # Create output subdirectory
                pdf_output_dir = output_dir / pdf_file.stem
                pdf_output_dir.mkdir(exist_ok=True)
                
                # Update configuration for this PDF
                config_data = {
                    'pdf_input_file': str(pdf_file),
                    'output_directory': str(pdf_output_dir)
                }
                
                # Process PDF
                orchestrator = PipelineOrchestrator()
                result = orchestrator.run_full_pipeline(mode=3)  # Memory-safe
                
                # Store results
                results.append({
                    'pdf_file': str(pdf_file),
                    'output_dir': str(pdf_output_dir),
                    'toc_entries': result['toc_entries'],
                    'content_items': result['content_items'],
                    'success': True
                })
                
            except Exception as e:
                results.append({
                    'pdf_file': str(pdf_file),
                    'error': str(e),
                    'success': False
                })
            
            pbar.update(1)
    
    # Save batch results
    batch_results_file = output_dir / "batch_results.json"
    with open(batch_results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"\nBatch processing complete:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Results saved to: {batch_results_file}")
    
    return results

# Usage
results = batch_process_pdfs("input_pdfs/", "batch_output/")
```

### 15. Custom Output Formats

```python
import csv
import xml.etree.ElementTree as ET
from search_content import ContentSearcher
import json

class OutputFormatter:
    """Convert JSONL output to different formats."""
    
    def __init__(self, jsonl_file: str):
        self.jsonl_file = jsonl_file
    
    def to_csv(self, output_file: str):
        """Convert to CSV format."""
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['doc_title', 'section_id', 'title', 'page', 'level'])
            
            # Write data
            with open(self.jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        writer.writerow([
                            data.get('doc_title', ''),
                            data.get('section_id', ''),
                            data.get('title', ''),
                            data.get('page', ''),
                            data.get('level', '')
                        ])
    
    def to_xml(self, output_file: str):
        """Convert to XML format."""
        root = ET.Element('document')
        
        with open(self.jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    
                    entry = ET.SubElement(root, 'entry')
                    for key, value in data.items():
                        elem = ET.SubElement(entry, key)
                        elem.text = str(value)
        
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    def to_markdown(self, output_file: str):
        """Convert TOC to Markdown format."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Table of Contents\n\n")
            
            with open(self.jsonl_file, 'r', encoding='utf-8') as jsonl_f:
                for line in jsonl_f:
                    if line.strip():
                        data = json.loads(line)
                        level = data.get('level', 1)
                        title = data.get('title', '')
                        page = data.get('page', '')
                        
                        # Create markdown heading
                        heading = '#' * (level + 1)
                        f.write(f"{heading} {title} (Page {page})\n\n")

# Usage examples
formatter = OutputFormatter("outputs/usb_pd_toc.jsonl")
formatter.to_csv("outputs/toc.csv")
formatter.to_xml("outputs/toc.xml")
formatter.to_markdown("outputs/toc.md")
```

## Error Handling Examples

### 16. Comprehensive Error Handling

```python
from src.exceptions import *
from src.pipeline_orchestrator import PipelineOrchestrator
import logging

def robust_pdf_processing(pdf_path: str):
    """Demonstrate comprehensive error handling."""
    
    try:
        orchestrator = PipelineOrchestrator()
        results = orchestrator.run_full_pipeline(mode=1)
        return results
        
    except PDFNotFoundError as e:
        logging.error(f"PDF file not found: {e}")
        print("Please check the PDF file path in your configuration.")
        return None
        
    except InvalidInputError as e:
        logging.error(f"Invalid input: {e}")
        print("Please provide a valid PDF file.")
        return None
        
    except ProcessingTimeoutError as e:
        logging.error(f"Processing timeout: {e}")
        print("Processing took too long. Try using a smaller batch size (mode 3).")
        return None
        
    except MemoryLimitError as e:
        logging.error(f"Memory limit exceeded: {e}")
        print("Not enough memory. Try using mode 3 for memory-safe processing.")
        return None
        
    except ValidationError as e:
        logging.error(f"Validation failed: {e}")
        print("Output validation failed. Check the generated files.")
        return None
        
    except USBPDParserError as e:
        logging.error(f"Parser error: {e}")
        print(f"An error occurred during processing: {e}")
        return None
        
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")
        return None

# Usage with error handling
result = robust_pdf_processing("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
if result:
    print("Processing completed successfully!")
else:
    print("Processing failed. Check the logs for details.")
```

These examples demonstrate the full capabilities of the USB PD Parser with proper error handling, security considerations, and real-world integration scenarios.