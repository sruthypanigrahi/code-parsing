#!/usr/bin/env python3
"""Development environment setup script."""

import subprocess
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def install_pre_commit():
    """Install and setup pre-commit hooks."""
    logger.info(" Setting up pre-commit hooks...")
    
    try:
        # Install pre-commit if not already installed
        logger.info("Installing pre-commit package...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"], check=True)
        
        # Install the git hook scripts
        logger.info("Installing git hook scripts...")
        subprocess.run(["pre-commit", "install"], check=True)
        
        # Run hooks on all files to test
        logger.info(" Testing pre-commit hooks on all files...")
        result = subprocess.run(["pre-commit", "run", "--all-files"], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(" Pre-commit hooks installed and tested successfully!")
        else:
            logger.warning(" Pre-commit hooks installed but some checks failed:")
            logger.warning(result.stdout)
            logger.info("Run 'pre-commit run --all-files' to see and fix issues.")
            
    except subprocess.CalledProcessError as e:
        logger.error(f" Oops! Error setting up pre-commit: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logger.error(" Oops! pre-commit command not found. Make sure it's installed.")
        sys.exit(1)


def install_dev_dependencies():
    """Install development dependencies."""
    logger.info(" Installing development dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements-dev.txt"
        ], check=True)
        logger.info(" Development dependencies installed!")
    except subprocess.CalledProcessError as e:
        logger.error(f" Oops! Error installing dependencies: {e}")
        sys.exit(1)


def main():
    """Main setup function."""
    logger.info(" Setting up development environment...")
    
    try:
        # Check if we're in the right directory
        if not Path("requirements-dev.txt").exists():
            logger.error(" Oops! requirements-dev.txt not found. Run this script from the project root.")
            sys.exit(1)
        
        install_dev_dependencies()
        install_pre_commit()
        
        logger.info("\n Development environment setup complete!")
        logger.info("\nNext steps:")
        logger.info("1. Run 'python run_tests.py' to run tests with coverage")
        logger.info("2. Run 'pre-commit run --all-files' to check code quality")
        logger.info("3. Make a commit to test pre-commit hooks")
        
    except Exception as e:
        logger.error(f" Oops! Unexpected error during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()