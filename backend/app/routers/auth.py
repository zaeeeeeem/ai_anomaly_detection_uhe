from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import auth_service
from app.utils.dependencies import get_current_active_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    - **email**: Valid email address
    - **username**: Unique username (3-50 characters)
    - **password**: Strong password (minimum 8 characters)
    - **full_name**: Optional full name
    """
    user = auth_service.create_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and get access token

    - **email**: User's email
    - **password**: User's password

    Returns JWT access token for subsequent requests
    """
    token = auth_service.authenticate_user(db, credentials)
    return token


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user=Depends(get_current_active_user)):
    """Get current authenticated user information"""
    return current_user


@router.post("/logout")
def logout():
    """
    Logout endpoint (client should discard token)
    JWT tokens are stateless, so logout is handled client-side
    """
    return {"message": "Logged out successfully"}
