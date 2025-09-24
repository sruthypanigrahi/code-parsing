#!/usr/bin/env python3


from src.app import USBPDParser


def main():
    """Main entry point - just instantiate and run."""
    parser = USBPDParser()
    parser.run()

if __name__ == "__main__":
    main()