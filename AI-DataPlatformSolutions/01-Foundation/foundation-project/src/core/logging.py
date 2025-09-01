"""
Foundation Project - Logging Configuration
Structured logging with correlation IDs and formatting
"""

import logging
import sys
from typing import Optional
from structlog import configure, get_logger
from structlog.stdlib import LoggerFactory
from structlog.processors import (
    TimeStamper, 
    JSONRenderer, 
    add_log_level,
    StackInfoRenderer,
    format_exc_info
)

def setup_logging(
    log_level: str = "INFO",
    log_format: str = "json",
    enable_console: bool = True,
    enable_file: bool = False,
    log_file: str = "logs/foundation.log"
) -> None:
    """
    Setup structured logging for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log format (json, console)
        enable_console: Enable console logging
        enable_file: Enable file logging
        log_file: Log file path
    """
    
    # Configure standard library logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(message)s",
        handlers=[]
    )
    
    # Add console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        logging.getLogger().addHandler(console_handler)
    
    # Add file handler
    if enable_file:
        import os
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        logging.getLogger().addHandler(file_handler)
    
    # Configure structlog
    processors = [
        add_log_level,
        add_log_level,
        StackInfoRenderer(),
        format_exc_info,
        TimeStamper(fmt="iso"),
    ]
    
    if log_format == "json":
        processors.append(JSONRenderer())
    else:
        processors.append(format_exc_info)
    
    configure(
        processors=processors,
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=logging.BoundLogger,
        cache_logger_on_first_use=True,
    )

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name (defaults to calling module name)
        
    Returns:
        Configured logger instance
    """
    if name is None:
        import inspect
        name = inspect.getmodule(inspect.currentframe().f_back).__name__
    
    return get_logger(name)

def log_function_call(func_name: str, **kwargs):
    """
    Decorator to log function calls
    
    Args:
        func_name: Name of the function being called
        **kwargs: Function arguments to log
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            logger.info(
                f"Calling function: {func_name}",
                function=func_name,
                args=args,
                kwargs=kwargs
            )
            try:
                result = func(*args, **kwargs)
                logger.info(
                    f"Function {func_name} completed successfully",
                    function=func_name,
                    result=result
                )
                return result
            except Exception as e:
                logger.error(
                    f"Function {func_name} failed",
                    function=func_name,
                    error=str(e),
                    exc_info=True
                )
                raise
        return wrapper
    return decorator

# Initialize logging with default settings
setup_logging()
