# Troubleshooting Guide

Complete troubleshooting guide for USB PD Specification Parser.

## Common Issues and Solutions

### 1. Installation Issues

#### Problem: PyMuPDF Installation Fails
```bash
ERROR: Failed building wheel for PyMuPDF
```

**Solutions:**
```bash
# Option 1: Use pre-compiled wheel
pip install --upgrade pip
pip install PyMuPDF

# Option 2: Install system dependencies (Linux)
sudo apt-get install python3-dev
sudo apt-get install libmupdf-dev

# Option 3: Use conda (recommended)
conda install -c conda-forge pymupdf

# Option 4: Windows specific
pip install --upgrade setuptools wheel
pip install PyMuPDF
```

#### Problem: Permission Denied During Installation
```bash
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
```bash
# Use user installation
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. PDF Processing Issues

#### Problem: PDF Not Found Error
```
PDFNotFoundError: PDF not found: assets/document.pdf
```

**Solutions:**
```python
# Check file path
from pathlib import Path
pdf_path = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
print(f"File exists: {pdf_path.exists()}")
print(f"Absolute path: {pdf_path.absolute()}")

# Update configuration
# Edit application.yml
pdf_input_file: "assets/your-actual-file.pdf"
```

#### Problem: Invalid PDF File
```
InvalidInputError: File is not a valid PDF
```

**Solutions:**
```python
# Verify PDF file
with open("document.pdf", "rb") as f:
    header = f.read(4)
    print(f"File header: {header}")  # Should be b'%PDF'

# Check file size
import os
size = os.path.getsize("document.pdf")
print(f"File size: {size} bytes")

# Try with different PDF
# Ensure PDF is not corrupted or password-protected
```

#### Problem: Memory Issues with Large PDFs
```
MemoryError: Unable to allocate memory
```

**Solutions:**
```bash
# Use memory-safe mode
python main.py --mode 3  # Process only 200 pages

# Or process in smaller batches
python main.py --mode 2  # Process 600 pages

# Monitor memory usage
python -m memory_profiler main.py --mode 3
```

### 3. Extraction Issues

#### Problem: No TOC Entries Found
```
Extracted 0 TOC entries
```

**Solutions:**
```python
# Debug TOC extraction
from src.toc_extractor import TOCExtractor
from src.pdf_extractor import PDFExtractor

# Check PDF content
extractor = PDFExtractor(Path("document.pdf"))
pages = extractor.extract_pages(max_pages=20)

# Look for TOC patterns
for i, page in enumerate(pages):
    if "contents" in page.lower() or "table of contents" in page.lower():
        print(f"TOC found on page {i+1}")
        print(page[:500])  # First 500 characters

# Manual TOC extraction
toc_extractor = TOCExtractor("Document Title")
entries = toc_extractor.extract_from_content(pages[12])  # Adjust page number
print(f"Found {len(entries)} entries")
```

#### Problem: No Images Found
```
Images: 0
```

**Solutions:**
```python
# Images are often in later pages
python main.py --mode 1  # Extract all pages

# Check image detection settings
from src.pdf_extractor import PDFExtractor

extractor = PDFExtractor(Path("document.pdf"))
for item in extractor.extract_structured_content(max_pages=1047):
    if item['type'] == 'image':
        print(f"Image found on page {item['page']}: {item['content']}")
        break
```

#### Problem: Poor Table Detection
```
Tables: 0 or very few tables detected
```

**Solutions:**
```python
# Tables require specific patterns
# Check if PDF has proper table formatting

# Try with pdfplumber for better table detection
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page_num, page in enumerate(pdf.pages[:10]):
        tables = page.extract_tables()
        if tables:
            print(f"Page {page_num + 1}: {len(tables)} tables found")
```

### 4. Performance Issues

#### Problem: Very Slow Processing
```
Processing takes hours for large PDFs
```

**Solutions:**
```python
# Enable async processing
from src.async_processor import AsyncProcessor
import asyncio

async def fast_processing():
    with AsyncProcessor(max_workers=4) as processor:
        # Use async capabilities
        pass

# Use progress tracking to monitor
from src.progress_tracker import ProgressBar

with ProgressBar(total_pages, "Processing") as pbar:
    # Process with progress updates
    pass

# Profile performance
python -m cProfile main.py --mode 3 > profile.txt
```

