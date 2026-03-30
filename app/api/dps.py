from fastapi import HTTPException, status
from schemas.user import UserRole, User
from services.user import UserService

def is_user_admin(user_id:int):
    user: User = UserService.get_user(user_id)

    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='access denied')
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user not found')

def is_user_student(user_id:int):
    user: User = UserService.get_user(user_id)

    if user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='access denied')
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user not found')