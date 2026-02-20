from fastapi import APIRouter, status, HTTPException, Header, Depends
from app.schemas.enrollment import EnrollmentCreate
from app.services.enrollment import EnrollmentService

enrollments_router = APIRouter()

def verify_student(x_user_role: str = Header(...)):
    if x_user_role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student role required")
    return x_user_role

def verify_admin(x_user_role: str = Header(...)):
    if x_user_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return x_user_role


# Student endpoints
@enrollments_router.post("/", status_code=status.HTTP_201_CREATED)
def enroll_student(enrollment_in: EnrollmentCreate, role: str = Depends(verify_student)):
    return EnrollmentService.enroll_student(enrollment_in)

@enrollments_router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def deregister_student(enrollment_id: int, x_user_id: int = Header(...), role: str = Depends(verify_student)):
    EnrollmentService.deregister_student(enrollment_id, requesting_user_id=x_user_id)

@enrollments_router.get("/students/{user_id}")
def get_my_enrollments(user_id: int, role: str = Depends(verify_student)):
    return EnrollmentService.get_student_enrollments(user_id)


# Admin endpoints
@enrollments_router.get("/")
def get_all_enrollments(role: str = Depends(verify_admin)):
    return EnrollmentService.get_all_enrollments()

@enrollments_router.get("/courses/{course_id}")
def get_course_enrollments(course_id: int, role: str = Depends(verify_admin)):
    return EnrollmentService.get_course_enrollments(course_id)

@enrollments_router.delete("/{enrollment_id}/force", status_code=status.HTTP_204_NO_CONTENT)
def force_deregister_student(enrollment_id: int, role: str = Depends(verify_admin)):
    # admin doesn't need to own the enrollment (we pass 0 or ignored user_id, force=True)
    EnrollmentService.deregister_student(enrollment_id, requesting_user_id=0, force=True)
