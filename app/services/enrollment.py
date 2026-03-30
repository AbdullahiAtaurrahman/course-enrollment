from fastapi import HTTPException, status
from app.core.db import users, courses, enrollments
from app.schemas.enrollment import Enrollment

class EnrollmentService:
    @staticmethod
    def enroll_student(user_id: int, course_id: int):
        if user_id not in users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        if course_id not in courses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
        enrollment_id = f"{user_id}_{course_id}"
        if enrollment_id in enrollments:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already enrolled in this course")
        
        enrollment = Enrollment(
            id=enrollment_id,
            user_id=user_id,
            course_id=course_id
        )
        enrollments[enrollment_id] = enrollment
        return enrollment
        
    @staticmethod
    def deregister_student(user_id: int, course_id: int):
        enrollment_id = f"{user_id}_{course_id}"
        if enrollment_id not in enrollments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
        
        del enrollments[enrollment_id]
        return {"message": "Successfully deregistered from the course"}

    @staticmethod
    def get_student_enrollments(user_id: int):
        return [e for e in enrollments.values() if e.user_id == user_id]

    @staticmethod
    def get_course_enrollments(course_id: int):
        return [e for e in enrollments.values() if e.course_id == course_id]

    @staticmethod
    def get_all_enrollments():
        return list(enrollments.values())

    @staticmethod
    def force_deregister(user_id: int, course_id: int):
        return EnrollmentService.deregister_student(user_id, course_id)
