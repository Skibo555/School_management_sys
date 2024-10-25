from fastapi import APIRouter, Request, status
from ..schemas.requests import StaffIn, StudentIn, StudentUpdateFormIn
from ..controllers.students import StudentAffairs


# This is a router that will be used to bind this route to the app in the app.py file
router = APIRouter(prefix='/api/user', tags=["Staffs Panel"])


@router.get("/")
async def get_courses(student_id: int):

    return await StudentAffairs.get_all_courses(student_id)


@router.post("/{course_id}")
async def delete_course(course_id):
    return await StudentAffairs.delete_course(course_id)
