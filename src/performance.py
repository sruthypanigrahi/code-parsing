"""Performance monitoring and optimization utilities."""

import functools
import threading
import time
from contextlib import contextmanager
from typing import Any


class PerformanceMonitor:
    """Monitor performance metrics."""

    def __init__(self):
        self.metrics: dict[str, Any] = {}
        self._lock = threading.Lock()

    def record(self, key: str, value: Any):
        """Record a performance metric."""
        with self._lock:
            self.metrics[key] = value

    def increment(self, key: str, value: int = 1):
        """Increment a counter metric."""
        with self._lock:
            self.metrics[key] = self.metrics.get(key, 0) + value

    def report(self):
        """Print performance report."""
        print("\n=== Performance Report ===")
        for key, value in self.metrics.items():
            print(f"{key}: {value}")


# Global monitor instance
monitor = PerformanceMonitor()


def timer(func):
    """Decorator to time function execution."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        monitor.record(f"{func.__name__}_duration", f"{duration:.2f}s")
        return result

    return wrapper


@contextmanager
def timed_operation(name: str):
    """Context manager for timing operations."""
    start = time.time()
    try:
        yield
    finally:
        duration = time.time() - start
        monitor.record(f"{name}_duration", f"{duration:.2f}s")


@functools.lru_cache(maxsize=128)
def cached_metadata_parse(content_hash: str, content: str):
    """Cache expensive metadata parsing operations."""
    # Placeholder for expensive parsing
    return {"length": len(content), "hash": content_hash}
