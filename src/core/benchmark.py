"""USB PD Specification Parser - Performance Benchmarking."""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import Any


class BaseBenchmark(ABC):  # Abstraction
    """Base benchmark definition."""

    def __init__(self, name: str) -> None:
        self.__name = name  # Private

    @property
    def name(self) -> str:
        """Human-friendly benchmark name."""
        return str(self.__name)

    @abstractmethod
    def run(self) -> dict[str, Any]:
        """Execute the benchmark and return summary data."""


class ConfigBenchmark(BaseBenchmark):  # Inheritance
    """Benchmark configuration access."""

    def run(self) -> dict[str, Any]:
        """Run config benchmark."""
        from src.config import Config

        config = Config("application.yml")  # Create once, reuse
        start = time.perf_counter()
        for _ in range(100):
            _ = config.pdf_input_file
        elapsed = time.perf_counter() - start
        return {"name": self.name, "time": elapsed, "ops": 100}


class ModelBenchmark(BaseBenchmark):  # Inheritance
    """Benchmark model instantiation."""

    def run(self) -> dict[str, Any]:
        """Run model benchmark."""
        start = time.perf_counter()
        from src.core.models import BaseContent

        for i in range(200):
            BaseContent(page=i + 1, content=f"test {i}")
        elapsed = time.perf_counter() - start
        return {"name": self.name, "time": elapsed, "ops": 200}


class BenchmarkSuite:
    """Collects benchmarks and executes them as a batch."""

    def __init__(self) -> None:
        self._benchmarks: list[BaseBenchmark] = []

    def add(self, benchmark: BaseBenchmark) -> None:
        """Register a benchmark in the suite."""
        self._benchmarks.append(benchmark)

    def __iter__(self) -> Iterable[BaseBenchmark]:
        return iter(self._benchmarks)

    def run(self) -> list[dict[str, Any]]:
        """Execute all benchmarks and return their summaries."""
        return [benchmark.run() for benchmark in self._benchmarks]


class BenchmarkCLI:
    """CLI adapter responsible for presenting benchmark results."""

    def __init__(
        self,
        suite: BenchmarkSuite,
        *,
        output: Callable[[str], None] | None = None,
    ):
        """Create a CLI wrapper with an injectable output sink."""
        self._suite = suite
        self._output = output or print

    def run(self) -> None:
        """Execute the suite and emit formatted results through the sink."""
        for result in self._suite.run():
            name = result["name"]
            time_val = result["time"]
            ops = result["ops"]
            msg = f"{name}: {time_val:.3f}s ({ops} ops)"
            self._output(msg)


def build_default_suite() -> BenchmarkSuite:
    """Create a suite populated with default benchmarks."""
    suite = BenchmarkSuite()
    suite.add(ConfigBenchmark("Config"))
    suite.add(ModelBenchmark("Model"))
    return suite


def main() -> None:
    """Main benchmark entry point."""
    logging.basicConfig(level=logging.INFO)
    suite = build_default_suite()
    BenchmarkCLI(suite).run()


if __name__ == "__main__":
    main()
