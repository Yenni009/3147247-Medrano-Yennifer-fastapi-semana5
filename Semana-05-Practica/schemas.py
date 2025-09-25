from pydantic import BaseModel
from typing import Literal

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRoleUpdate(BaseModel):
    role: Literal["user", "admin"]

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
