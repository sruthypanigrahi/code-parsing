# Content Search Guide

## Overview

The USB PD Parser includes built-in search functionality to find specific terms and content within extracted PDF documents. This guide covers all search capabilities and usage patterns.

## Quick Start

```bash
# Basic search
python src/search_content.py "USB"

# Search in specific file
python src/search_content.py "Power Delivery" outputs/custom.jsonl

# Case-sensitive search
python src/search_content.py "USB" --case-sensitive
```

## Search Functionality

### Basic Search
```bash
python src/search_content.py "search_term"
```

### Advanced Search Options
```bash
# Search specific file
python src/search_content.py "term" path/to/file.jsonl

# Case-sensitive search
python src/search_content.py "Term" --case-sensitive

# Search with context (show surrounding text)
python src/search_content.py "term" --context 50
```

## Search Examples

### Common Use Cases

1. **Find USB specifications**:
   ```bash
   python src/search_content.py "USB"
   ```

2. **Search for power requirements**:
   ```bash
   python src/search_content.py "power"
   ```

3. **Find voltage specifications**:
   ```bash
   python src/search_content.py "voltage"
   ```

4. **Search for table references**:
   ```bash
   python src/search_content.py "Table"
   ```

### Output Format

Search results show:
- **Page number** where term was found
- **Context** surrounding the search term
- **Match count** per page
- **Total matches** across document

Example output:
```
Found 'USB' on page 1: Universal Serial Bus Power Delivery Specification
Found 'USB' on page 5: USB Type-C connector specifications
Found 'USB' on page 12: USB PD protocol implementation

Total matches: 247 across 156 pages
```

## Integration with Extraction

### Complete Workflow

1. **Extract PDF content**:
   ```bash
   python main.py --input "document.pdf" --output "extracted.jsonl"
   ```

2. **Search extracted content**:
   ```bash
   python src/search_content.py "search_term" extracted.jsonl
   ```

### Batch Processing

```bash
# Extract multiple documents
for pdf in assets/*.pdf; do
    python main.py --input "$pdf" --output "outputs/$(basename "$pdf" .pdf).jsonl"
done

# Search all extracted files
for jsonl in outputs/*.jsonl; do
    echo "Searching in $jsonl:"
    python src/search_content.py "USB" "$jsonl"
done
```

## Performance

- **Fast Search**: Optimized for large documents (1000+ pages)
- **Memory Efficient**: Streams through JSONL files
- **Regex Support**: Advanced pattern matching capabilities
- **Unicode Support**: Handles international characters

## Troubleshooting

### Common Issues

1. **File not found**: Ensure JSONL file exists and path is correct
2. **No matches**: Try case-insensitive search or broader terms
3. **Large output**: Use `--limit` to restrict number of results

### Error Messages

- `FileNotFoundError`: Check file path and ensure extraction completed
- `JSONDecodeError`: Verify JSONL file format is valid
- `UnicodeError`: Use UTF-8 encoding for international content

## API Reference

### search_content.py

```python
def search_content(
    search_term: str,
    jsonl_file: str = "outputs/usb_pd_spec.jsonl",
    case_sensitive: bool = False,
    context_chars: int = 100
) -> List[SearchResult]
```

**Parameters**:
- `search_term`: Text to search for
- `jsonl_file`: Path to extracted JSONL file
- `case_sensitive`: Enable case-sensitive matching
- `context_chars`: Characters to show around matches

**Returns**: List of search results with page numbers and context

## Recent Improvements

- ✅ Enhanced search performance for large documents
- ✅ Added context display around matches
- ✅ Improved Unicode and special character handling
- ✅ Added batch search capabilities
- ✅ Integrated with main extraction pipeline