from typing import Optional

from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .user import Base


class Course(Base):
    __tablename__ = "courses"
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_title: Mapped[str] = mapped_column(String(100), nullable=False)
    course_code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    course_description: Mapped[str] = mapped_column(Text)
    student: Mapped[str] = relationship('StudentCourse', back_populates='course')


# association table for many-to-many relationship
class StudentCourse(Base):
    __tablename__ = "student_courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id_"))
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.course_id"))

    student: Mapped[str] = relationship('Student', back_populates='course')
    course: Mapped[str] = relationship('Course', back_populates='student')