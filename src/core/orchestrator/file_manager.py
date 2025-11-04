"""USB PD Specification Parser - File Management Module"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from src.config.config import Config
from src.config.constants import USB_PD_SPEC_FILE, USB_PD_TOC_FILE
from src.core.orchestrator.component import PipelineComponent
from src.support.output_writer import BaseWriter, JSONLWriter

WriterFactory = Callable[[Path], BaseWriter]


class FileManager(PipelineComponent):
    """Manage writing pipeline artifacts to disk using pluggable writers."""

    def __init__(
        self,
        config: Config,
        logger: Any,
        *,
        toc_writer_factory: WriterFactory | None = None,
        spec_writer_factory: WriterFactory | None = None,
    ):
        """Initialize the manager with dependency-injected writer factories."""
        super().__init__(config, logger)
        self._toc_writer_factory = toc_writer_factory or (lambda path: JSONLWriter(path))
        self._spec_writer_factory = spec_writer_factory or (lambda path: JSONLWriter(path))
        self.__prepare_output_directory()

    def __prepare_output_directory(self) -> None:
        """Ensure the configured output directory exists before writing."""
        output_dir = self._ensure_directory(self.config.output_directory)
        self.logger.info("Output directory prepared: %s", output_dir)

    def __write_toc_file(self, toc: list[Any]) -> None:
        """Write TOC data to the configured writer."""
        if not toc:
            raise ValueError("TOC data cannot be empty")

        output_dir = self.config.output_directory
        toc_path = output_dir / USB_PD_TOC_FILE
        toc_writer = self._toc_writer_factory(toc_path)
        toc_writer.write(toc)
        self.logger.info("TOC file written: %s", toc_path)

    def __write_spec_file(self, content: list[Any]) -> None:
        """Write extracted content to the configured writer."""
        if not content:
            raise ValueError("Content data cannot be empty")

        output_dir = self.config.output_directory
        spec_path = output_dir / USB_PD_SPEC_FILE
        spec_writer = self._spec_writer_factory(spec_path)
        spec_writer.write(content)
        self.logger.info("Spec file written: %s", spec_path)

    def write_files(self, toc: list[Any], content: list[Any]) -> None:
        """Write both TOC and content artifacts using the injected writers."""
        self.logger.info("Writing JSONL output files...")
        self.__write_toc_file(toc)
        self.__write_spec_file(content)
        self.logger.info("JSONL files written successfully")
