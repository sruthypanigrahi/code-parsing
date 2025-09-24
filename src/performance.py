"""Performance monitoring and optimization utilities."""

import time
import functools
from typing import Callable, Any



class PerformanceMonitor:
    """Monitor and log performance metrics for PDF processing operations.
    
    This class implements the Observer pattern to track execution times
    and memory usage across different components.
    """
    
    def __init__(self):
        self._metrics: dict[str, float] = {}
    
    def time_operation(self, operation_name: str):
        """Decorator to time function execution.
        
        Args:
            operation_name: Name of the operation being timed
            
        Returns:
            Decorated function with timing capability
        """
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                
                execution_time = end_time - start_time
                self._metrics[operation_name] = execution_time
                
                return result
            return wrapper
        return decorator
    
    def get_metrics(self) -> dict[str, float]:
        """Get collected performance metrics.
        
        Returns:
            Dictionary of operation names and execution times
        """
        return self._metrics.copy()
    
    def log_metrics(self, logger: Any) -> None:
        """Log performance metrics.
        
        Args:
            logger: Logger instance to use for output
        """
        for operation, time_taken in self._metrics.items():
            logger.info(f"Performance - {operation}: {time_taken:.3f}s")


class MemoryOptimizer:
    """Memory optimization utilities for large PDF processing.
    
    Implements strategies to reduce memory footprint during processing.
    """
    
    @staticmethod
    def process_in_chunks(items: list[Any], chunk_size: int = 100):
        """Process items in chunks to reduce memory usage.
        
        Args:
            items: List of items to process
            chunk_size: Size of each processing chunk
            
        Yields:
            Chunks of items for processing
        """
        for i in range(0, len(items), chunk_size):
            yield items[i:i + chunk_size]
    
    @staticmethod
    def cleanup_resources(*resources: Any) -> None:
        """Clean up resources to free memory.
        
        Args:
            *resources: Resources to clean up (files, connections, etc.)
        """
        for resource in resources:
            if hasattr(resource, 'close'):
                resource.close()