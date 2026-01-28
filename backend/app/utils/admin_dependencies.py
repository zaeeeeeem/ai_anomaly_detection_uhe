from fastapi import Depends, HTTPException, status
from app.models.user import User, UserRole
from app.utils.dependencies import get_current_active_user


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
