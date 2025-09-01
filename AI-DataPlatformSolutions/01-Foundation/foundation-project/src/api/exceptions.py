"""
Foundation Project - Custom Exceptions
Custom exception classes for the API
"""

from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class FoundationProjectException(HTTPException):
    """Base exception for Foundation Project"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class ValidationException(FoundationProjectException):
    """Exception for validation errors"""
    
    def __init__(self, detail: str, field: Optional[str] = None):
        if field:
            detail = f"Validation error in field '{field}': {detail}"
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

class AuthenticationException(FoundationProjectException):
    """Exception for authentication errors"""
    
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationException(FoundationProjectException):
    """Exception for authorization errors"""
    
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class ResourceNotFoundException(FoundationProjectException):
    """Exception for resource not found"""
    
    def __init__(self, resource_type: str, resource_id: str):
        detail = f"{resource_type} with id '{resource_id}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class ResourceConflictException(FoundationProjectException):
    """Exception for resource conflicts"""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

class RateLimitException(FoundationProjectException):
    """Exception for rate limiting"""
    
    def __init__(self, retry_after: int = 60):
        headers = {"Retry-After": str(retry_after)}
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
            headers=headers
        )

class ServiceUnavailableException(FoundationProjectException):
    """Exception for service unavailability"""
    
    def __init__(self, detail: str = "Service temporarily unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )

class DatabaseException(FoundationProjectException):
    """Exception for database errors"""
    
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class ExternalServiceException(FoundationProjectException):
    """Exception for external service errors"""
    
    def __init__(self, service_name: str, detail: str):
        detail = f"External service '{service_name}' error: {detail}"
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail
        )

class ConfigurationException(FoundationProjectException):
    """Exception for configuration errors"""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration error: {detail}"
        )

class MLModelException(FoundationProjectException):
    """Exception for ML model errors"""
    
    def __init__(self, detail: str, model_id: Optional[str] = None):
        if model_id:
            detail = f"ML model '{model_id}' error: {detail}"
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class DataProcessingException(FoundationProjectException):
    """Exception for data processing errors"""
    
    def __init__(self, detail: str, operation: Optional[str] = None):
        if operation:
            detail = f"Data processing error in '{operation}': {detail}"
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

# Exception handlers
def handle_validation_error(exc: ValidationException):
    """Handle validation errors"""
    return {
        "error": "Validation Error",
        "detail": exc.detail,
        "status_code": exc.status_code
    }

def handle_authentication_error(exc: AuthenticationException):
    """Handle authentication errors"""
    return {
        "error": "Authentication Error",
        "detail": exc.detail,
        "status_code": exc.status_code
    }

def handle_authorization_error(exc: AuthorizationException):
    """Handle authorization errors"""
    return {
        "error": "Authorization Error",
        "detail": exc.detail,
        "status_code": exc.status_code
    }

def handle_resource_not_found(exc: ResourceNotFoundException):
    """Handle resource not found errors"""
    return {
        "error": "Resource Not Found",
        "detail": exc.detail,
        "status_code": exc.status_code
    }

def handle_rate_limit_error(exc: RateLimitException):
    """Handle rate limit errors"""
    return {
        "error": "Rate Limit Exceeded",
        "detail": exc.detail,
        "status_code": exc.status_code,
        "retry_after": exc.headers.get("Retry-After") if exc.headers else None
    }
