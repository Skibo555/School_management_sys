from fastapi import APIRouter, Request, status

from ..models.user import Student, Staff
from ..database.database import get_db
from ..schemas.requests import StaffIn, StudentIn, StudentUpdateFormIn
from ..controllers.staff import StudentManager


# This is a router that will be used to bind this route to the app in the app.py file
router = APIRouter(prefix='/api/admin', tags=["Admin Panel"])


@router.get("/")
async def admin():
    """
    This greets the admin in the admin panel after the system has authenticated the admin.
    :return: message
    """
    message = {
        "Message": "You are welcome to the admin panel"
    }
    return message


@router.get("/student")
async def student(user_data: StaffIn):
    """
    This gets the list of all the users/students registered on the database.
    :return: list of students
    """

    pass


@router.get("/users/{id_}")
async def get_students_by_id(id_: Request):
    """
    This route will get student based on the id provided.
    :param id_: student's ID, email address
    :return: student object
    """
    pass


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: StudentIn):
    """
    this will register a user
    :param student_data: student's data will be sent, pydantic model.
    :return: created user.
    """
    return await StudentManager.add_students(student_data=student_data)


@router.put("/user/{id}")
async def update_user(id_: int, user_data: StudentUpdateFormIn):
    user = user_data
    return await StudentManager.update_student_record(student_id=id_, record_to_update=user.dict())
