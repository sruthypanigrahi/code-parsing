"""Performance tests with OOP principles."""

import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class BasePerformanceTest(ABC):  # Abstraction
    """Abstract performance test (Abstraction, Encapsulation)."""
    
    def __init__(self, name: str):
        self._name = name  # Encapsulation
        self._results: Dict[str, Any] = {}  # Encapsulation
    
    @abstractmethod  # Abstraction
    def run_test(self) -> Dict[str, Any]:
        pass
    
    def _measure_time(self, func, *args) -> float:  # Encapsulation
        start = time.perf_counter()
        func(*args)
        return time.perf_counter() - start


class ConfigPerformanceTest(BasePerformanceTest):  # Inheritance
    """Config performance test (Inheritance, Polymorphism)."""
    
    def run_test(self) -> Dict[str, Any]:  # Polymorphism
        from src.config import Config
        
        # Test config loading speed
        load_time = self._measure_time(self._test_config_load)
        
        return {
            "test_name": self._name,
            "config_load_time": load_time,
            "status": "PASS" if load_time < 0.1 else "SLOW"
        }
    
    def _test_config_load(self) -> None:  # Encapsulation
        from src.config import Config
        for _ in range(100):
            Config("application.yml")


class ModelPerformanceTest(BasePerformanceTest):  # Inheritance
    """Model performance test (Inheritance, Polymorphism)."""
    
    def run_test(self) -> Dict[str, Any]:  # Polymorphism
        from src.models import TOCEntry, BaseContent
        
        # Test model creation speed
        model_time = self._measure_time(self._test_model_creation)
        
        return {
            "test_name": self._name,
            "model_creation_time": model_time,
            "status": "PASS" if model_time < 0.5 else "SLOW"
        }
    
    def _test_model_creation(self) -> None:  # Encapsulation
        from src.models import BaseContent, TOCEntry
        for i in range(1000):
            BaseContent(page=i+1, content=f"test content {i}")
            TOCEntry(
                doc_title="Test", section_id=f"S{i}", title=f"Title {i}",
                full_path=f"Path {i}", page=i+1, level=1
            )


class PerformanceTestSuite:  # Abstraction
    """Performance test suite (Abstraction, Encapsulation)."""
    
    def __init__(self):
        self._tests: List[BasePerformanceTest] = []  # Encapsulation
        self._results: List[Dict[str, Any]] = []  # Encapsulation
    
    def add_test(self, test: BasePerformanceTest) -> None:  # Polymorphism
        self._tests.append(test)
    
    def run_all(self) -> List[Dict[str, Any]]:  # Abstraction
        self._results = []
        for test in self._tests:
            result = test.run_test()  # Polymorphism
            self._results.append(result)
        return self._results
    
    def get_summary(self) -> Dict[str, Any]:  # Encapsulation
        total_tests = len(self._results)
        passed = sum(1 for r in self._results if r["status"] == "PASS")
        return {
            "total_tests": total_tests,
            "passed": passed,
            "failed": total_tests - passed,
            "pass_rate": f"{(passed/total_tests)*100:.1f}%" if total_tests > 0 else "0%"
        }


def test_performance_suite():
    """Test performance with OOP principles."""
    suite = PerformanceTestSuite()  # Factory pattern
    
    # Add tests (Polymorphism)
    suite.add_test(ConfigPerformanceTest("Config Loading"))
    suite.add_test(ModelPerformanceTest("Model Creation"))
    
    # Run tests
    results = suite.run_all()
    summary = suite.get_summary()
    
    # Assertions
    assert summary["total_tests"] == 2
    assert summary["passed"] >= 1  # At least one should pass
    assert all(isinstance(r, dict) for r in results)