"""Logging configuration for the FastAPI backend."""

import logging
import sys
from pathlib import Path
from typing import Optional

from backend.app.config import CONFIG


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """Setup logging configuration.
    
    Args:
        log_level: Override log level (default: uses CONFIG.LOG_LEVEL)
        log_file: Path to log file (optional)
        
    Returns:
        Configured logger instance
    """
    level_str = (log_level or CONFIG.LOG_LEVEL).upper()
    level = getattr(logging, level_str, logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = []
    root_logger.addHandler(console_handler)
    
    # Setup file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Setup app logger
    app_logger = logging.getLogger('backend')
    app_logger.setLevel(level)
    
    # Silence noisy third-party loggers
    for logger_name in ['httpx', 'httpcore', 'urllib3', 'asyncio']:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
    
    return app_logger


# Initialize logging
logger = setup_logging()
