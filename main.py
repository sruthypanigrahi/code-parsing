#!/usr/bin/env python3
"""CLI entry point for USB PD Specification Parser."""

from src.app import USBPDParser


def main():
    """Main entry point - just instantiate and run."""
    app = USBPDParser()
    app.run()


if __name__ == "__main__":
    main()