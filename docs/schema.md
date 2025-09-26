# Output Schema

## usb_pd_toc.jsonl

TOC entries with hierarchical structure:

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

## usb_pd_content.jsonl / usb_pd_spec.jsonl

Content items (paragraphs, images, tables):

### Paragraph
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

### Image
```json
{
  "doc_title": "USB_PD_R3_2 V1.1 2024-10.pdf", 
  "content_id": "C2",
  "type": "image",
  "content": "[Image 469x72 on page 1032]",
  "page": 1032,
  "block_id": "img1032_8", 
  "bbox": [71.74, 260.98, 540.26, 332.54],
  "metadata": {
    "extracted_at": "2025-09-27T01:28:59.335084",
    "content_length": 27
  }
}
```

### Table
```json
{
  "doc_title": "USB_PD_R3_2 V1.1 2024-10.pdf",
  "content_id": "C3", 
  "type": "table",
  "content": "Table 2.1 Fixed Supply Power Ranges...",
  "page": 27,
  "block_id": "tbl27_0",
  "bbox": [],
  "metadata": {
    "extracted_at": "2025-09-27T01:28:59.335084", 
    "content_length": 156
  }
}
```