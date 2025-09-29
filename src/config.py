"""Simple configuration loader."""

from pathlib import Path
from typing import Any, Optional
import yaml


class Config:
    """Simple YAML configuration loader."""
    
    def __init__(self, config_path: str = "application.yml"):
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self) -> dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            # Default config
            return {
                "pdf_input_file": "assets/USB_PD_R3_2_V1.1_2024-10.pdf",
                "output_directory": "outputs",
                "max_pages": None,
            }
        
        try:
            with open(self.config_path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}") from e
    
    @property
    def pdf_input_file(self) -> Path:
        return Path(self._config.get("pdf_input_file", "assets/sample.pdf"))
    
    @property
    def output_directory(self) -> Path:
        return Path(self._config.get("output_directory", "outputs"))
    
    @property
    def max_pages(self) -> Optional[int]:
        return self._config.get("max_pages")