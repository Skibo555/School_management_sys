import datetime
from odmantic import Field, Model, Reference

from .user import User
from .enums import Status


class Course(Model):
    course_title: str
    course_code: str
    course_description: str
    course_status = Field(default=Status.normal.name)
    course_owner_id: User = Reference()
    createdAt: datetime = Field(default_factory=datetime.datetime.utcnow)

    model_config = {
        "collection": "courses"
    }


class Enrollment(Model):
    student_id: User = Reference()
    course_id: Course = Reference()


# from sqlalchemy import String, Integer, ForeignKey, Text
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
#
# from .user import Base
#
#
# class Course(Base):
#     __tablename__ = "courses"
#     course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     course_title: Mapped[str] = mapped_column(String(100), nullable=False)
#     course_code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
#     course_description: Mapped[str] = mapped_column(Text)
#     student: Mapped[str] = relationship('StudentCourse', back_populates='course')
#
#
# # association table for many-to-many relationship
# class StudentCourse(Base):
#     __tablename__ = "student_courses"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id_"))
#     course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.course_id"))
#
#     student: Mapped[str] = relationship('Student', back_populates='course')
#     course: Mapped[str] = relationship('Course', back_populates='student')
