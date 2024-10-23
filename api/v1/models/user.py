from typing import Optional

from sqlalchemy import String, Enum, TIMESTAMP, BOOLEAN, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .enums import Roles, Level


class Base(DeclarativeBase):
    id_: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(type_=Enum, default=Roles.student.student)
    birthday: Mapped[str] = mapped_column(Date)
    department: Mapped[str] = mapped_column(String(100))
    joined_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    is_deleted: Mapped[str] = mapped_column(BOOLEAN, default=False)


class Student(Base):
    __tablename__ = "students"
    level: Mapped[str] = mapped_column(Enum, default=Level.jss1.jss1)
    admission_number: Mapped[str] = mapped_column()
    # Relationship to the StudentCourses association table.
    courses: Mapped[str] = relationship("StudentCourse", back_populates='student')

    def __repr__(self) -> str:
        return f"User(id={self.id_!r}, name={self.first_name!r}, fullname={self.last_name!r})"


class Staff(Base):
    __tablename__ = "staffs"
    course: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"User(id={self.id_!r}, name={self.first_name!r}, fullname={self.last_name!r})"

