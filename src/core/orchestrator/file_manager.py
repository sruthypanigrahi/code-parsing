"""USB PD Specification Parser - File Management Module"""

from typing import Any

from src.config.config import Config
from src.config.constants import USB_PD_SPEC_FILE, USB_PD_TOC_FILE
from src.core.orchestrator.component import PipelineComponent
from src.support.output_writer import JSONLWriter


class FileManager(PipelineComponent):
    """Manages all file I/O operations."""

    def __init__(self, config: Config, logger: Any):
        """Initialize file manager with dependencies."""
        super().__init__(config, logger)
        self.__prepare_output_directory()

    def __prepare_output_directory(self) -> None:
        """Prepare output directory for file operations."""
        output_dir = self._ensure_directory(self.config.output_directory)
        self.logger.info("Output directory prepared: %s", output_dir)

    def __write_toc_file(self, toc: list[Any]) -> None:
        """Write TOC data to JSONL file."""
        if not toc:
            raise ValueError("TOC data cannot be empty")

        output_dir = self.config.output_directory
        toc_path = output_dir / USB_PD_TOC_FILE
        toc_writer = JSONLWriter(toc_path)
        toc_writer.write(toc)
        self.logger.info("TOC file written: %s", toc_path)

    def __write_spec_file(self, content: list[Any]) -> None:
        """Write specification content to JSONL file."""
        if not content:
            raise ValueError("Content data cannot be empty")

        output_dir = self.config.output_directory
        spec_path = output_dir / USB_PD_SPEC_FILE
        spec_writer = JSONLWriter(spec_path)
        spec_writer.write(content)
        self.logger.info("Spec file written: %s", spec_path)

    def write_files(self, toc: list[Any], content: list[Any]) -> None:
        """Write all JSONL output files."""
        self.logger.info("Writing JSONL output files...")
        self.__write_toc_file(toc)
        self.__write_spec_file(content)
        self.logger.info("JSONL files written successfully")