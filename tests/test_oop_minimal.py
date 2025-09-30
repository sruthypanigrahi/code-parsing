"""Minimal OOP tests with all 4 principles."""

from abc import ABC, abstractmethod
from typing import Dict, List


class BaseTest(ABC):  # Abstraction
    """Abstract test base (Abstraction, Encapsulation)."""
    
    def __init__(self, name: str):
        self._name = name  # Encapsulation
    
    @abstractmethod  # Abstraction
    def run(self) -> bool:
        pass


class ConfigTest(BaseTest):  # Inheritance
    """Config test (Inheritance, Polymorphism)."""
    
    def run(self) -> bool:  # Polymorphism
        from src.config import Config
        config = Config("application.yml")
        pdf_file = config.pdf_input_file
        return len(str(pdf_file)) > 0


class ModelTest(BaseTest):  # Inheritance
    """Model test (Inheritance, Polymorphism)."""
    
    def run(self) -> bool:  # Polymorphism
        from src.models import BaseContent
        content = BaseContent(page=1, content="test")
        return content.page == 1


class TestRunner:  # Encapsulation
    """Test runner (All 4 OOP principles)."""
    
    def __init__(self):
        self._tests: List[BaseTest] = []  # Encapsulation
    
    def add(self, test: BaseTest) -> None:  # Polymorphism
        self._tests.append(test)
    
    def run_all(self) -> Dict[str, bool]:  # Abstraction
        results: Dict[str, bool] = {test._name: test.run() for test in self._tests}
        return results


def test_oop_principles():
    """Test all 4 OOP principles in minimal code."""
    runner = TestRunner()
    runner.add(ConfigTest("config"))  # Factory pattern
    runner.add(ModelTest("model"))
    
    results = runner.run_all()
    assert all(results.values())