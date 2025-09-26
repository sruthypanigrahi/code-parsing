import json
from pathlib import Path
from typing import Iterable
from .models import TOCEntry


def write_jsonl(entries: Iterable[TOCEntry], out_path: Path) -> None:
    """Write TOC entries to JSONL file using streaming approach."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for e in entries:
            fh.write(json.dumps(e.model_dump(), ensure_ascii=False) + "\n")
