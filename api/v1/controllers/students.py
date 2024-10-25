from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.courses import Course
from ..models.user import Student
from ..schemas.requests import StudentUpdateFormIn


class StudentAffairs:
    @staticmethod
    async def get_all_courses(student_id: int, db: Session = Depends(get_db)):
        record = db.query(Student).where(Student.id_ == student_id).first()
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        courses = db.query(Course.course_title).all()
        return courses

    @staticmethod
    async def update_details(user_id: int, info_to_update: StudentUpdateFormIn, db: Session = Depends(get_db)):
        student_id = db.query(Student).filter(Student.id_ == user_id).first()
        if not student_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        course = db.query(Course).filter(Course.student == user_id).update(info_to_update.dict())
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    async def delete_course(course_id: int, db: Session = Depends(get_db)):
        record = db.query(Course).filter(Course.course_id == course_id).first()
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {course_id} not found")
        db.delete(record)

