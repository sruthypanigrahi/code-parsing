"""Caching utilities for performance optimization."""

import hashlib
import json
import pickle
from pathlib import Path
from typing import Any, Optional, TypeVar, Callable
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class FileCache:
    """Simple file-based cache for expensive operations."""

    def __init__(self, cache_dir: Path = Path(".cache")) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(self, *args: Any, **kwargs: Any) -> str:
        """Generate cache key from arguments."""
        key_data = json.dumps([args, kwargs], sort_keys=True, default=str)
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        cache_file = self.cache_dir / f"{key}.pkl"
        if cache_file.exists():
            try:
                with open(cache_file, "rb") as f:
                    return pickle.load(f)
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
        return None

    def set(self, key: str, value: Any) -> None:
        """Set cached value."""
        cache_file = self.cache_dir / f"{key}.pkl"
        try:
            with open(cache_file, "wb") as f:
                pickle.dump(value, f)
        except Exception as e:
            logger.warning(f"Cache write error: {e}")

    def cached(self, func: Callable[..., T]) -> Callable[..., T]:
        """Decorator for caching function results."""

        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = self._get_cache_key(func.__name__, *args, **kwargs)
            result = self.get(key)
            if result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return result

            result = func(*args, **kwargs)
            self.set(key, result)
            logger.debug(f"Cache miss for {func.__name__}")
            return result

        return wrapper


# Global cache instance
cache = FileCache()
