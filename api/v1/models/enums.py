from enum import Enum


class Roles(Enum):
    student = "student"
    lecturer = "lecturer"
    admin = "admin"
    supper_admin = "supper"
    course_rep = "rep"


class Level(Enum):
    level1 = "100"
    level2 = "200"
    level3 = "300"
    level4 = "400"


class CourseStatus(Enum):
    withdrawn = "withdrawn"
    normal = "normal"
    suspended = "suspended"


class StudentStatus(Enum):
    active = "active"
    inactive = "inactive"


class PositionHeld(Enum):
    member = "member"
    course_rep = "course rep"
    supervisor = "supervisor"
    counsellor = "counsellor"


class EventStatus(Enum):
    pending = "pending"
    suspended = "suspended"
    approved = "approved"
    ongoing = "ongoing"

