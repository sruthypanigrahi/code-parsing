"""Main orchestrator using core OOP classes."""

from src.core.cleaner import TextCleaner
from src.core.config import ConfigManager
from src.core.loader import PDFLoader
from src.core.parser import PDFParser
from src.core.writer import OutputWriter


def main() -> None:
    """Main function orchestrating OOP classes."""

    # Use ConfigManager class
    config = ConfigManager()
    cfg = config.get_all()

    # Use PDFLoader class
    loader = PDFLoader()
    pdf_path = cfg.get("pdf_input_file", "assets/USB_PD_R3_2_V1.1_2024-10.pdf")
    file_path = loader.load_file(pdf_path)

    # Use PDFParser class
    parser = PDFParser(cfg)
    data = parser.parse_file(str(file_path))

    # Use TextCleaner class
    cleaner = TextCleaner()
    clean_data = cleaner.normalize_content(data)

    # Use OutputWriter class
    writer = OutputWriter(cfg.get("output_directory", "outputs"))

    # Write outputs
    json_file = writer.write_json(clean_data, "parsed_data.json")

    if clean_data.get("paragraphs"):
        para_file = writer.write_jsonl(
            [{"id": i, "text": p} for i, p in enumerate(clean_data["paragraphs"])],
            "paragraphs.jsonl",
        )

    if clean_data.get("toc"):
        toc_file = writer.write_jsonl(clean_data["toc"], "toc.jsonl")

    # Results
    print(f"Processed: {clean_data['source_file']}")
    print(f"Paragraphs: {len(clean_data.get('paragraphs', []))}")
    print(f"TOC entries: {len(clean_data.get('toc', []))}")
    print(f"Output: {json_file}")


if __name__ == "__main__":
    main()
