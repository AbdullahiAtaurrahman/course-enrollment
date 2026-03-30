from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    title: str
    code: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None