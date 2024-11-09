from datetime import datetime
from datetime import date
from typing import Optional, ClassVar

from bson import ObjectId
from odmantic import Model, Reference, Field, EmbeddedModel
from pydantic import EmailStr, HttpUrl, ConfigDict, validator, ValidationError

from .enums import (
    StudentStatus,
    Roles,
    PositionHeld,
    Level,
    EventStatus)


class Education(Model):
    university: str
    degree: str
    startDate: str
    endDate: str
    city: str

    model_config: ClassVar[ConfigDict] = ConfigDict({"collection": "education", "arbitrary_types_allowed": True})


class User(Model):
    email: EmailStr = Field(unique=True)
    password: str
    phoneNumber: str
    idNumber: str
    # role: str = Field(default=Roles.student.name)
    isAdmin: bool = Field(default=False)
    isStudent: bool = Field(default=True)
    firstName: str
    lastName: str
    photo: str
    # photo: Optional[HttpUrl] = None
    # dateOfBirth: date
    dateOfBirth: str
    placeOfBirth: str

    education: Education = Reference()

    status: str = Field(default=StudentStatus.active.name)
    # createdAt: datetime = Field(default_factory=datetime.utcnow)
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    # Guardian information
    parentFirstName: Optional[str] = None
    parentLastName: Optional[str] = None
    parentEmail: Optional[EmailStr] = None
    parentAddress: Optional[str] = None
    parentPhone: Optional[str] = None

    address: str
    about: str
    expertise: str

    # @validator("dateOfBirth")
    # def validate_date_of_birth(cls, dob):
    #     if dob.year < 1960:
    #         raise ValueError("Year of birth cannot be earlier than 1960")
    #     return dob

    model_config: ClassVar[ConfigDict] = ConfigDict({"collection": "users", "arbitrary_types_allowed": True})


class Position(Model):
    user_id: ObjectId
    class_: Field(default=Level.level1.name)
    role: Field(default=PositionHeld.member.name)
    course: str

    model_config: ClassVar[ConfigDict] = ConfigDict({"collection": "positions", "arbitrary_types_allowed": True})


class Event(Model):
    date: str
    title: str
    course: Optional[str] = None
    class_: Optional[str] = None
    startTime: int
    endTime: int
    status: Field(default=EventStatus.pending.name)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    creatorId: User = Reference()

    model_config: ClassVar[ConfigDict] = ConfigDict({"collection": "events", "arbitrary_types_allowed": True})

