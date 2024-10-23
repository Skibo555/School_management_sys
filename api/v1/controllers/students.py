from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..models.user import Staff
from ..database.database import get_db
from ..schemas.response import StudentOut
from ..schemas.requests import StudentUpdateFormIn
from ..models.user import Student


class StudentAffairs:
    @staticmethod
    async def get_all_courses(student_id: int, db: Session = Depends(get_db)):
        record = db.query(Student).where(Student.id_ == student_id).first()
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        courses = db.query(Student.courses).all()
        return courses

    @staticmethod
    async def update_details(user_id: int, info_to_update: StudentUpdateFormIn, db: Session = Depends(get_db)):
        student_id = db.query(Student).filter(Student.id_ == user_id).first()
        if not student_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        data = db.query(Student).filter(Student.id_ == user_id).update(info_to_update.dict())
        db.commit()
        db.refresh(data)
        return data
