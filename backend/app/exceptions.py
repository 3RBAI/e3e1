"""Custom exceptions for the application."""

from typing import Any


class AppException(Exception):
    """Base exception for application errors."""
    
    def __init__(self, status_code: int, message: str, details: Any = None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(f'Error {status_code}: {message}')


class LLMException(AppException):
    """Exception for LLM-related errors."""
    
    def __init__(self, status_code: int, message: str, details: Any = None):
        super().__init__(status_code, message, details)


class ValidationException(AppException):
    """Exception for validation errors."""
    
    def __init__(self, message: str, details: Any = None):
        super().__init__(400, message, details)


class AuthenticationException(AppException):
    """Exception for authentication errors."""
    
    def __init__(self, message: str = 'Authentication failed', details: Any = None):
        super().__init__(401, message, details)


class NotFoundException(AppException):
    """Exception for not found errors."""
    
    def __init__(self, message: str = 'Resource not found', details: Any = None):
        super().__init__(404, message, details)
