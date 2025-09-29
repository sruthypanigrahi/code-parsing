"""Async processing utilities for improved performance."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class AsyncProcessor:
    """Async processor for CPU and I/O bound tasks."""

    def __init__(self, max_workers: Optional[int] = None):
        self.max_workers = max_workers or 4
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

    async def process_batch_async(
        self, func: Callable[[T], R], items: list[T], batch_size: int = 10
    ) -> list[R]:
        """Process items in batches asynchronously."""
        results = []

        for i in range(0, len(items), batch_size):
            batch = items[i : i + batch_size]
            batch_tasks = [
                asyncio.get_event_loop().run_in_executor(self.executor, func, item)
                for item in batch
            ]
            batch_results = await asyncio.gather(*batch_tasks)
            results.extend(batch_results)

        return results

    async def process_files_async(
        self, file_processor: Callable[[Path], Any], file_paths: list[Path]
    ) -> list[Any]:
        """Process multiple files asynchronously."""
        tasks = [
            asyncio.get_event_loop().run_in_executor(
                self.executor, file_processor, path
            )
            for path in file_paths
        ]
        return await asyncio.gather(*tasks)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.executor.shutdown(wait=True)


def async_timer(func: Callable) -> Callable:
    """Decorator for timing async functions."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        import time

        start = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end = time.time()
            print(f"{func.__name__} took {end - start:.2f} seconds")

    return wrapper


async def run_with_timeout(coro, timeout_seconds: int = 300):
    """Run coroutine with timeout."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout_seconds)
    except asyncio.TimeoutError:
        from .exceptions import ProcessingTimeoutError

        raise ProcessingTimeoutError(
            f"Operation timed out after {timeout_seconds} seconds"
        )
