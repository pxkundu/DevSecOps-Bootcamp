"""
Foundation Project - API Routers
API route handlers for different domains
"""

from . import auth
from . import users
from . import data
from . import ml
from . import health
from . import monitoring
from . import admin

__all__ = [
    "auth",
    "users",
    "data", 
    "ml",
    "health",
    "monitoring",
    "admin"
]
