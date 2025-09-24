import logging
from pathlib import Path


class LoggerFactory:
    """Factory class for creating configured loggers."""
    
    def __init__(self, name: str = "usb_pd_parser"):
        self._name = name
        self._formatter = self._create_formatter()
    
    def _create_formatter(self) -> logging.Formatter:
        """Create log formatter."""
        return logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
    
    def create_logger(self, output_dir: Path | None = None) -> logging.Logger:
        """Create configured logger instance."""
        logger = logging.getLogger(self._name)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            self._add_console_handler(logger)
            if output_dir:
                self._add_file_handler(logger, output_dir)
        
        return logger
    
    def _add_console_handler(self, logger: logging.Logger) -> None:
        """Add console handler to logger."""
        ch = logging.StreamHandler()
        ch.setFormatter(self._formatter)
        logger.addHandler(ch)
    
    def _add_file_handler(self, logger: logging.Logger, output_dir: Path) -> None:
        """Add file handler to logger."""
        output_dir.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(output_dir / "parser.log")
        fh.setFormatter(self._formatter)
        logger.addHandler(fh)


def get_logger(name: str = "usb_pd_parser", output_dir: Path | None = None) -> logging.Logger:
    """Factory function for backward compatibility."""
    factory = LoggerFactory(name)
    return factory.create_logger(output_dir)
