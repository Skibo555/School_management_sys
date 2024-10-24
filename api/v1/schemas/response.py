from .base import Base


class StudentOut(Base):
    _id: int
    role: str
    admission_number: str


class StaffOut(Base):
    _id: int
    role: str
    course: str
