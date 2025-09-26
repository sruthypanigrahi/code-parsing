"""Performance monitoring and optimization utilities."""

import time
import functools
import logging
from typing import Any, Callable, TypeVar
from contextlib import contextmanager

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def timer(func: F) -> F:
    """Decorator to time function execution."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info(f"{func.__name__} took {end - start:.3f}s")
        return result

    return wrapper


@contextmanager
def timed_operation(operation_name: str):
    """Context manager for timing operations."""
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        logger.info(f"{operation_name} took {end - start:.3f}s")


class PerformanceMonitor:
    """Monitor performance metrics."""

    def __init__(self) -> None:
        self.metrics: dict[str, list[float]] = {}

    def record(self, metric_name: str, value: float) -> None:
        """Record a performance metric."""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(value)

    def get_stats(self, metric_name: str) -> dict[str, float]:
        """Get statistics for a metric."""
        values = self.metrics.get(metric_name, [])
        if not values:
            return {}

        return {
            "count": len(values),
            "total": sum(values),
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }

    def report(self) -> None:
        """Log performance report."""
        for metric, stats in [(m, self.get_stats(m)) for m in self.metrics]:
            if stats:
                logger.info(f"{metric}: {stats}")


# Global performance monitor
monitor = PerformanceMonitor()