#### Problem: High Memory Usage
```
Process killed due to memory usage
```

**Solutions:**
```bash
# Use smaller batch sizes
python main.py --mode 3

# Monitor memory
import psutil
import os

process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB")

# Use generators instead of lists
def process_pages_generator(pdf_path):
    # Yield pages one at a time instead of loading all
    pass
```

### 5. Output Issues

#### Problem: Empty Output Files
```
Generated files are empty or have no content
```

**Solutions:**
```python
# Check extraction results
results = orchestrator.run_full_pipeline(mode=1)
print(f"Results: {results}")

# Verify file creation
from pathlib import Path
output_files = [
    "outputs/usb_pd_toc.jsonl",
    "outputs/usb_pd_content.jsonl", 
    "outputs/usb_pd_spec.jsonl"
]

for file_path in output_files:
    path = Path(file_path)
    if path.exists():
        size = path.stat().st_size
        print(f"{file_path}: {size} bytes")
    else:
        print(f"{file_path}: NOT FOUND")
```

#### Problem: Invalid JSON in Output
```
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solutions:**
```python
# Validate output files
from tools.validate_output import OutputValidator

validator = OutputValidator(Path("outputs/usb_pd_toc.jsonl"))
is_valid = validator.validate()

# Check for encoding issues
with open("outputs/usb_pd_toc.jsonl", "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        if line.strip():
            try:
                import json
                json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: {e}")
                print(f"Content: {line[:100]}")
```

### 6. Search Issues

#### Problem: Search Returns No Results
```
Found 0 matches for 'USB'
```

**Solutions:**
```python
# Check if files exist and have content
from pathlib import Path

search_file = Path("outputs/usb_pd_spec.jsonl")
if search_file.exists():
    with open(search_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        print(f"File has {len(lines)} lines")
        
        # Check first few lines
        for i, line in enumerate(lines[:3]):
            print(f"Line {i+1}: {line[:100]}")
else:
    print("Search file does not exist")

# Try case-insensitive search
from search_content import ContentSearcher
searcher = ContentSearcher("outputs/usb_pd_spec.jsonl")
matches = searcher.search("usb")  # lowercase
print(f"Found {len(matches)} matches")
```

#### Problem: Search is Very Slow
```
Search takes a long time for large files
```

**Solutions:**
```python
# Index content for faster search
import sqlite3
import json

def create_search_index(jsonl_file):
    conn = sqlite3.connect("search_index.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS content_fts 
        USING fts5(content, page, type)
    ''')
    
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                cursor.execute(
                    "INSERT INTO content_fts VALUES (?, ?, ?)",
                    (data.get("content", ""), data.get("page", ""), data.get("type", ""))
                )
    
    conn.commit()
    conn.close()

# Use indexed search
create_search_index("outputs/usb_pd_spec.jsonl")
```

### 7. Configuration Issues

#### Problem: Configuration File Not Found
```
FileNotFoundError: application.yml not found
```

**Solutions:**
```bash
# Copy example configuration
cp application.example.yml application.yml

# Or specify custom config
python main.py --config custom.yml

# Check current directory
ls -la *.yml
```

#### Problem: Invalid Configuration Format
```
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Solutions:**
```yaml
# Check YAML syntax
# Correct format:
pdf_input_file: "assets/document.pdf"
output_directory: "outputs"

# Incorrect format (missing quotes):
pdf_input_file: assets/document.pdf with spaces

# Validate YAML online or with:
python -c "import yaml; yaml.safe_load(open('application.yml'))"
```

### 8. Type Checking Issues

#### Problem: MyPy Type Errors
```
error: Argument 1 to "function" has incompatible type
```

**Solutions:**
```python
# Add proper type annotations
from typing import Optional, List, Dict, Any

def function(param: str) -> Optional[str]:
    return param if param else None

# Use type: ignore for external libraries
import fitz  # type: ignore

# Check MyPy configuration
# pyproject.toml
[tool.mypy]
ignore_missing_imports = true
```

### 9. Async Issues

#### Problem: Async Functions Not Working
```
RuntimeError: asyncio.run() cannot be called from a running event loop
```

**Solutions:**
```python
# Use proper async context
import asyncio

# Correct way
async def main():
    # Async code here
    pass

if __name__ == "__main__":
    asyncio.run(main())

# In Jupyter notebooks
import nest_asyncio
nest_asyncio.apply()

# Check if already in event loop
try:
    loop = asyncio.get_running_loop()
    print("Already in event loop")
except RuntimeError:
    print("No event loop running")
```

### 10. Testing Issues

#### Problem: Tests Fail with Import Errors
```
ModuleNotFoundError: No module named 'src'
```

**Solutions:**
```bash
# Run tests from project root
cd /path/to/usb-pd-parser
python -m pytest tests/

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/usb-pd-parser"

# Install in development mode
pip install -e .
```

#### Problem: Async Tests Fail
```
RuntimeError: no running event loop
```

**Solutions:**
```python
# Install pytest-asyncio
pip install pytest-asyncio

# Mark async tests
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

## Debugging Techniques

### 1. Enable Debug Logging

```python
import logging

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Or use CLI debug flag
python main.py --debug --mode 1
```

### 2. Step-by-Step Debugging

```python
# Debug PDF extraction
from src.pdf_extractor import PDFExtractor
from pathlib import Path

pdf_path = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
print(f"1. PDF exists: {pdf_path.exists()}")

extractor = PDFExtractor(pdf_path)
print(f"2. Extractor created successfully")

title = extractor.get_doc_title()
print(f"3. Document title: {title}")

pages = extractor.extract_pages(max_pages=5)
print(f"4. Extracted {len(pages)} pages")

for i, page in enumerate(pages):
    print(f"   Page {i+1}: {len(page)} characters")
```

### 3. Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler main.py --mode 3

# Line-by-line profiling
@profile
def memory_intensive_function():
    # Function code
    pass
```

### 4. Performance Profiling

```bash
# Profile with cProfile
python -m cProfile -o profile.prof main.py --mode 3

# Analyze profile
python -c "
import pstats
p = pstats.Stats('profile.prof')
p.sort_stats('cumulative').print_stats(10)
"
```

### 5. Interactive Debugging

```python
# Add breakpoints
import pdb

def problematic_function():
    pdb.set_trace()  # Debugger will stop here
    # Code to debug
    pass

# Or use ipdb for better interface
import ipdb
ipdb.set_trace()
```

## Getting Help

### 1. Check Logs

```bash
# Check application logs
tail -f outputs/parser.log

# Check system logs (Linux)
journalctl -f

# Windows Event Viewer
# Look for Python application errors
```

### 2. Collect System Information

```python
import sys
import platform
import pkg_resources

print(f"Python version: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Architecture: {platform.architecture()}")

# Check installed packages
installed_packages = [d for d in pkg_resources.working_set]
for package in sorted(installed_packages, key=lambda x: x.project_name):
    print(f"{package.project_name}: {package.version}")
```

### 3. Create Minimal Reproduction

```python
# Create minimal example that reproduces the issue
from pathlib import Path
from src.pdf_extractor import PDFExtractor

try:
    # Minimal reproduction code
    extractor = PDFExtractor(Path("test.pdf"))
    pages = extractor.extract_pages(max_pages=1)
    print(f"Success: {len(pages)} pages")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

### 4. Report Issues

When reporting issues, include:

1. **Environment Information**
   - Operating system and version
   - Python version
   - Package versions

2. **Error Details**
   - Complete error message
   - Stack trace
   - Steps to reproduce

3. **Configuration**
   - Configuration file contents
   - Command line arguments used

4. **Sample Data**
   - PDF file characteristics (if possible to share)
   - Expected vs actual output

### 5. Community Resources

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check latest documentation
- **Examples**: Review usage examples
- **Stack Overflow**: Search for similar issues

## Prevention Tips

1. **Always use virtual environments**
2. **Keep dependencies updated**
3. **Validate inputs before processing**
4. **Use appropriate batch sizes for your system**
5. **Monitor memory usage for large files**
6. **Enable logging for production use**
7. **Test with sample files before processing important documents**
8. **Backup important data before processing**