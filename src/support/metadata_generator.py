"""Metadata generators with OOP principles."""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any, ClassVar

from src.utils.mixins import OutputDirMixin, StatsMixin


class BaseMetadataGenerator(OutputDirMixin, StatsMixin, ABC):
    """Template method base class for metadata generators."""

    file_name: ClassVar[str]

    def __init__(self, output_dir: Path) -> None:
        super().__init__(output_dir)
        self._logger = logging.getLogger(self.__class__.__name__)

    def generate_metadata(self, spec_file: Path) -> Path:
        """Run the metadata generation template method."""
        metadata_path = self.output_dir / self.file_name
        entry_stream = self._iterate_spec_entries(spec_file)
        if entry_stream is None:
            self._set_stat("entries_processed", 0)
            return metadata_path

        processed = self._write_entries(metadata_path, entry_stream)
        self._set_stat("entries_processed", processed)
        return metadata_path

    def _iterate_spec_entries(
        self, spec_file: Path
    ) -> Iterator[dict[str, Any]] | None:
        """Yield parsed JSON entries from the specification file."""
        if not spec_file.exists():
            return None

        def _generator() -> Iterator[dict[str, Any]]:
            try:
                with open(spec_file, encoding="utf-8") as handle:
                    for line in handle:
                        if not line.strip():
                            continue
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError as exc:
                            self._logger.debug("Skipping malformed entry: %s", exc)
            except OSError as exc:
                self._logger.debug("Cannot read %s: %s", spec_file, exc)

        return _generator()

    @abstractmethod
    def _write_entries(
        self, output_path: Path, entries: Iterable[dict[str, Any]]
    ) -> int:
        """Persist metadata entries and return the count written."""


class JSONLMetadataGenerator(BaseMetadataGenerator):
    """JSONL metadata generator."""

    file_name = "usb_pd_metadata.jsonl"

    def _write_entries(
        self, output_path: Path, entries: Iterable[dict[str, Any]]
    ) -> int:
        count = 0
        try:
            with open(output_path, "w", encoding="utf-8") as handle:
                for item in entries:
                    handle.write(json.dumps(self._create_metadata(item)) + "\n")
                    count += 1
        except OSError as exc:
            self._logger.debug("Cannot write JSONL metadata: %s", exc)
        return count

    def _create_metadata(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create metadata entry."""
        content = data.get("content", "")
        return {
            "doc_title": data.get("doc_title", "USB PD Specification"),
            "section_id": data.get("section_id", ""),
            "page": data.get("page", 1),
            "type": data.get("type", "paragraph"),
            "word_count": len(content.split()),
            "char_count": len(content),
        }


class CSVMetadataGenerator(BaseMetadataGenerator):
    """CSV metadata generator."""

    file_name = "usb_pd_metadata.csv"

    def _write_entries(
        self, output_path: Path, entries: Iterable[dict[str, Any]]
    ) -> int:
        count = 0
        try:
            with open(output_path, "w", encoding="utf-8") as handle:
                handle.write(
                    "doc_title,section_id,page,type,word_count,char_count\n"
                )
                for item in entries:
                    handle.write(self._create_csv_row(item) + "\n")
                    count += 1
        except OSError as exc:
            self._logger.debug("Cannot write CSV metadata: %s", exc)
        return count

    def _create_csv_row(self, data: dict[str, Any]) -> str:
        """Create CSV row from data."""
        content = data.get("content", "")
        doc_title = data.get("doc_title", "USB PD Specification")
        section_id = data.get("section_id", "")
        page = data.get("page", 1)
        data_type = data.get("type", "paragraph")
        word_count = len(content.split())
        char_count = len(content)

        return (
            f"{doc_title},{section_id},{page},{data_type},"
            f"{word_count},{char_count}"
        )


class MetadataGeneratorFactory:
    """Factory for metadata generators backed by a registry."""

    _REGISTRY: dict[str, type[BaseMetadataGenerator]] = {}

    @classmethod
    def register(cls, key: str, generator: type[BaseMetadataGenerator]) -> None:
        """Register a metadata generator implementation."""
        cls._REGISTRY[key.lower()] = generator

    @classmethod
    def create(
        cls, generator_type: str, output_dir: Path
    ) -> BaseMetadataGenerator:
        """Create a metadata generator instance."""
        key = generator_type.lower()
        try:
            generator_cls = cls._REGISTRY[key]
        except KeyError as exc:
            available = ", ".join(sorted(cls._REGISTRY))
            raise ValueError(
                f"Unknown generator type: {generator_type}. "
                f"Available types: {available}"
            ) from exc
        return generator_cls(output_dir)

    @classmethod
    def registered_types(cls) -> tuple[str, ...]:
        """Return the registered generator identifiers."""
        return tuple(sorted(cls._REGISTRY))


def create_metadata_file(
    output_dir: Path, spec_file: Path, generator_type: str = "jsonl"
) -> Path:
    """Factory function to create a metadata file using the registry."""
    generator = MetadataGeneratorFactory.create(generator_type, output_dir)
    return generator.generate_metadata(spec_file)


# Register default generators.
MetadataGeneratorFactory.register("jsonl", JSONLMetadataGenerator)
MetadataGeneratorFactory.register("csv", CSVMetadataGenerator)
