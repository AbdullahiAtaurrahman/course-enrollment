from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
     ADMIN = 'admin'
     STUDENT = 'student'

class UserBase(BaseModel):
    email: str
    name: str
    role: UserRole

class UserCreate(UserBase):
    pass

class User(UserCreate):
     id: str