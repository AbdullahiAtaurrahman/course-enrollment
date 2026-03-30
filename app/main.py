from fastapi import FastAPI
from app.api.v1.user import router as users_router
from app.api.v1.enrollment import router as enrollments_router
from app.api.v1.course import router as courses_router


app = FastAPI()


app.include_router(users_router, prefix='/users', tags=['users'])
app.include_router(enrollments_router, prefix='/enrollments', tags=['enrollments'])
app.include_router(courses_router, prefix='/courses', tags=['courses'])
