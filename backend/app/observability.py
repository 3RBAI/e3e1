"""Observability module for tracing and monitoring."""

import logging
import os
from functools import wraps
from typing import Any, Callable, Literal, TypeVar, cast

logger = logging.getLogger(__name__)

# Type variable for decorators
F = TypeVar('F', bound=Callable[..., Any])

# Check if we're in debug mode
_DEBUG_MODE = os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes')


def observe(
    name: str | None = None,
    ignore_input: bool = False,
    ignore_output: bool = False,
    metadata: dict[str, Any] | None = None,
    span_type: Literal['DEFAULT', 'LLM', 'TOOL'] = 'DEFAULT',
    **kwargs: Any,
) -> Callable[[F], F]:
    """Observability decorator for tracing function execution.
    
    This is a simplified version that logs function calls.
    Can be extended to integrate with tracing systems like OpenTelemetry.
    
    Args:
        name: Name of the span/trace
        ignore_input: Whether to ignore function input parameters
        ignore_output: Whether to ignore function output
        metadata: Additional metadata
        span_type: Type of span (DEFAULT, LLM, TOOL)
        **kwargs: Additional parameters
        
    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        import asyncio
        
        @wraps(func)
        async def async_wrapper(*args, **func_kwargs):
            span_name = name or func.__name__
            logger.debug(f'[{span_type}] Starting: {span_name}')
            
            try:
                result = await func(*args, **func_kwargs)
                logger.debug(f'[{span_type}] Completed: {span_name}')
                return result
            except Exception as e:
                logger.error(f'[{span_type}] Error in {span_name}: {e}')
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **func_kwargs):
            span_name = name or func.__name__
            logger.debug(f'[{span_type}] Starting: {span_name}')
            
            try:
                result = func(*args, **func_kwargs)
                logger.debug(f'[{span_type}] Completed: {span_name}')
                return result
            except Exception as e:
                logger.error(f'[{span_type}] Error in {span_name}: {e}')
                raise
        
        if asyncio.iscoroutinefunction(func):
            return cast(F, async_wrapper)
        else:
            return cast(F, sync_wrapper)
    
    return decorator


def observe_debug(
    name: str | None = None,
    ignore_input: bool = False,
    ignore_output: bool = False,
    metadata: dict[str, Any] | None = None,
    span_type: Literal['DEFAULT', 'LLM', 'TOOL'] = 'DEFAULT',
    **kwargs: Any,
) -> Callable[[F], F]:
    """Debug-only observability decorator.
    
    Only traces when in debug mode.
    
    Args:
        name: Name of the span/trace
        ignore_input: Whether to ignore function input parameters
        ignore_output: Whether to ignore function output
        metadata: Additional metadata
        span_type: Type of span (DEFAULT, LLM, TOOL)
        **kwargs: Additional parameters
        
    Returns:
        Decorated function
    """
    if _DEBUG_MODE:
        return observe(name, ignore_input, ignore_output, metadata, span_type, **kwargs)
    
    # No-op decorator when not in debug mode
    def decorator(func: F) -> F:
        return func
    
    return decorator
