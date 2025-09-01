"""
Foundation Project - Database Connection
Database connection management and session handling
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging

from ..core.config import settings

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    f"postgresql://{settings.database.user}:{settings.database.password.get_secret_value()}@"
    f"{settings.database.host}:{settings.database.port}/{settings.database.name}",
    poolclass=QueuePool,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    echo=settings.database.echo,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

def get_db() -> Session:
    """
    Get database session
    
    Returns:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context() -> Session:
    """
    Get database session context manager
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db() -> None:
    """Initialize database tables"""
    try:
        # Import all models to ensure they are registered
        from . import models
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def check_db_connection() -> bool:
    """
    Check database connection
    
    Returns:
        True if connection is successful, False otherwise
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False

def get_db_stats() -> dict:
    """
    Get database statistics
    
    Returns:
        Dictionary with database statistics
    """
    try:
        with engine.connect() as connection:
            # Get connection pool stats
            pool = engine.pool
            stats = {
                "pool_size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "invalid": pool.invalid()
            }
            
            # Get database size
            result = connection.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
            db_size = result.scalar()
            stats["database_size"] = db_size
            
            return stats
            
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {"error": str(e)}

def close_db_connections() -> None:
    """Close all database connections"""
    try:
        engine.dispose()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Failed to close database connections: {e}")
