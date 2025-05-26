from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_admin: Optional[int] = 0


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: int
    is_admin: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"