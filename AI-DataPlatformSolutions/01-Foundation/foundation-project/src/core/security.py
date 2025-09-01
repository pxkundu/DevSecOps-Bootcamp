"""
Foundation Project - Security Module
JWT token handling, password hashing, and security utilities
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext

from .config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        data: Data to encode in token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.security.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire, "type": "access"})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.security.secret_key.get_secret_value(), 
        algorithm=settings.security.algorithm
    )
    
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT refresh token
    
    Args:
        data: Data to encode in token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.security.refresh_token_expire_days
        )
    
    to_encode.update({"exp": expire, "type": "refresh"})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.security.secret_key.get_secret_value(), 
        algorithm=settings.security.algorithm
    )
    
    return encoded_jwt

def verify_token(token: str, is_refresh: bool = False) -> Dict[str, Any]:
    """
    Verify JWT token and return payload
    
    Args:
        token: JWT token to verify
        is_refresh: Whether this is a refresh token
        
    Returns:
        Token payload
        
    Raises:
        jwt.InvalidTokenError: If token is invalid
        jwt.ExpiredSignatureError: If token has expired
    """
    try:
        payload = jwt.decode(
            token, 
            settings.security.secret_key.get_secret_value(), 
            algorithms=[settings.security.algorithm]
        )
        
        # Check token type
        token_type = payload.get("type")
        if is_refresh and token_type != "refresh":
            raise jwt.InvalidTokenError("Invalid token type: expected refresh token")
        elif not is_refresh and token_type != "access":
            raise jwt.InvalidTokenError("Invalid token type: expected access token")
        
        return payload
        
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise jwt.InvalidTokenError(f"Invalid token: {e}")

def get_password_hash(password: str) -> str:
    """
    Hash password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to check against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def generate_secure_password(length: int = 16) -> str:
    """
    Generate secure random password
    
    Args:
        length: Length of password to generate
        
    Returns:
        Secure random password
    """
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    # Ensure password contains at least one of each type
    if not any(c.islower() for c in password):
        password += secrets.choice(string.ascii_lowercase)
    if not any(c.isupper() for c in password):
        password += secrets.choice(string.ascii_uppercase)
    if not any(c.isdigit() for c in password):
        password += secrets.choice(string.digits)
    if not any(c in string.punctuation for c in password):
        password += secrets.choice(string.punctuation)
    
    return password

def hash_api_key(api_key: str) -> str:
    """
    Hash API key for storage
    
    Args:
        api_key: Plain text API key
        
    Returns:
        Hashed API key
    """
    return pwd_context.hash(api_key)

def verify_api_key(plain_api_key: str, hashed_api_key: str) -> bool:
    """
    Verify API key against hash
    
    Args:
        plain_api_key: Plain text API key to verify
        hashed_api_key: Hashed API key to check against
        
    Returns:
        True if API key matches, False otherwise
    """
    return pwd_context.verify(plain_api_key, hashed_api_key)

def generate_api_key(prefix: str = "fp", length: int = 32) -> str:
    """
    Generate secure API key
    
    Args:
        prefix: Prefix for API key
        length: Length of random part
        
    Returns:
        Generated API key
    """
    import secrets
    import string
    
    # Generate random part
    alphabet = string.ascii_letters + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    # Create API key with prefix
    api_key = f"{prefix}_{random_part}"
    
    return api_key

