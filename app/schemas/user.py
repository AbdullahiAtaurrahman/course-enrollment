from pydantic import BaseModel, EmailStr, Field, field_validator

class UserBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    role: str
    
    @field_validator('role')
    @classmethod
    def role_must_be_valid(cls, v: str) -> str:
        if v not in ['student', 'admin']:
            raise ValueError('role must be either student or admin')
        return v

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
