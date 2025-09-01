"""
Foundation Project - Cache Management
Redis cache utilities and management
"""

import json
import pickle
from typing import Any, Optional, Union
from datetime import timedelta
import redis
from redis.exceptions import RedisError

from .config import settings
from .logging import get_logger

logger = get_logger(__name__)

class CacheManager:
    """Redis cache manager for the Foundation Project"""
    
    def __init__(self):
        self.redis_client = None
        self._connect()
    
    def _connect(self):
        """Connect to Redis"""
        try:
            self.redis_client = redis.Redis(
                host=settings.redis.host,
                port=settings.redis.port,
                db=settings.redis.db,
                password=settings.redis.password.get_secret_value() if settings.redis.password else None,
                decode_responses=False,  # Keep as bytes for pickle support
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            self.redis_client.ping()
            logger.info("Redis cache connected successfully")
            
        except RedisError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis_client = None
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.ping()
            return True
        except RedisError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from cache
        
        Args:
            key: Cache key
            default: Default value if key not found
            
        Returns:
            Cached value or default
        """
        if not self.is_connected():
            return default
        
        try:
            value = self.redis_client.get(key)
            if value is None:
                return default
            
            # Try to deserialize
            try:
                return pickle.loads(value)
            except (pickle.PickleError, TypeError):
                # Fallback to JSON
                try:
                    return json.loads(value.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    return value.decode('utf-8')
                    
        except RedisError as e:
            logger.error(f"Redis get error: {e}")
            return default
    
    def set(self, key: str, value: Any, expire: Optional[Union[int, timedelta]] = None) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds or timedelta
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            # Serialize value
            if isinstance(value, (str, int, float, bool, type(None))):
                # Simple types can be JSON serialized
                serialized_value = json.dumps(value).encode('utf-8')
            else:
                # Complex types use pickle
                serialized_value = pickle.dumps(value)
            
            # Set with expiration
            if expire:
                if isinstance(expire, timedelta):
                    expire = int(expire.total_seconds())
                self.redis_client.setex(key, expire, serialized_value)
            else:
                self.redis_client.set(key, serialized_value)
            
            return True
            
        except RedisError as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete key from cache
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            result = self.redis_client.delete(key)
            return result > 0
            
        except RedisError as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache
        
        Args:
            key: Cache key to check
            
        Returns:
            True if key exists, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            return bool(self.redis_client.exists(key))
            
        except RedisError as e:
            logger.error(f"Redis exists error: {e}")
            return False
    
    def expire(self, key: str, seconds: int) -> bool:
        """
        Set expiration for a key
        
        Args:
            key: Cache key
            seconds: Expiration time in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            return bool(self.redis_client.expire(key, seconds))
            
        except RedisError as e:
            logger.error(f"Redis expire error: {e}")
            return False
    
    def ttl(self, key: str) -> int:
        """
        Get time to live for a key
        
        Args:
            key: Cache key
            
        Returns:
            TTL in seconds, -1 if no expiration, -2 if key doesn't exist
        """
        if not self.is_connected():
            return -2
        
        try:
            return self.redis_client.ttl(key)
            
        except RedisError as e:
            logger.error(f"Redis TTL error: {e}")
            return -2
    
    def clear_pattern(self, pattern: str) -> int:
        """
        Clear keys matching a pattern
        
        Args:
            pattern: Redis pattern (e.g., "user:*")
            
        Returns:
            Number of keys deleted
        """
        if not self.is_connected():
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
            
        except RedisError as e:
            logger.error(f"Redis clear pattern error: {e}")
            return 0
    
    def get_stats(self) -> dict:
        """
        Get Redis statistics
        
        Returns:
            Dictionary with Redis stats
        """
        if not self.is_connected():
            return {"error": "Redis not connected"}
        
        try:
            info = self.redis_client.info()
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "uptime_in_seconds": info.get("uptime_in_seconds", 0)
            }
            
        except RedisError as e:
            logger.error(f"Redis info error: {e}")
            return {"error": str(e)}
    
    def close(self):
        """Close Redis connection"""
        if self.redis_client:
            try:
                self.redis_client.close()
                logger.info("Redis cache connection closed")
            except RedisError as e:
                logger.error(f"Error closing Redis connection: {e}")

# Global cache instance
cache = CacheManager()

# Convenience functions
def get_cache() -> CacheManager:
    """Get cache manager instance"""
    return cache

def cache_get(key: str, default: Any = None) -> Any:
    """Get value from cache"""
    return cache.get(key, default)

def cache_set(key: str, value: Any, expire: Optional[Union[int, timedelta]] = None) -> bool:
    """Set value in cache"""
    return cache.set(key, value, expire)

def cache_delete(key: str) -> bool:
    """Delete key from cache"""
    return cache.delete(key)

def cache_exists(key: str) -> bool:
    """Check if key exists in cache"""
    return cache.exists(key)
