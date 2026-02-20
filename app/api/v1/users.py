from fastapi import APIRouter, status, HTTPException
from app.schemas.user import UserCreate
from app.services.user import UserService

users_router = APIRouter()

@users_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate):
    return UserService.create_user(user_in)

@users_router.get("/")
def get_all_users():
    return UserService.list_users()

@users_router.get("/{user_id}")
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
