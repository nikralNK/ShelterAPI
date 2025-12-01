from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    fullname: Optional[str] = None
    password: Optional[str] = None
    avatar: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
