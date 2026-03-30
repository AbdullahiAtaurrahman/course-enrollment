from fastapi import APIRouter, Depends, status
from app.services.enrollment import EnrollmentService
from app.api.dps import is_user_admin, is_user_student

router = APIRouter()

# Student Operations

@router.post("/enroll", status_code=status.HTTP_201_CREATED, dependencies=[Depends(is_user_student)])
def enroll_student(user_id: int, course_id: int):
    return EnrollmentService.enroll_student(user_id, course_id)

@router.delete("/deregister", status_code=status.HTTP_200_OK, dependencies=[Depends(is_user_student)])
def deregister_student(user_id: int, course_id: int):
    return EnrollmentService.deregister_student(user_id, course_id)

@router.get("/student/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(is_user_student)])
def get_student_enrollments(user_id: int):
    return EnrollmentService.get_student_enrollments(user_id)

# Admin Operations

@router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(is_user_admin)])
def get_all_enrollments(user_id: int): 
    return EnrollmentService.get_all_enrollments()

@router.get("/course/{course_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(is_user_admin)])
def get_course_enrollments(user_id: int, course_id: int):
    return EnrollmentService.get_course_enrollments(course_id)

@router.delete("/force-deregister", status_code=status.HTTP_200_OK, dependencies=[Depends(is_user_admin)])
def force_deregister(user_id: int, student_id: int, course_id: int):
    return EnrollmentService.force_deregister(student_id, course_id)
