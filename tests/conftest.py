"""Minimal test configuration with OOP principles."""

from abc import ABC, abstractmethod
from pathlib import Path

import pytest


class BaseFixture(ABC):  # Abstraction
    def __init__(self):
        self._data = {}  # Encapsulation

    @abstractmethod  # Abstraction
    def create(self, tmp_path: Path):
        pass


class ConfigFixture(BaseFixture):  # Inheritance
    def create(self, tmp_path: Path):  # Polymorphism
        config_file = tmp_path / "test.yml"
        config_file.write_text("pdf_input_file: test.pdf\noutput_directory: outputs")
        return config_file


class PDFFixture(BaseFixture):  # Inheritance
    def create(self, tmp_path: Path):  # Polymorphism
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_text("Mock PDF")
        return pdf_file


class FixtureFactory:  # Encapsulation
    def __init__(self):
        self._fixtures = {}  # Encapsulation

    def register(self, name: str, fixture: BaseFixture) -> None:  # Polymorphism
        self._fixtures[name] = fixture

    def create(self, name: str, tmp_path: Path):  # Abstraction
        return self._fixtures[name].create(tmp_path)


@pytest.fixture
def fixture_factory():
    factory = FixtureFactory()
    factory.register("config", ConfigFixture())
    factory.register("pdf", PDFFixture())
    return factory
