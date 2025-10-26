"""Utility functions for the backend."""

import asyncio
import logging
import time
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar

logger = logging.getLogger(__name__)

# Type variables for decorators
R = TypeVar('R')
P = ParamSpec('P')


def time_execution_sync(func_name: str = '') -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to time synchronous function execution.
    
    Args:
        func_name: Optional name to display in logs
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            if execution_time > 0.25:
                name = func_name or func.__name__
                logger.debug(f'⏳ {name}() took {execution_time:.2f}s')
            
            return result
        return wrapper
    return decorator


def time_execution_async(func_name: str = '') -> Callable:
    """Decorator to time asynchronous function execution.
    
    Args:
        func_name: Optional name to display in logs
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            if execution_time > 0.25:
                name = func_name or func.__name__
                logger.debug(f'⏳ {name}() took {execution_time:.2f}s')
            
            return result
        return wrapper
    return decorator


def validate_file_extension(filename: str, allowed_extensions: list[str]) -> bool:
    """Validate file extension.
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions (e.g., ['.pdf', '.txt'])
        
    Returns:
        True if extension is allowed, False otherwise
    """
    from pathlib import Path
    
    ext = Path(filename).suffix.lower()
    return ext in allowed_extensions


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
