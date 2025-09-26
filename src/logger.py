import logging
from pathlib import Path
from typing import Optional


class LoggerFactory:
    def __init__(self, name: str = "usb_pd_parser"):
        self._name = name
        self._formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )

    def create_logger(
        self, output_dir: Optional[Path] = None, debug: bool = False
    ) -> logging.Logger:
        logger = logging.getLogger(self._name)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

        if not logger.handlers:
            self._add_console_handler(logger, debug)
            if output_dir:
                self._add_file_handler(logger, output_dir, debug)
        return logger

    def _add_console_handler(self, logger: logging.Logger, debug: bool) -> None:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG if debug else logging.INFO)
        ch.setFormatter(self._formatter)
        logger.addHandler(ch)

    def _add_file_handler(
        self, logger: logging.Logger, output_dir: Path, debug: bool
    ) -> None:
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(output_dir / "parser.log")
            fh.setLevel(logging.DEBUG if debug else logging.INFO)
            fh.setFormatter(self._formatter)
            logger.addHandler(fh)
        except (OSError, PermissionError) as e:
            logger.warning(f"Could not create file handler: {e}")


def get_logger(
    name: str = "usb_pd_parser", output_dir: Optional[Path] = None, debug: bool = False
) -> logging.Logger:
    factory = LoggerFactory(name)
    return factory.create_logger(output_dir, debug)
