from typing import List, Optional
from fastapi import HTTPException, status
from app.schemas.course import CourseCreate, CourseBase, Course
from app.core.db import courses_db

class CourseService:
    @staticmethod
    def create_course(course_in: CourseCreate) -> Course:
        # Check if code is unique
        for course in courses_db.values():
            if course.code == course_in.code:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course code must be unique")
        
        course_id = len(courses_db) + 1
        new_course = Course(id=course_id, **course_in.model_dump())
        courses_db[course_id] = new_course
        return new_course

    @staticmethod
    def list_courses() -> List[Course]:
        return list(courses_db.values())

    @staticmethod
    def get_course(course_id: int) -> Optional[Course]:
        return courses_db.get(course_id)

    @staticmethod
    def update_course(course_id: int, course_in: CourseBase) -> Course:
        existing_course = courses_db.get(course_id)
        if not existing_course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
        # Check code uniqueness if changing code
        if course_in.code != existing_course.code:
            for course in courses_db.values():
                if course.code == course_in.code:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course code must be unique")
        
        updated_course = Course(id=course_id, **course_in.model_dump())
        courses_db[course_id] = updated_course
        return updated_course

    @staticmethod
    def delete_course(course_id: int) -> None:
        if course_id not in courses_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        del courses_db[course_id]
