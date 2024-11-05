from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..models.user import User
from ..models.enums import Roles
from ..database.database import get_db
from ..schemas.requests import StaffUpdateFormIn
# from ..schemas.requests import StaffIn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class StaffManager:
    @staticmethod
    async def get_staffs():
        db = get_db()
        record = await db.find(User)
        return record

    @staticmethod
    async def add_staff(staff_data: User):
        db = get_db()
        check_existing_record = await db.find_one(User.email == staff_data.email)
        if check_existing_record:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Staff with the email {staff_data.email} exits.")
        staff_data.password = pwd_context.hash(staff_data.password)
        new_staff = User(**staff_data.dict())
        db.save(new_staff)

        return staff_data

    @staticmethod
    async def get_staff_by_id(staff_id: int):
        db = get_db()
        staff = await db.find_one(User, User.ObjectId == staff_id)
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        return staff

    @staticmethod
    async def get_staff_by_email(email: str):
        db = get_db()
        staff = await db.find_one(User, User.email == email)
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        return staff

    @staticmethod
    async def update_staff_details(staff_id: int, staff_data):
        db = get_db()
        staff = await db.find_one(User, User.ObjectId == staff_id)
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        obj_updated = StaffUpdateFormIn(**staff_data)
        staff.model_update(obj_updated)
        return await db.save(staff)

    @staticmethod
    async def upgrade_downgrade_staff(staff_id: int, role: Roles):
        db = get_db()
        staff = await db.query(User).filter(User.id_ == staff_id).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        staff.role = role
        db.commit()
        db.refresh(staff)
        return staff

    @staticmethod
    async def delete_staff(staff_id: int):
        db = get_db()
        staff = await db.query(User).filter(User.id_ == staff_id).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
        db.delete(staff)
        db.commit()

