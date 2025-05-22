from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: int
    is_admin: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
