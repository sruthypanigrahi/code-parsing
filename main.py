#!/usr/bin/env python3
"""USB PD Specification Parser - Main Entry Point with OOP principles"""

from abc import ABC, abstractmethod
from typing import Any

from src.app import CLIApp


class BaseRunner(ABC):  # Abstraction
    """Abstract application runner (Abstraction, Encapsulation)."""

    def __init__(self):
        self._app = None  # Encapsulation: protected attribute

    @abstractmethod  # Abstraction: must be implemented
    def create_app(self) -> Any:
        """Create application instance."""
        pass

    def run(self) -> None:  # Abstraction: template method
        """Run the application (Template Method pattern)."""
        self._app = self.create_app()  # Encapsulation
        self._execute()  # Encapsulation: protected method

    def _execute(self) -> None:  # Encapsulation: protected method
        """Execute the application."""
        if self._app:
            self._app.run()


class CLIRunner(BaseRunner):  # Inheritance
    """CLI application runner (Inheritance, Polymorphism)."""

    def create_app(self) -> CLIApp:  # Polymorphism: implements abstract method
        """Create CLI application instance."""
        return CLIApp()


class ApplicationFactory:  # Abstraction: Factory pattern
    """Application factory (Abstraction, Encapsulation)."""

    @staticmethod  # Encapsulation: static factory method
    def create_runner(runner_type: str = "cli") -> BaseRunner:
        """Create runner instance (Factory Method pattern)."""
        if runner_type == "cli":
            return CLIRunner()  # Polymorphism: returns concrete implementation
        raise ValueError(f"Invalid runner type: {runner_type}")


def main():
    """Main entry point using OOP principles."""
    # Factory pattern (Abstraction)
    runner = ApplicationFactory.create_runner("cli")  # Polymorphism
    runner.run()  # Polymorphism: calls concrete implementation


if __name__ == "__main__":
    main()
