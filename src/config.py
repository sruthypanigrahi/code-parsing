from pathlib import Path
from typing import Any, Optional

import yaml


class Config:
    def __init__(self, config_path: str = "application.yml"):
        self.config_path = Path(config_path)
        self._config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        try:
            with open(self.config_path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}") from e

    @property
    def pdf_input_file(self) -> Path:
        return Path(self._config.get("pdf_input_file", "assets/sample.pdf"))

    @property
    def output_directory(self) -> Path:
        return Path(self._config.get("output_directory", "outputs"))

    @property
    def toc_file(self) -> Path:
        return Path(self._config.get("toc_file", "outputs/output.jsonl"))

    @property
    def ocr_fallback(self) -> bool:
        return bool(self._config.get("ocr_fallback", False))

    @property
    def max_pages(self) -> Optional[int]:
        value = self._config.get("max_pages")
        if value is not None and value <= 0:
            raise ValueError("max_pages must be positive")
        return value

    @property
    def strategy(self) -> str:
        return self._config.get("strategy", "regex")
