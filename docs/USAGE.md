# Usage Examples

## Extract TOC only
```bash
python main.py --toc-only
```

## Full run (all content)
```bash
python main.py --mode 1
```

## Extract first 200 pages (memory-safe)
```bash
python main.py --mode 3
```

## Search extracted content
```bash
python search_content.py "USB"
python search_content.py "Power Delivery" outputs/usb_pd_content.jsonl
```

## Testing

### Run all tests
```bash
pytest -q
```

### Run a single test
```bash
pytest tests/test_toc.py::test_toc_parsing -q
```

### Run with coverage
```bash
pytest --cov=src --cov-report=html
```

## Regenerate outputs locally for CI
```bash
python main.py --mode 1
# This creates outputs/usb_pd_toc.jsonl, usb_pd_content.jsonl, usb_pd_spec.jsonl
```