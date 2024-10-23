from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..models.user import Staff, Student
from ..database.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class StudentManager:
    @staticmethod
    async def add_students(student_data, db: Session = Depends(get_db)):
        student_record = db.query(Student).where(Student.email == student_data.email).first()
        if student_record:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student already exists.")
        student_record.password = pwd_context.hash(student_data.password)
        new_student = Student(**student_record.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student

    @staticmethod
    async def get_user_with_id(student_id, db: Session = Depends(get_db)):
        record = db.query(Student).where(Student.id_ == student_id).first()
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {student_id} not found")
        return record

    @staticmethod
    async def get_user_with_email(student_email, db: Session = Depends(get_db)):
        record = db.query(Student).where(Student.email == student_email).first()
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {student_email} not found")
        return record

    @staticmethod
    async def update_student_record(student_id: int, record_to_update: dict, db: Session = Depends(get_db)):
        record = db.query(Student).filter(Student.id_ == student_id).first()
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {student_id} not found")
        to_update = db.query(Student).filter(Student.id_ == student_id).update(record_to_update)
        db.commit()
        db.refresh(to_update)
        return to_update

    @staticmethod
    async def delete_student(student_id: int, db: Session = Depends(get_db)):
        record = db.query(Student).filter(Student.id_ == student_id).first()
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {student_id} not found")
        db.delete(record)
