from fastapi import APIRouter, status, HTTPException, Header, Depends
from app.schemas.course import CourseCreate, CourseBase
from app.services.course import CourseService

courses_router = APIRouter()

def verify_admin(x_user_role: str = Header(...)):
    if x_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return x_user_role

@courses_router.get("/")
def get_all_courses():
    return CourseService.list_courses()

@courses_router.get("/{course_id}")
def get_course(course_id: int):
    course = CourseService.get_course(course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@courses_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_admin)])
def create_course(course_in: CourseCreate):
    return CourseService.create_course(course_in)

@courses_router.put("/{course_id}", dependencies=[Depends(verify_admin)])
def update_course(course_id: int, course_in: CourseBase):
    return CourseService.update_course(course_id, course_in)

@courses_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_admin)])
def delete_course(course_id: int):
    CourseService.delete_course(course_id)
