import re
from fastapi import HTTPException, status
from core.db import users
from schemas.user import UserCreate, UserBase, User

class UserService:
    @staticmethod
    def create_user(user_in: UserCreate):
        if not user_in.name.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must not be empty")
        
        user_id = len(users) + 1
        user = User(
            id=str(user_id),
            **user_in.model_dump()
        )
        users[user_id] = user
        return user

    @staticmethod
    def get_users() -> list:
        return list(users.values())
    
    @staticmethod
    def get_user(id: int):
        user = users.get(id)
        return user