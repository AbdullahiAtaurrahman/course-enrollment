from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.course import CourseCreate, CourseUpdate
from app.services.course import CourseService
from app.api.dps import is_user_admin

router = APIRouter()

# basic operations open to everyone

@router.get('/', status_code=status.HTTP_200_OK)
def get_courses():
    courses_in = CourseService.get_courses()
    return {'message': 'successful', 'data': courses_in}

@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_course(id: int):
    course_resp = CourseService.get_course(id)
    if not course_resp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='course not found')
    return course_resp

# operations open to only admin

@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(is_user_admin)])
def create_course(course_in: CourseCreate):
    new_course = CourseService.create_course(course_in)
    return new_course

@router.patch('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(is_user_admin)])
def update_course(id: int, course_in: CourseUpdate):
    course = CourseService.update_course(id, course_in)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='course not found')
    return {'message': 'successful', 'data': course}

@router.delete('/{course_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(is_user_admin)])
def delete_course(course_id: int):
    CourseService.delete_course(course_id)
    return {'message': 'course successfully deleted'}
