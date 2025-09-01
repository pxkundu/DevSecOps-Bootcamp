"""
Foundation Project - Users Router
User management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ...core.security import get_current_user, get_current_superuser
from ...data.database import get_db
from ...data.models import User, AuditLog
from ...core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Pydantic models
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None

class UserListResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

@router.get("/users", response_model=List[UserListResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """List all users (superuser only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/me", response_model=UserListResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.put("/users/me", response_model=UserListResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    try:
        if user_update.full_name is not None:
            current_user.full_name = user_update.full_name
        
        if user_update.email is not None:
            # Check if email is already taken
            existing_user = db.query(User).filter(
                User.email == user_update.email,
                User.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            current_user.email = user_update.email
        
        db.commit()
        db.refresh(current_user)
        
        # Log the update
        audit_log = AuditLog(
            user_id=current_user.id,
            action="user_updated",
            resource_type="user",
            resource_id=current_user.id,
            details={"updated_fields": user_update.dict(exclude_unset=True)}
        )
        db.add(audit_log)
        db.commit()
        
        logger.info(f"User updated: {current_user.username}")
        return current_user
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user"
        )

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """Delete a user (superuser only)"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete yourself"
            )
        
        # Log the deletion
        audit_log = AuditLog(
            user_id=current_user.id,
            action="user_deleted",
            resource_type="user",
            resource_id=user_id,
            details={"deleted_username": user.username}
        )
        db.add(audit_log)
        
        # Delete the user
        db.delete(user)
        db.commit()
        
        logger.info(f"User deleted: {user.username}")
        return {"message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )
