from typing import List, Optional
from fastapi import HTTPException, status
from app.schemas.enrollment import EnrollmentCreate, Enrollment
from app.core.db import enrollments_db, users_db, courses_db

class EnrollmentService:
    @staticmethod
    def enroll_student(enrollment_in: EnrollmentCreate) -> Enrollment:
        user = users_db.get(enrollment_in.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if user.role != "student":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can enroll in courses")
            
        course = courses_db.get(enrollment_in.course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
            
        # Check if already enrolled
        for enrollment in enrollments_db.values():
            if enrollment.user_id == enrollment_in.user_id and enrollment.course_id == enrollment_in.course_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already enrolled in this course")
                
        enroll_id = len(enrollments_db) + 1
        new_enrollment = Enrollment(id=enroll_id, **enrollment_in.model_dump())
        enrollments_db[enroll_id] = new_enrollment
        return new_enrollment

    @staticmethod
    def deregister_student(enrollment_id: int, requesting_user_id: int, force: bool = False) -> None:
        enrollment = enrollments_db.get(enrollment_id)
        if not enrollment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
            
        if not force:
            # Check ownership
            if enrollment.user_id != requesting_user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to deregister this enrollment")
                
        del enrollments_db[enrollment_id]

    @staticmethod
    def get_student_enrollments(user_id: int) -> List[Enrollment]:
        return [e for e in enrollments_db.values() if e.user_id == user_id]

    @staticmethod
    def get_all_enrollments() -> List[Enrollment]:
        return list(enrollments_db.values())

    @staticmethod
    def get_course_enrollments(course_id: int) -> List[Enrollment]:
        return [e for e in enrollments_db.values() if e.course_id == course_id]
