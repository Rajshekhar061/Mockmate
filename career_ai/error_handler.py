"""
Error handling and utility functions for CareerAI.
"""

import logging
from typing import Tuple, Dict, Any
from django.http import JsonResponse
from django.contrib import messages

logger = logging.getLogger(__name__)


class APIError(Exception):
    """
    Custom exception for API errors.
    """
    def __init__(self, message: str, status_code: int = 400, details: str = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class ValidationError(APIError):
    """
    Custom exception for validation errors.
    """
    def __init__(self, message: str, details: str = None):
        super().__init__(message, status_code=400, details=details)


class AuthenticationError(APIError):
    """
    Custom exception for authentication errors.
    """
    def __init__(self, message: str = "Authentication required", details: str = None):
        super().__init__(message, status_code=401, details=details)


class FileUploadError(APIError):
    """
    Custom exception for file upload errors.
    """
    def __init__(self, message: str, details: str = None):
        super().__init__(message, status_code=400, details=details)


def handle_api_error(error: APIError) -> JsonResponse:
    """
    Convert APIError to JSON response.
    
    Args:
        error (APIError): The error to handle
        
    Returns:
        JsonResponse: JSON response with error details
    """
    response_data = {
        'error': True,
        'message': error.message,
    }
    
    if error.details:
        response_data['details'] = error.details
    
    return JsonResponse(response_data, status=error.status_code)


def log_error(logger_obj: logging.Logger, error: Exception, context: str = ""):
    """
    Log an error with context.
    
    Args:
        logger_obj (logging.Logger): Logger instance
        error (Exception): The exception to log
        context (str): Additional context about where the error occurred
    """
    error_msg = f"{context}: {str(error)}" if context else str(error)
    logger_obj.error(error_msg, exc_info=True)


def safe_file_operation(operation_func) -> Tuple[bool, Any, str]:
    """
    Safely execute a file operation with error handling.
    
    Args:
        operation_func: Function to execute
        
    Returns:
        Tuple[bool, Any, str]: (success, result, error_message)
    """
    try:
        result = operation_func()
        return True, result, None
    except FileNotFoundError as e:
        error_msg = f"File not found: {str(e)}"
        logger.error(error_msg)
        return False, None, error_msg
    except PermissionError as e:
        error_msg = f"Permission denied: {str(e)}"
        logger.error(error_msg)
        return False, None, error_msg
    except Exception as e:
        error_msg = f"File operation failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, None, error_msg


def validate_file_upload(file, max_size: int, allowed_types: list) -> Tuple[bool, str]:
    """
    Validate uploaded file.
    
    Args:
        file: The file to validate
        max_size (int): Maximum file size in bytes
        allowed_types (list): List of allowed MIME types
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not file:
        return False, "No file provided."
    
    # Check file size
    if file.size > max_size:
        size_mb = max_size / (1024 * 1024)
        return False, f"File size exceeds {size_mb}MB limit."
    
    # Check file type
    if file.content_type not in allowed_types:
        allowed = ", ".join(allowed_types)
        return False, f"File type not allowed. Allowed types: {allowed}"
    
    return True, ""


def get_error_message(error: Exception, default: str = "An error occurred") -> str:
    """
    Extract user-friendly error message from exception.
    
    Args:
        error (Exception): The exception
        default (str): Default message if error message is empty
        
    Returns:
        str: User-friendly error message
    """
    if hasattr(error, 'message'):
        return error.message
    
    error_str = str(error)
    return error_str if error_str else default
