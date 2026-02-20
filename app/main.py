from fastapi import FastAPI
from app.api.v1.users import users_router
from app.api.v1.courses import courses_router
from app.api.v1.enrollments import enrollments_router

app = FastAPI(title="Course Enrollment API")

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(courses_router, prefix="/courses", tags=["Courses"])
app.include_router(enrollments_router, prefix="/enrollments", tags=["Enrollments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Course Enrollment API"}
