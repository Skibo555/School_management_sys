from typing import Optional

from sqlalchemy import String, Enum, TIMESTAMP, BOOLEAN, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .user import Base


class Course(Base):
    __tablename__ = "courses"
    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_title: Mapped[str] = mapped_column(String(100), nullable=False)
    course_code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    course_description: Mapped[str] = mapped_column(Text)
    students: Mapped[str] = relationship('StudentCourse', back_populates='course')


# class StudentCourse(DeclarativeBase):
#     __tablename__ = "student_courses"
#     student_id: Mapped[str] = ForeignKey()
#
#     pass
