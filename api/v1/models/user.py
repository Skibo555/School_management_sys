from datetime import datetime
from typing import Optional, ClassVar
from odmantic import Model, Reference, Field
from pydantic import EmailStr, HttpUrl, ConfigDict

from .enums import StudentStatus, Roles


class Education(Model):
    university: str
    degree: str
    startDate: str
    endDate: str
    city: str

    model_config: ClassVar[ConfigDict] = ConfigDict(collection="education")


class User(Model):
    email: EmailStr = Field(unique=True)
    password: str
    phoneNumber: str
    # idNumber: str
    role: str = Field(default=Roles.student.name)

    firstName: str
    lastName: str
    photo: Optional[HttpUrl] = None
    dateOfBirth: str
    placeOfBirth: str

    education: Education = Reference()

    status: str = Field(default=StudentStatus.active.name)
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    # Guardian information
    parentFirstName: Optional[str] = None
    parentLastName: Optional[str] = None
    parentEmail: Optional[EmailStr] = None
    parentAddress: Optional[str] = None
    parentPhone: Optional[str] = None

    address: Optional[str] = None
    about: Optional[str] = None
    expertise: Optional[str] = None

    model_config: ClassVar[ConfigDict] = ConfigDict(collection="users")


class Position(Model):
    user: User = Reference()
    class_: str
    role: str
    course: str


# class Event(Model):
#     date: str
#     title: str
#     course: Optional[str] = None
#     class_: Optional[str] = None
#     startTime: int
#     endTime: int
#     status: Field(default=Status.normal.name)

# from sqlalchemy import String, Enum, TIMESTAMP, BOOLEAN, Date, Integer, ForeignKey, Text
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from sqlalchemy.sql import func
#
# from .enums import Roles, Level
#
#
# class Base(DeclarativeBase):
#     pass
#
#
# class Student(Base):
#     __tablename__ = "students"
#     id_: Mapped[int] = mapped_column(Integer, primary_key=True)
#     email: Mapped[str] = mapped_column(unique=True, nullable=False)
#     first_name: Mapped[str] = mapped_column(String(30), nullable=False)
#     last_name: Mapped[str] = mapped_column(String(30), nullable=False)
#     middle_name: Mapped[Optional[str]] = mapped_column(String(30))
#     password: Mapped[str] = mapped_column(String(50), nullable=False)
#     role: Mapped[str] = mapped_column(type_=Enum, default=Roles.student.student)
#     birthday: Mapped[str] = mapped_column(Date)
#     department: Mapped[str] = mapped_column(String(100))
#     joined_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
#     updated_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
#     is_deleted: Mapped[str] = mapped_column(BOOLEAN, default=False)
#     level: Mapped[str] = mapped_column(Enum, default=Level.jss1.jss1)
#     admission_number: Mapped[str] = mapped_column()
#
#     # Relationship to the StudentCourses association table.
#     course: Mapped[str] = relationship("StudentCourse", back_populates='student')
#
#     def __repr__(self) -> str:
#         return f"User(id={self.id_!r}, name={self.first_name!r}, fullname={self.last_name!r})"
#
#
# class Staff(Base):
#     __tablename__ = "staffs"
#     id_: Mapped[int] = mapped_column(Integer, primary_key=True)
#     email: Mapped[str] = mapped_column(unique=True, nullable=False)
#     first_name: Mapped[str] = mapped_column(String(30), nullable=False)
#     last_name: Mapped[str] = mapped_column(String(30), nullable=False)
#     middle_name: Mapped[Optional[str]] = mapped_column(String(30))
#     password: Mapped[str] = mapped_column(String(50), nullable=False)
#     role: Mapped[str] = mapped_column(type_=Enum, default=Roles.student.student)
#     birthday: Mapped[str] = mapped_column(Date)
#     department: Mapped[str] = mapped_column(String(100))
#     joined_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
#     updated_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
#     is_deleted: Mapped[str] = mapped_column(BOOLEAN, default=False)
#
#     # relationship to the courses table
#     course_title: Mapped[str] = relationship("Course", back_populates="course_title")
#
#     def __repr__(self) -> str:
#         return f"User(id={self.id_!r}, name={self.first_name!r}, fullname={self.last_name!r})"
