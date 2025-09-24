# #!/usr/bin/env python3
# """Quick test to verify the fixes work."""

# from src.models import TOCEntry, PageContent
# from src.parser import TOCParser
# from src.writer import JSONLWriter
# from pathlib import Path

# def test_models():
#     """Test model creation and serialization."""
#     # Test PageContent
#     page = PageContent(page=1, text="Sample text", image_count=0, table_count=0)
#     json_str = page.model_dump_json()
#     print(f"✓ PageContent serialization works: {len(json_str)} chars")
    
#     # Test TOCEntry
#     entry = TOCEntry(
#         doc_title="Test Doc",
#         section_id="1.2.3",
#         title="Test Section",
#         page=42,
#         level=None,
#         full_path="1.2.3 Test Section"
#     )
#     json_str = entry.model_dump_json()
#     print(f"✓ TOCEntry serialization works: {len(json_str)} chars")
#     print(f"  Level inferred: {entry.level}")
#     print(f"  Parent ID inferred: {entry.parent_id}")

# def test_parser():
#     """Test improved parser patterns."""
#     parser = TOCParser()
#     test_lines = [
#         "1.2.3 Test Section  42",
#         "1.2.3    Test Section    42", 
#         "1.2.3 Test Section .... 42",
#         "1.2.3 Test Section..........42"
#     ]
    
#     for line in test_lines:
#         entries = parser.parse_toc([(1, line)])
#         if entries:
#             print(f"✓ Parsed: '{line}' -> {entries[0].section_id} '{entries[0].title}' p.{entries[0].page}")
#         else:
#             print(f"✗ Failed to parse: '{line}'")

# def test_writer():
#     """Test JSONL writer."""
#     entries = [
#         TOCEntry(
#             doc_title="Test",
#             section_id="1",
#             title="Introduction", 
#             page=1,
#             level=None,
#             full_path="1 Introduction"
#         )
#     ]
    
#     output_file = Path("test_output.jsonl")
#     JSONLWriter.write(entries, output_file)
    
#     if output_file.exists():
#         content = output_file.read_text()
#         print(f"✓ JSONL writer works: {len(content)} chars written")
#         output_file.unlink()  # cleanup
#     else:
#         print("✗ JSONL writer failed")

# if __name__ == "__main__":
#     print("Testing fixes...")
#     test_models()
#     test_parser() 
#     test_writer()
#     print("All tests completed!")