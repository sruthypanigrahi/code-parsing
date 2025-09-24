# from src.config import Config
# from src.extractor import PDFExtractor

# cfg = Config("application.yml")
# extractor = PDFExtractor(str(cfg.pdf_input_file), cfg.output_directory, cfg.ocr_fallback, 5)  # Just 5 pages for quick test
# pages = extractor.extract_full_content()

# total_images = sum(p.image_count for p in pages)
# total_tables = sum(p.table_count for p in pages)

# print(f"Pages: {len(pages)}")
# print(f"Images: {total_images}")
# print(f"Tables: {total_tables}")