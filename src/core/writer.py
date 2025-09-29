"""OutputWriter class for writing JSON/CSV files."""

import json
import csv
from pathlib import Path
from typing import Dict, List


class OutputWriter:
    """Writes JSON/CSV output files."""
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def write_json(self, data: Dict, filename: str) -> Path:
        """Write data to JSON file."""
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def write_jsonl(self, items: List[Dict], filename: str) -> Path:
        """Write items to JSONL file."""
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        return output_path
    
    def write_csv(self, data: List[Dict], filename: str) -> Path:
        """Write data to CSV file."""
        if not data:
            return None
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        return output_path
    
    def write_text(self, content: str, filename: str) -> Path:
        """Write content to text file."""
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path