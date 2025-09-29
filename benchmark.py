#!/usr/bin/env python3
"""Performance benchmark with OOP principles."""

import time
import psutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class BaseBenchmark(ABC):  # Abstraction
    """Abstract benchmark (Abstraction, Encapsulation)."""
    
    def __init__(self, name: str):
        self._name = name  # Encapsulation
        self._process = psutil.Process()  # Encapsulation
    
    @abstractmethod  # Abstraction
    def run_benchmark(self) -> Dict[str, Any]:
        pass
    
    def _measure_performance(self, func, *args) -> Dict[str, Any]:  # Encapsulation
        # Memory before
        mem_before = self._process.memory_info().rss / 1024 / 1024  # MB
        
        # Time execution
        start_time = time.perf_counter()
        result = func(*args)
        end_time = time.perf_counter()
        
        # Memory after
        mem_after = self._process.memory_info().rss / 1024 / 1024  # MB
        
        return {
            "execution_time": end_time - start_time,
            "memory_before_mb": mem_before,
            "memory_after_mb": mem_after,
            "memory_delta_mb": mem_after - mem_before,
            "result": result
        }


class ConfigBenchmark(BaseBenchmark):  # Inheritance
    """Config benchmark (Inheritance, Polymorphism)."""
    
    def run_benchmark(self) -> Dict[str, Any]:  # Polymorphism
        from src.config import Config
        
        metrics = self._measure_performance(self._config_operations)
        
        return {
            "benchmark": self._name,
            "operations": 1000,
            "avg_time_ms": (metrics["execution_time"] / 1000) * 1000,
            "memory_usage_mb": metrics["memory_delta_mb"],
            "status": "OPTIMAL" if metrics["execution_time"] < 1.0 else "SLOW"
        }
    
    def _config_operations(self) -> int:  # Encapsulation
        count = 0
        for _ in range(1000):
            config = Config("application.yml")
            _ = config.pdf_input_file
            _ = config.output_directory
            count += 1
        return count


class ModelBenchmark(BaseBenchmark):  # Inheritance
    """Model benchmark (Inheritance, Polymorphism)."""
    
    def run_benchmark(self) -> Dict[str, Any]:  # Polymorphism
        from src.models import TOCEntry, BaseContent
        
        metrics = self._measure_performance(self._model_operations)
        
        return {
            "benchmark": self._name,
            "operations": 5000,
            "avg_time_ms": (metrics["execution_time"] / 5000) * 1000,
            "memory_usage_mb": metrics["memory_delta_mb"],
            "status": "OPTIMAL" if metrics["execution_time"] < 2.0 else "SLOW"
        }
    
    def _model_operations(self) -> int:  # Encapsulation
        count = 0
        for i in range(5000):
            BaseContent(page=i+1, content=f"content {i}")
            if i % 10 == 0:  # Every 10th iteration
                TOCEntry(
                    doc_title="Benchmark", section_id=f"S{i}", 
                    title=f"Section {i}", full_path=f"Path {i}",
                    page=i+1, level=1
                )
            count += 1
        return count


class BenchmarkRunner:  # Abstraction
    """Benchmark runner (Abstraction, Encapsulation)."""
    
    def __init__(self):
        self._benchmarks: List[BaseBenchmark] = []  # Encapsulation
    
    def add_benchmark(self, benchmark: BaseBenchmark) -> None:  # Polymorphism
        self._benchmarks.append(benchmark)
    
    def run_all(self) -> List[Dict[str, Any]]:  # Abstraction
        results = []
        for benchmark in self._benchmarks:
            result = benchmark.run_benchmark()  # Polymorphism
            results.append(result)
        return results


def main():
    """Run benchmarks with OOP principles."""
    runner = BenchmarkRunner()
    
    # Add benchmarks (Factory pattern)
    runner.add_benchmark(ConfigBenchmark("Config Performance"))
    runner.add_benchmark(ModelBenchmark("Model Performance"))
    
    # Run and display results
    results = runner.run_all()
    
    print("Performance Benchmark Results:")
    print("=" * 50)
    for result in results:
        print(f"Test: {result['benchmark']}")
        print(f"  Operations: {result['operations']}")
        print(f"  Avg Time: {result['avg_time_ms']:.3f}ms")
        print(f"  Memory: {result['memory_usage_mb']:.2f}MB")
        print(f"  Status: {result['status']}")
        print()


if __name__ == "__main__":
    main()