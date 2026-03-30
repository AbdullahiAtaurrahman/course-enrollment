from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum


class UserRole(str, Enum):
    ADMIN = 'admin'
    STUDENT = 'student'


class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole

    @field_validator('name')
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('name must not be empty')
        return v


class UserCreate(UserBase):
    pass


class User(UserCreate):
    id: str
