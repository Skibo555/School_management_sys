import datetime

from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

from pydantic.v1 import validator

from ..models.enums import StudentStatus
from ..models.user import Education


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
    idNumber: str
    isAdmin: Optional[bool] = False
    isStudent: Optional[bool] = True
    firstName: str
    lastName: str
    photo: str
    # photo: Optional[HttpUrl] = None
    # dateOfBirth: datetime.date
    dateOfBirth: str
    placeOfBirth: str

    education: Education

    status: StudentStatus = Optional[StudentStatus.active.name]

    # Guardian information
    parentFirstName: Optional[str] = None
    parentLastName: Optional[str] = None
    parentEmail: Optional[EmailStr] = None
    parentAddress: Optional[str] = None
    parentPhone: Optional[str] = None

    address: str
    about: str
    expertise: str

    @validator("dateOfBirth")
    def validate_date_of_birth(cls, dob):
        if dob.year < 1960:
            raise ValueError("Year of birth cannot be earlier than 1960")
        return dob

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types


class StudentUpdateFormIn(BaseModel):
    level: str


class StaffUpdateFormIn(BaseModel):
    firstName: str
    lastName: str


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


class PasswordResetEmailIn(BaseModel):
    email: EmailStr


class PasswordResetIn(BaseModel):
    new_password: str
    confirm_password: str


class UpdateUserPosition(BaseModel):
    class_: str
    role: str
    course: str
