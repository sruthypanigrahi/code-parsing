import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration loader for the USB PD Parser."""

    def __init__(self, config_path: str = "application.yml"):
        self.config_path = Path(config_path)
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @property
    def pdf_input_file(self) -> Path:
        return Path(self._config.get("pdf_input_file", "assets/sample.pdf"))
    
    @pdf_input_file.setter
    def pdf_input_file(self, value: Path) -> None:
        self._config["pdf_input_file"] = str(value)

    @property
    def output_directory(self) -> Path:
        return Path(self._config.get("output_directory", "outputs"))

    @property
    def toc_file(self) -> Path:
        return Path(self._config.get("toc_file", "outputs/output.jsonl"))
    
    @toc_file.setter
    def toc_file(self, value: Path) -> None:
        self._config["toc_file"] = str(value)

    @property
    def ocr_fallback(self) -> bool:
        return bool(self._config.get("ocr_fallback", False))

    @property
    def max_pages(self) -> int | None:
        return self._config.get("max_pages")
    
    @max_pages.setter
    def max_pages(self, value: int | None) -> None:
        self._config["max_pages"] = value
