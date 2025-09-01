"""
Foundation Project - Enterprise AI-Data Platform
A comprehensive, production-ready implementation of enterprise AI-Data platform fundamentals
"""

__version__ = "1.0.0"
__author__ = "Foundation Project Team"
__description__ = "Enterprise AI-Data Platform Foundation"

from . import api
from . import core
from . import data
from . import ml
from . import services
from . import utils

__all__ = [
    "api",
    "core", 
    "data",
    "ml",
    "services",
    "utils"
]
