#!/usr/bin/env python3
"""CLI entry point for USB PD Specification Parser."""

import click
import sys
from pathlib import Path
from src.app import USBPDParser


@click.command()
@click.option(
    "--input",
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    help="Input PDF file path (required)"
)
@click.option(
    "--out",
    "output_path",
    type=click.Path(path_type=Path),
    help="Output JSONL file path"
)
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True, path_type=Path),
    default="application.yml",
    help="Configuration file path (default: application.yml)"
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging"
)
@click.option(
    "--max-pages",
    type=int,
    help="Maximum pages to process (default: all)"
)
def main(
    input_path: Path | None,
    output_path: Path,
    config_path: Path,
    debug: bool,
    max_pages: int | None
) -> None:
    """USB PD Specification Parser - Extract TOC from PDF files."""
    try:
        # Set debug logging if requested
        if debug:
            import logging
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Load configuration with debug flag
        app = USBPDParser(str(config_path), debug=debug)
        
        # Override config with CLI arguments if provided
        if input_path:
            app.cfg.pdf_input_file = input_path
        if output_path:
            app.cfg.toc_file = output_path
        if max_pages:
            app.cfg.max_pages = max_pages
        
        # Validate required input
        if not input_path and not app.cfg.pdf_input_file.exists():
            click.echo("Error: Input PDF file is required. Use --input to specify the file.", err=True)
            sys.exit(1)
        elif input_path and not input_path.exists():
            click.echo(f"Error: Input PDF file not found: {input_path}", err=True)
            sys.exit(1)
        
        # Run the parser
        app.run()
        
        click.echo(f" Processing complete! Output saved to: {app.cfg.toc_file}")
        
    except Exception as e:
        click.echo(f" Error: {e}", err=True)
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()