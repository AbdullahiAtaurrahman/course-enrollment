from fastapi import APIRouter, status, HTTPException
from core.db import users
from schemas.user import UserCreate
from app.services.user import UserService

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate):
    user = UserService.create_user(user_in)
    return {"message": "successful", "data": user}

@router.get('/', status_code=status.HTTP_200_OK)
def get_users():
    users_list = UserService.get_users()
    return {"message": "successful", "data": users_list}

@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_user(id: int):
    user = UserService.get_user(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return {"message": "successful", "data": user}
