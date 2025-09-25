from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# -------- Users --------
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    role: str

    class Config:
        from_attributes = True  # equivalente a orm_mode=True en Pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRoleUpdate(BaseModel):
    role: str  # "admin" | "user" (si quieres, cámbialo a Enum)

# Posts 
class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
 