from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..models.user import Staff, Student
from ..models.enums import Roles
from ..database.database import get_db
from ..schemas.requests import StaffIn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class StaffManager:
    @staticmethod
    async def get_staffs(db: Session = Depends(get_db)):
        record = db.query(Student).all()
        return record

    @staticmethod
    async def add_staff(staff_data: StaffIn, db: Session = Depends(get_db)):
        check_existing_record = db.query(Staff).where(Staff.email == staff_data.email).first()
        if check_existing_record:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Staff with the email {staff_data.email} exits.")
        staff_data.password = pwd_context.hash(staff_data.password)
        new_staff = Staff(**staff_data.dict())
        db.add(new_staff)
        db.commit()
        db.refresh(staff_data)
        return staff_data

    @staticmethod
    async def get_staff_by_id(staff_id: int, db: Session = Depends(get_db)):
        staff = db.query(Staff).filter(Staff.id_ == staff_id).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        return staff

    @staticmethod
    async def get_staff_by_email(email: str, db: Session = Depends(get_db)):
        staff = db.query(Staff).filter(Staff.id_ == email).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        return staff

    @staticmethod
    async def update_staff_details(staff_id: int, staff_data, db: Session = Depends(get_db)):
        staff = db.query(Staff).filter(Staff.id_ == staff_id).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        updated = db.query(Staff).filter(Staff.id_ == staff_id).update(staff_data)
        db.commit()
        db.refresh(updated)
        return updated

    @staticmethod
    async def upgrade_downgrade_staff(staff_id: int, role: Roles, db: Session = Depends(get_db)):
        staff = db.query(Staff).filter(Staff.id_ == staff_id).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        staff.role = role
        db.commit()
        db.refresh(staff)
        return staff

    @staticmethod
    async def delete_staff(staff_id: int, db: Session = Depends(get_db)):
        staff = db.query(Staff).filter(Staff.id_ == staff_id).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        db.delete(staff)
        db.commit()

