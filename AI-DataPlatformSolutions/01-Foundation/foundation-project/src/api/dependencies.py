"""
Foundation Project - API Dependencies
Common dependencies used across API endpoints
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ..core.security import get_current_user, get_current_superuser
from ..data.database import get_db
from ..data.models import User, Role, UserRole
from ..core.logging import get_logger

logger = get_logger(__name__)

# Database dependency
def get_database() -> Session:
    """Get database session"""
    return Depends(get_db)

# Authentication dependencies
def get_authenticated_user() -> User:
    """Get current authenticated user"""
    return Depends(get_current_user)

def get_superuser() -> User:
    """Get current superuser"""
    return Depends(get_current_superuser)

# Role-based access control
def require_role(role_name: str):
    """
    Dependency to require a specific role
    
    Args:
        role_name: Name of the required role
        
    Returns:
        Dependency function
    """
    def role_checker(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        # Check if user has the required role
        user_role = db.query(UserRole).join(Role).filter(
            UserRole.user_id == current_user.id,
            Role.name == role_name
        ).first()
        
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role_name}' required"
            )
        
        return current_user
    
    return role_checker

def require_permission(permission_name: str):
    """
    Dependency to require a specific permission
    
    Args:
        permission_name: Name of the required permission
        
    Returns:
        Dependency function
    """
    def permission_checker(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        # Check if user has the required permission
        # This is a simplified implementation - you might want to implement
        # a more sophisticated permission system
        
        if not current_user.is_superuser:
            # For now, only superusers have all permissions
            # In a real implementation, you'd check specific permissions
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission_name}' required"
            )
        
        return current_user
    
    return permission_checker

# Resource ownership check
def check_resource_ownership(resource_model, resource_id_field: str = "id"):
    """
    Dependency to check if the current user owns a resource
    
    Args:
        resource_model: SQLAlchemy model class
        resource_id_field: Field name for the resource ID
        
    Returns:
        Dependency function
    """
    def ownership_checker(
        resource_id: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        # Query the resource
        resource = db.query(resource_model).filter(
            getattr(resource_model, resource_id_field) == resource_id
        ).first()
        
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        # Check ownership
        if hasattr(resource, 'owner_id') and resource.owner_id != current_user.id:
            if not current_user.is_superuser:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied - resource ownership required"
                )
        
        return resource
    
    return ownership_checker

# Rate limiting dependency
def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """
    Dependency for rate limiting
    
    Args:
        max_requests: Maximum requests allowed in the time window
        window_seconds: Time window in seconds
        
    Returns:
        Dependency function
    """
    def rate_limiter(current_user: User = Depends(get_current_user)):
        # This is a simplified rate limiter
        # In production, you'd want to use Redis or a similar solution
        # to track requests across multiple instances
        
        # For now, just return the user
        # TODO: Implement actual rate limiting logic
        return current_user
    
    return rate_limiter

# Pagination dependency
def get_pagination_params(
    skip: int = 0,
    limit: int = 100,
    max_limit: int = 1000
):
    """
    Dependency for pagination parameters
    
    Args:
        skip: Number of items to skip
        limit: Number of items to return
        max_limit: Maximum allowed limit
        
    Returns:
        Pagination parameters
    """
    if limit > max_limit:
        limit = max_limit
    
    if skip < 0:
        skip = 0
    
    if limit < 1:
        limit = 1
    
    return {"skip": skip, "limit": limit}

# Common response models
def create_paginated_response(items: list, total: int, skip: int, limit: int):
    """
    Create a paginated response
    
    Args:
        items: List of items
        total: Total number of items
        skip: Number of items skipped
        limit: Number of items returned
        
    Returns:
        Paginated response dictionary
    """
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total,
        "page": (skip // limit) + 1,
        "total_pages": (total + limit - 1) // limit
    }
