import json
from collections.abc import Iterable
from pathlib import Path

from .models import TOCEntry


def write_jsonl(entries: Iterable[TOCEntry], out_path: Path) -> None:
    """Write TOC entries to JSONL file using streaming approach."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with out_path.open("w", encoding="utf-8") as fh:
        for e in entries:
            fh.write(json.dumps(e.model_dump(), ensure_ascii=False) + "\n")
            count += 1
            # Flush periodically for large files
            if count % 1000 == 0:
                fh.flush()
