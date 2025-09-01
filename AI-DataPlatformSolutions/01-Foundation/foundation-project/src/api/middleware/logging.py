"""
Foundation Project - Request Logging Middleware
Logs all HTTP requests with correlation IDs and timing
"""

import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from ...core.logging import get_logger
from ...core.metrics import record_http_request

logger = get_logger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests with correlation IDs"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        
        # Add correlation ID to response headers
        start_time = time.time()
        
        # Log request start
        logger.info(
            "HTTP request started",
            correlation_id=correlation_id,
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            content_length=request.headers.get("content-length")
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log request completion
            logger.info(
                "HTTP request completed",
                correlation_id=correlation_id,
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                duration=duration,
                content_length=response.headers.get("content-length")
            )
            
            # Record metrics
            record_http_request(
                method=request.method,
                endpoint=str(request.url.path),
                status=response.status_code,
                duration=duration,
                request_size=int(request.headers.get("content-length", 0)) if request.headers.get("content-length") else None,
                response_size=int(response.headers.get("content-length", 0)) if response.headers.get("content-length") else None
            )
            
            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id
            
            return response
            
        except Exception as e:
            # Calculate duration
            duration = time.time() - start_time
            
            # Log request error
            logger.error(
                "HTTP request failed",
                correlation_id=correlation_id,
                method=request.method,
                url=str(request.url),
                error=str(e),
                duration=duration,
                exc_info=True
            )
            
            # Record metrics for failed request
            record_http_request(
                method=request.method,
                endpoint=str(request.url.path),
                status=500,
                duration=duration
            )
            
            raise