def validate_password_strength(password: str) -> Dict[str, Any]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        
    Returns:
        Dictionary with validation results
    """
    result = {
        "is_valid": True,
        "score": 0,
        "issues": [],
        "suggestions": []
    }
    
    # Check length
    if len(password) < 8:
        result["is_valid"] = False
        result["issues"].append("Password must be at least 8 characters long")
        result["suggestions"].append("Increase password length")
    
    # Check for different character types
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    # Calculate score
    if has_lower:
        result["score"] += 1
    if has_upper:
        result["score"] += 1
    if has_digit:
        result["score"] += 1
    if has_special:
        result["score"] += 1
    if len(password) >= 12:
        result["score"] += 1
    
    # Check for common patterns
    if password.lower() in ["password", "123456", "qwerty", "admin"]:
        result["is_valid"] = False
        result["issues"].append("Password is too common")
        result["suggestions"].append("Choose a more unique password")
    
    # Check for sequential characters
    if any(password[i:i+3] in "abcdefghijklmnopqrstuvwxyz" for i in range(len(password)-2)):
        result["score"] -= 1
        result["suggestions"].append("Avoid sequential characters")
    
    # Check for repeated characters
    if any(password[i] == password[i+1] for i in range(len(password)-1)):
        result["score"] -= 1
        result["suggestions"].append("Avoid repeated characters")
    
    # Determine strength level
    if result["score"] <= 2:
        result["strength"] = "weak"
        result["is_valid"] = False
    elif result["score"] <= 3:
        result["strength"] = "fair"
    elif result["score"] <= 4:
        result["strength"] = "good"
    else:
        result["strength"] = "strong"
    
    return result

def sanitize_input(input_string: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        input_string: Input string to sanitize
        
    Returns:
        Sanitized string
    """
    import html
    
    # HTML escape
    sanitized = html.escape(input_string)
    
    # Remove potential script tags
    sanitized = sanitized.replace("<script", "&lt;script")
    sanitized = sanitized.replace("</script", "&lt;/script")
    
    # Remove potential SQL injection patterns
    sql_patterns = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
    for pattern in sql_patterns:
        sanitized = sanitized.replace(pattern, '')
    
    return sanitized

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email to validate
        
    Returns:
        True if email is valid, False otherwise
    """
    import re
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_csrf_token() -> str:
    """
    Generate CSRF token
    
    Returns:
        Generated CSRF token
    """
    import secrets
    
    return secrets.token_urlsafe(32)

def verify_csrf_token(token: str, stored_token: str) -> bool:
    """
    Verify CSRF token
    
    Args:
        token: Token to verify
        stored_token: Stored token to check against
        
    Returns:
        True if tokens match, False otherwise
    """
    return secrets.compare_digest(token, stored_token)

# Rate limiting utilities
class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed
        
        Args:
            identifier: Unique identifier (e.g., IP address, user ID)
            
        Returns:
            True if request is allowed, False otherwise
        """
        now = datetime.utcnow()
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Remove old requests outside the window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if (now - req_time).total_seconds() < self.window_seconds
        ]
        
        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True
        
        return False
    
    def get_remaining_requests(self, identifier: str) -> int:
        """
        Get remaining requests for identifier
        
        Args:
            identifier: Unique identifier
            
        Returns:
            Number of remaining requests
        """
        now = datetime.utcnow()
        
        if identifier not in self.requests:
            return self.max_requests
        
        # Remove old requests outside the window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if (now - req_time).total_seconds() < self.window_seconds
        ]
        
        return max(0, self.max_requests - len(self.requests[identifier]))

# Global rate limiter instance
rate_limiter = RateLimiter()

def check_rate_limit(identifier: str) -> bool:
    """
    Check rate limit for identifier
    
    Args:
        identifier: Unique identifier
        
    Returns:
        True if within rate limit, False otherwise
    """
    return rate_limiter.is_allowed(identifier)

def get_rate_limit_info(identifier: str) -> Dict[str, Any]:
    """
    Get rate limit information for identifier
    
    Args:
        identifier: Unique identifier
        
    Returns:
        Dictionary with rate limit information
    """
    remaining = rate_limiter.get_remaining_requests(identifier)
    
    return {
        "remaining_requests": remaining,
        "max_requests": rate_limiter.max_requests,
        "window_seconds": rate_limiter.window_seconds,
        "reset_time": datetime.utcnow() + timedelta(seconds=rate_limiter.window_seconds)
    }
