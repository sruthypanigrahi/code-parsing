"""Main orchestrator using core OOP classes."""

import logging

from src.core.cleaner import TextCleaner
from src.core.config import ConfigManager
from src.core.loader import PDFLoader
from src.core.parser import PDFParser
from src.core.writer import OutputWriter

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Main function orchestrating OOP classes."""

    try:
        # Use ConfigManager class
        config = ConfigManager()
        cfg = config.get_all()

        # Use PDFLoader class
        loader = PDFLoader()
        pdf_path = cfg.get("pdf_input_file", "assets/USB_PD_R3_2_V1.1_2024-10.pdf")
        file_path = loader.load_file(pdf_path)
        logger.info(f"Loaded PDF: {file_path}")

        # Use PDFParser class
        parser = PDFParser(cfg)
        data = parser.parse_file(str(file_path))
        logger.info(f"Parsed {data.get('total_lines', 0)} lines")

        # Use TextCleaner class
        cleaner = TextCleaner()
        clean_data = cleaner.normalize_content(data)
        logger.info("Text cleaning completed")

        # Use OutputWriter class
        writer = OutputWriter(cfg.get("output_directory", "outputs"))

        # Write outputs
        json_file = writer.write_json(clean_data, "parsed_data.json")
        logger.info(f"Created: {json_file}")

        if clean_data.get("paragraphs"):
            writer.write_jsonl(
                [{"id": i, "text": p} for i, p in enumerate(clean_data["paragraphs"])],
                "paragraphs.jsonl",
            )

        if clean_data.get("toc"):
            writer.write_jsonl(clean_data["toc"], "toc.jsonl")

        # Results
        logger.info(f"Processing complete - File: {clean_data['source_file']}")
        logger.info(f"Paragraphs: {len(clean_data.get('paragraphs', []))}")
        logger.info(f"TOC entries: {len(clean_data.get('toc', []))}")

    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise


if __name__ == "__main__":
    main()
