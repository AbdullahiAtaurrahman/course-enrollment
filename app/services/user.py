from typing import List, Optional
from fastapi import HTTPException
from app.schemas.user import UserCreate, User
from app.core.db import users_db

class UserService:
    @staticmethod
    def create_user(user_in: UserCreate) -> User:
        user_id = len(users_db) + 1
        new_user = User(id=user_id, **user_in.model_dump())
        users_db[user_id] = new_user
        return new_user

    @staticmethod
    def list_users() -> List[User]:
        return list(users_db.values())

    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        return users_db.get(user_id)
