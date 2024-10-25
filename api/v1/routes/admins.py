from fastapi import APIRouter, Request, status
from ..schemas.requests import StaffIn, StudentIn, StudentUpdateFormIn
from ..controllers.staff import StudentManager
from ..controllers.admin import StaffManager


# This is a router that will be used to bind this route to the app in the app.py file
router = APIRouter(prefix='/api', tags=["Admin Panel"])


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


@router.get("/staff")
async def get_staffs():
    """
    This gets the list of all the staffs registered on the database.
    :return: list of staffs
    """
    return await StaffManager.get_staffs()


@router.get("/staffs/{id_}")
async def get_staff_by_id(staff_id: Request):
    """
    This route will get staff based on the id provided.
    :param staff_id: staff's ID, email address
    :return: staff object
    """
    return await StaffManager.get_staff_by_id(**staff_id)


@router.get("/staffs/")
async def get_staff_by_email(email: Request):
    """
    This route will get student based on the id provided.
    :param email: student's ID, email address
    :return: student object
    """
    return await StaffManager.get_staff_by_email(**email)


@router.post("/staffs", status_code=status.HTTP_201_CREATED)
async def add_staff(staff_data: StaffIn):
    """
    this will register a user
    :param staff_data: student's data will be sent, pydantic model.
    :return: created user.
    """
    return await StaffManager.add_staff(staff_data=staff_data)


@router.put("/staffs/{id}")
async def update_staff(id_: int, staff_data: StaffIn):
    """
    This updates staff data in the database
    :param id_: id of the staff that wants to update their details
    :param staff_data: data of the staff
    :return: updated details of the staff
    """
    return await StaffManager.update_staff_details(staff_id=id_, staff_data=staff_data)


@router.put("/staffs/")
async def change_staff_role(staff_id: int, role):
    """
    it changes the staff's role
    :return:
    """
    return await StaffManager.upgrade_downgrade_staff(staff_id, role)


@router.put("/students/{id}")
async def delete_staff(staff_id):
    """
    this deletes a staff with the supplied id from the database permanently.
    :param staff_id: staff to delete id
    :return: None
    """
    return await StaffManager.delete_staff(staff_id)


