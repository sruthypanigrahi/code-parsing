#!/usr/bin/env python3
"""Test runner script with coverage reporting."""

import subprocess
import sys


def run_tests():
    """Run tests with coverage reporting."""
    print(" Running tests with coverage...")
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-fail-under=85",
        "-v"
    ]
    
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print("\n All tests passed!")
        print(" Coverage report generated in htmlcov/index.html")
    else:
        print("\n Some tests failed or coverage below threshold")
        sys.exit(1)


def run_specific_tests():
    """Run specific test categories."""
    print(" Running parser edge case tests...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_parser.py::TestTOCParser::test_malformed_lines",
        "tests/test_parser.py::TestTOCParser::test_multi_line_entries",
        "-v"
    ]
    
    subprocess.run(cmd)
    
    print("\n Running end-to-end tests...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_end_to_end.py",
        "-v"
    ]
    
    subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--specific":
        run_specific_tests()
    else:
        run_tests()