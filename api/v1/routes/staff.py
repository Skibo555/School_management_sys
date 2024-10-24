from fastapi import APIRouter, Request, status
from ..schemas.requests import StaffIn, StudentIn, StudentUpdateFormIn
from ..controllers.staff import StudentManager


# This is a router that will be used to bind this route to the app in the app.py file
router = APIRouter(prefix='/api', tags=["Staffs Panel"])


@router.get("/")
async def home():
    """
    This greets the admin in the admin panel after the system has authenticated the admin.
    :return: message
    """
    message = {
        "Message": "You are welcome to the admin panel"
    }
    return message


@router.get("/students")
async def get_students():
    """
    This gets the list of all the users/students registered on the database.
    :return: list of students
    """
    return await StudentManager.get_all_student()


@router.get("/students/{id_}")
async def get_students_by_id(id_: Request):
    """
    This route will get student based on the id provided.
    :param id_: student's ID, email address
    :return: student object
    """
    return await StudentManager.get_student_with_id(id_)


@router.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student_data: StudentIn):
    """
    this will register a user
    :param student_data: student's data will be sent, pydantic model.
    :return: created user.
    """
    return await StudentManager.add_students(student_data=student_data)


@router.put("/students/{id}")
async def update_user(id_: int, user_data: StudentUpdateFormIn):
    """
    This updates student data in the database
    :param id_: id of the student that wants to update their details
    :param user_data: data of the student
    :return: updated details of the student
    """
    user = user_data
    return await StudentManager.update_student_record(student_id=id_, record_to_update=user.dict())


@router.put("/students/{id}")
async def delete_student(student_id):
    """
    this deletes a student with the supplied id from the database permanently.
    :param student_id: student to delete id
    :return: None
    """
    return await StudentManager.delete_student(student_id)
