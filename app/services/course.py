from schemas.course import CourseCreate, Course, CourseUpdate
from core.db import courses
from fastapi import HTTPException, status

class CourseService:
    @staticmethod
    def create_course(course_in: CourseCreate):
        if not course_in.title.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="title must not be empty")
        if not course_in.code.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="code must not be empty")
        
        for c in courses.values():
            if c.code == course_in.code:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="course code must be unique")

        course_id = len(courses) + 1 
        course = Course(
            id = course_id,
            **course_in.model_dump()
        )
        courses[course_id] = course
        return {"message": "added successfully", "data": course}
    
    @staticmethod
    def get_courses():
        return list(courses.values())

    @staticmethod
    def get_course(id: int):
        course = courses.get(id)
        if not course:
            return None
        return {'message': 'successful', 'data': course}

    @staticmethod
    def delete_course(id: int):
        if id not in courses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='course not found')
        del courses[id]

    @staticmethod
    def update_course(id: int, course_in: CourseUpdate):
        if id not in courses:
            return None
            
        if course_in.title is not None and not course_in.title.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="title must not be empty")
            
        if course_in.code is not None:
            if not course_in.code.strip():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="code must not be empty")
            # Check uniqueness against other courses
            for c_id, c in courses.items():
                if c_id != id and c.code == course_in.code:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="course code must be unique")

        course = courses[id]
        update_data = course_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(course, field, value)
        return course    