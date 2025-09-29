"""PDFLoader class for file loading."""

from pathlib import Path
from typing import Iterator


class PDFLoader:
    """Iterates input directory, yields file paths."""

    def __init__(self, input_dir: str = "assets"):
        self.input_dir = Path(input_dir)

    def get_pdf_files(self) -> Iterator[Path]:
        """Yield PDF file paths from input directory."""
        for pdf_file in self.input_dir.glob("*.pdf"):
            yield pdf_file

    def load_file(self, file_path: str) -> Path:
        """Load and validate single PDF file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF file: {file_path}")
        return path
