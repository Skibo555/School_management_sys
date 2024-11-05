from fastapi import APIRouter, status, Depends, Request

from ..controllers.course import CourseManager
from ..utils.utils import is_admin, is_lecturer, is_student
from ..schemas.requests import CreateCourseIn, CourseUpdateForm


router = APIRouter(prefix="api/courses", tags=["Courses"])


@router.post("/", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(is_lecturer), Depends(is_admin)])
async def create_course(course_data: CreateCourseIn, request: Request):
    creator_id = request.state.user
    course_created = await CourseManager.create_course(course_data, creator_id)
    return course_created


@router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(is_admin), Depends(is_lecturer)])
async def get_courses():
    courses = await CourseManager.get_course()
    return courses


@router.get("/{id}", status_code=status.HTTP_302_FOUND)
async def get_course(id_: str):
    course = await CourseManager.get_course_by_id(id_)
    return course


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_course(id_: str, course_data: CourseUpdateForm):
    course = await CourseManager.update_course(id_, course_data)
    return course


@router.patch("/{id}/status", status_code=status.HTTP_201_CREATED)
async def update_course_status(id_: str, course_status: str):
    course = await CourseManager.update_course_status(id_, course_status)
    return course


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id_: str):
    await CourseManager.delete_course(id_)


