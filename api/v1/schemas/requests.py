from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

from ..models.user import User, Education
from ..models.courses import Course


# from .base import Base
#
#
# class StudentIn(Base):
#     level: str
#     password: str
#
#     # @field_validator("password")
#     # def check_password(self, value):
#     #     # Check if password meets the length requirement
#     #     if len(value) < 8:
#     #         raise ValueError("Password must have at least 8 characters")
#     #
#     #     # Check for at least one uppercase, one lowercase, one digit, and one special character
#     #     if not any(c.isupper() for c in value):
#     #         raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
#     #     if not any(c.islower() for c in value):
#     #         raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
#     #     if not any(c.isdigit() for c in value):
#     #         raise HTTPException(status_code=400, detail="Password must contain at least one digit.")
#     #     if not any(c in punctuation for c in value):
#     #         raise HTTPException(status_code=400, detail="Password must contain at least one special character.")
#     #
#     #     return value
#
#
# class StaffIn(Base):
#     course: str
#     password: str
#
#     # @field_validator("password")
#     # def check_password(self, value):
#     #     # Check if password meets the length requirement
#     #     if len(value) < 8:
#     #         raise ValueError("Password must have at least 8 characters")
#     #
#     #     # Check for at least one uppercase, one lowercase, one digit, and one special character
#     #     if not any(c.isupper() for c in value):
#     #         raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
#     #     if not any(c.islower() for c in value):
#     #         raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
#     #     if not any(c.isdigit() for c in value):
#     #         raise HTTPException(status_code=400, detail="Password must contain at least one digit.")
#     #     if not any(c in punctuation for c in value):
#     #         raise HTTPException(status_code=400, detail="Password must contain at least one special character.")
#     #
#     #     return value
#
#


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    phoneNumber: str
    role: str
    firstName: str
    lastName: str
    dateOfBirth: str
    placeOfBirth: str
    education: Optional[dict] = None
    parentFirstName: Optional[str] = None
    parentLastName: Optional[str] = None
    parentEmail: Optional[EmailStr] = None
    parentAddress: Optional[str] = None
    parentPhone: Optional[str] = None
    address: Optional[str] = None
    about: Optional[str] = None
    expertise: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types


class StudentUpdateFormIn(BaseModel):
    level: str


class StaffUpdateFormIn(BaseModel):
    firstName: str
    lastName: str


class UserObjTokenIn(BaseModel):
    ObjectId: str
    role: str


class CourseUpdateForm(BaseModel):
    course_title: str
    course_code: str
    course_description: str


class UserUpdateForm(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr


class CreateCourseIn(BaseModel):
    course_title: str
    course_code: str
    course_description: str
    course_owner_id: int


class LoginForm(BaseModel):
    password: str
    email: EmailStr

