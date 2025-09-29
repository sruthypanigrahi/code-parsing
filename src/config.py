"""Configuration loader with OOP principles."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional
import yaml


class BaseConfig(ABC):  # Abstraction
    """Abstract config loader (Abstraction, Encapsulation)."""
    
    def __init__(self, config_path: str):
        self._config_path = Path(config_path)  # Encapsulation
        self._config = self._load_config()  # Encapsulation
    
    @abstractmethod  # Abstraction
    def _load_config(self) -> dict[str, Any]:
        pass
    
    @abstractmethod  # Abstraction
    def _get_defaults(self) -> dict[str, Any]:
        pass


class Config(BaseConfig):  # Inheritance
    """YAML config loader (Inheritance, Polymorphism)."""
    
    def _load_config(self) -> dict[str, Any]:  # Polymorphism
        """Load config with defaults (Abstraction)."""
        if not self._config_path.exists():
            return self._get_defaults()
        
        try:
            with open(self._config_path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}") from e
    
    def _get_defaults(self) -> dict[str, Any]:  # Polymorphism
        """Default configuration (Abstraction)."""
        return {
            "pdf_input_file": "assets/USB_PD_R3_2_V1.1_2024-10.pdf",
            "output_directory": "outputs",
            "max_pages": None,
        }
    
    @property  # Encapsulation
    def pdf_input_file(self) -> Path:
        return Path(self._config.get("pdf_input_file", "assets/sample.pdf"))
    
    @property  # Encapsulation
    def output_directory(self) -> Path:
        return Path(self._config.get("output_directory", "outputs"))
    
    @property  # Encapsulation
    def max_pages(self) -> Optional[int]:
        return self._config.get("max_pages")
    
    def get(self, key: str, default: Any = None) -> Any:  # Abstraction
        return self._config.get(key, default)