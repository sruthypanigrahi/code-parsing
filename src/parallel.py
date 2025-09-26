"""Parallel processing utilities for USB PD Parser."""

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Callable, Iterator, Optional, TypeVar
import multiprocessing

T = TypeVar('T')
R = TypeVar('R')


def parallel_map_io(func: Callable[[T], R], items: List[T], workers: int = 4) -> List[R]:
    """Parallel map for I/O-bound tasks using threads."""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(func, items))


def parallel_map_cpu(func: Callable[[T], R], items: List[T], workers: Optional[int] = None) -> List[R]:
    """Parallel map for CPU-bound tasks using processes."""
    if workers is None:
        workers = multiprocessing.cpu_count()
    
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(func, items))


def stream_parallel_io(func: Callable[[T], R], items: Iterator[T], workers: int = 4) -> Iterator[R]:
    """Stream parallel processing for I/O-bound tasks."""
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit tasks in batches to avoid memory issues
        batch_size = workers * 2
        batch: List[T] = []
        
        for item in items:
            batch.append(item)
            if len(batch) >= batch_size:
                futures = [executor.submit(func, item) for item in batch]
                for future in futures:
                    yield future.result()
                batch = []
        
        # Process remaining items
        if batch:
            futures = [executor.submit(func, item) for item in batch]
            for future in futures:
                yield future.result()