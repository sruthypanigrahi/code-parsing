#!/usr/bin/env python3
"""Performance profiler with OOP principles."""

import cProfile
import pstats
from abc import ABC, abstractmethod
from io import StringIO
from typing import Any, Dict


class BaseProfiler(ABC):  # Abstraction
    """Abstract profiler (Abstraction, Encapsulation)."""
    
    def __init__(self, name: str):
        self._name = name  # Encapsulation
        self._profiler = cProfile.Profile()  # Encapsulation
    
    @abstractmethod  # Abstraction
    def profile_operation(self) -> Dict[str, Any]:
        pass
    
    def _run_profiled(self, func, *args) -> Dict[str, Any]:  # Encapsulation
        self._profiler.enable()
        result = func(*args)
        self._profiler.disable()
        
        # Get stats
        s = StringIO()
        ps = pstats.Stats(self._profiler, stream=s)
        ps.sort_stats('cumulative').print_stats(10)
        
        return {
            "result": result,
            "profile_output": s.getvalue(),
            "total_calls": ps.total_calls
        }


class ConfigProfiler(BaseProfiler):  # Inheritance
    """Config profiler (Inheritance, Polymorphism)."""
    
    def profile_operation(self) -> Dict[str, Any]:  # Polymorphism
        from src.config import Config
        
        profile_data = self._run_profiled(self._config_operations)
        
        return {
            "profiler": self._name,
            "operations": 500,
            "total_calls": profile_data["total_calls"],
            "profile_stats": profile_data["profile_output"][:500] + "..."
        }
    
    def _config_operations(self) -> int:  # Encapsulation
        count = 0
        for _ in range(500):
            config = Config("application.yml")
            _ = config.pdf_input_file
            count += 1
        return count


class ModelProfiler(BaseProfiler):  # Inheritance
    """Model profiler (Inheritance, Polymorphism)."""
    
    def profile_operation(self) -> Dict[str, Any]:  # Polymorphism
        from src.models import BaseContent, TOCEntry
        
        profile_data = self._run_profiled(self._model_operations)
        
        return {
            "profiler": self._name,
            "operations": 1000,
            "total_calls": profile_data["total_calls"],
            "profile_stats": profile_data["profile_output"][:500] + "..."
        }
    
    def _model_operations(self) -> int:  # Encapsulation
        count = 0
        for i in range(1000):
            BaseContent(page=i+1, content=f"test {i}")
            if i % 50 == 0:
                TOCEntry(
                    doc_title="Profile", section_id=f"S{i}",
                    title=f"Title {i}", full_path=f"Path {i}",
                    page=i+1, level=1
                )
            count += 1
        return count


class ProfilerSuite:  # Abstraction
    """Profiler suite (Abstraction, Encapsulation)."""
    
    def __init__(self):
        self._profilers = []  # Encapsulation
    
    def add_profiler(self, profiler: BaseProfiler) -> None:  # Polymorphism
        self._profilers.append(profiler)
    
    def run_all(self) -> Dict[str, Any]:  # Abstraction
        results = {}
        for profiler in self._profilers:
            result = profiler.profile_operation()  # Polymorphism
            results[result["profiler"]] = result
        return results


def main():
    """Run performance profiling with OOP principles."""
    suite = ProfilerSuite()
    
    # Add profilers (Factory pattern)
    suite.add_profiler(ConfigProfiler("Config Profiler"))
    suite.add_profiler(ModelProfiler("Model Profiler"))
    
    # Run profiling
    results = suite.run_all()
    
    print("Performance Profiling Results:")
    print("=" * 50)
    for name, result in results.items():
        print(f"Profiler: {name}")
        print(f"  Operations: {result['operations']}")
        print(f"  Total Calls: {result['total_calls']}")
        print(f"  Top Functions:")
        print(f"  {result['profile_stats']}")
        print()


if __name__ == "__main__":
    main()