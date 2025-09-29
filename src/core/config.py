"""ConfigManager class for loading YAML/.env configuration."""

import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Loads YAML/.env configuration."""
    
    def __init__(self, config_path: str = "application.yml"):
        self.config_path = Path(config_path)
        self.config = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from YAML file."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
        else:
            # Default configuration
            self.config = {
                "pdf_input_file": "assets/USB_PD_R3_2_V1.1_2024-10.pdf",
                "output_directory": "outputs",
                "max_pages": None,
                "toc_file": "outputs/usb_pd_toc.jsonl"
            }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration."""
        return self.config.copy()
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False)