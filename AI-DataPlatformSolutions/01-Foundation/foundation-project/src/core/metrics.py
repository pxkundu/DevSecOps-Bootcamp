"""
Foundation Project - Metrics Collection
Prometheus metrics and monitoring setup
"""

import time
from typing import Dict, Any, Optional
from prometheus_client import (
    Counter, 
    Histogram, 
    Gauge, 
    Summary,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry
)

# Create a custom registry for the application
registry = CollectorRegistry()

# HTTP metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status'],
    registry=registry
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    registry=registry
)

http_request_size_bytes = Histogram(
    'http_request_size_bytes',
    'HTTP request size in bytes',
    ['method', 'endpoint'],
    registry=registry
)

http_response_size_bytes = Histogram(
    'http_response_size_bytes',
    'HTTP response size in bytes',
    ['method', 'endpoint'],
    registry=registry
)

# Business metrics
user_registrations_total = Counter(
    'user_registrations_total',
    'Total user registrations',
    registry=registry
)

user_logins_total = Counter(
    'user_logins_total',
    'Total user logins',
    registry=registry
)

ml_model_training_total = Counter(
    'ml_model_training_total',
    'Total ML model training runs',
    ['model_type', 'algorithm'],
    registry=registry
)

ml_model_inference_total = Counter(
    'ml_model_inference_total',
    'Total ML model inference requests',
    ['model_type', 'algorithm'],
    registry=registry
)

# System metrics
active_users = Gauge(
    'active_users',
    'Number of currently active users',
    registry=registry
)

database_connections = Gauge(
    'database_connections',
    'Number of active database connections',
    registry=registry
)

redis_connections = Gauge(
    'redis_connections',
    'Number of active Redis connections',
    registry=registry
)

# Performance metrics
api_response_time = Summary(
    'api_response_time_seconds',
    'API response time in seconds',
    ['endpoint'],
    registry=registry
)

database_query_time = Summary(
    'database_query_time_seconds',
    'Database query time in seconds',
    ['query_type'],
    registry=registry
)

def setup_metrics() -> None:
    """Setup and initialize metrics collection"""
    # Initialize default values
    active_users.set(0)
    database_connections.set(0)
    redis_connections.set(0)

def record_http_request(method: str, endpoint: str, status: int, duration: float, 
                       request_size: Optional[int] = None, response_size: Optional[int] = None) -> None:
    """
    Record HTTP request metrics
    
    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint
        status: HTTP status code
        duration: Request duration in seconds
        request_size: Request size in bytes
        response_size: Response size in bytes
    """
    http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
    http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)
    
    if request_size:
        http_request_size_bytes.labels(method=method, endpoint=endpoint).observe(request_size)
    
    if response_size:
        http_response_size_bytes.labels(method=method, endpoint=endpoint).observe(response_size)

def record_user_registration() -> None:
    """Record a user registration"""
    user_registrations_total.inc()

def record_user_login() -> None:
    """Record a user login"""
    user_logins_total.inc()

def record_ml_training(model_type: str, algorithm: str) -> None:
    """
    Record ML model training
    
    Args:
        model_type: Type of ML model
        algorithm: Algorithm used
    """
    ml_model_training_total.labels(model_type=model_type, algorithm=algorithm).inc()

def record_ml_inference(model_type: str, algorithm: str) -> None:
    """
    Record ML model inference
    
    Args:
        model_type: Type of ML model
        algorithm: Algorithm used
    """
    ml_model_inference_total.labels(model_type=model_type, algorithm=algorithm).inc()

def update_active_users(count: int) -> None:
    """
    Update active users count
    
    Args:
        count: Number of active users
    """
    active_users.set(count)

def update_database_connections(count: int) -> None:
    """
    Update database connections count
    
    Args:
        count: Number of database connections
    """
    database_connections.set(count)

def update_redis_connections(count: int) -> None:
    """
    Update Redis connections count
    
    Args:
        count: Number of Redis connections
    """
    redis_connections.set(count)

def get_metrics() -> str:
    """
    Get metrics in Prometheus format
    
    Returns:
        Metrics in Prometheus text format
    """
    return generate_latest(registry)

def get_metrics_content_type() -> str:
    """
    Get metrics content type
    
    Returns:
        Content type for metrics
    """
    return CONTENT_TYPE_LATEST

# Decorator for timing functions
def time_function(metric_name: str, labels: Optional[Dict[str, str]] = None):
    """
    Decorator to time function execution and record metrics
    
    Args:
        metric_name: Name of the metric
        labels: Additional labels for the metric
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Record timing metric
                if labels:
                    # Create a summary metric for this function
                    func_timer = Summary(
                        f'{metric_name}_duration_seconds',
                        f'Duration of {metric_name}',
                        list(labels.keys()),
                        registry=registry
                    )
                    func_timer.labels(**labels).observe(duration)
                else:
                    func_timer = Summary(
                        f'{metric_name}_duration_seconds',
                        f'Duration of {metric_name}',
                        registry=registry
                    )
                    func_timer.observe(duration)
                
                return result
            except Exception as e:
                duration = time.time() - start_time
                
                # Record error metric
                error_counter = Counter(
                    f'{metric_name}_errors_total',
                    f'Total errors in {metric_name}',
                    registry=registry
                )
                error_counter.inc()
                
                raise
        return wrapper
    return decorator
