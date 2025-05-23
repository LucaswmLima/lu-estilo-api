from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.auth import UserCreate, UserOut, Token
from app.models.user import User
from app.db.database import get_db
from app.services.auth_service import (
    authenticate_user,
    create_user,
    generate_tokens,
    refresh_tokens,
    get_current_user,
    require_admin,
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.email, user.password)
    return new_user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, refresh_token = generate_tokens(user.email)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.delete("/user/delete", status_code=204)
def delete_current_user(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    db.delete(current_user)
    db.commit()
    return None

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str = Body(...)):
    access_token, new_refresh_token = refresh_tokens(refresh_token)
    if not access_token or not new_refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
