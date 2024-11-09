from bson import ObjectId

from typing import Optional

from pydantic import BaseModel, EmailStr

from .base import Base


class StudentOut(Base):
    _id: int
    role: str
    admission_number: str


class StaffOut(Base):
    _id: int
    role: str
    course: str

#
# class UserOut(BaseModel):
#     id: ObjectId
#     email: EmailStr
#     phoneNumber: str
#     role: str
#     firstName: str
#     lastName: str
#     dateOfBirth: str
#     placeOfBirth: str
#     # education: Optional[dict] = None
#     parentFirstName: Optional[str] = None
#     parentLastName: Optional[str] = None
#     parentEmail: Optional[EmailStr] = None
#     parentAddress: Optional[str] = None
#     parentPhone: Optional[str] = None
#     address: Optional[str] = None
#     about: Optional[str] = None
#     expertise: Optional[str] = None
#
#     class Config:
#         arbitrary_types_allowed = True  # Allow arbitrary types
#         json_encoders = {ObjectId: str}
#
