from fastapi import APIRouter, status, Depends, Request
from ..controllers.course import CourseManager
from ..utils.utils import is_admin_or_lecturer, oauth2_schema
from ..schemas.requests import CreateCourseIn, CourseUpdateForm


router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_course(course_data: CreateCourseIn, user=Depends(oauth2_schema), role=Depends(is_admin_or_lecturer)):
    return await CourseManager.create_course(course_data, user.id)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_courses(user=Depends(oauth2_schema)):
    return await CourseManager.get_courses()


@router.get("/{id}", status_code=status.HTTP_302_FOUND)
async def get_course(id_: str, user=Depends(oauth2_schema)):
    return await CourseManager.get_course_by_id(id_)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_course(id_: str, course_data: CourseUpdateForm,
                        user=Depends(oauth2_schema), role=Depends(is_admin_or_lecturer)):
    return await CourseManager.update_course(id_, course_data)


@router.patch("/{id}/status", status_code=status.HTTP_201_CREATED)
async def update_course_status(id_: str, course_status: str,
                               user=Depends(oauth2_schema), role=Depends(is_admin_or_lecturer)):
    return await CourseManager.update_course_status(id_, course_status)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id_: str, user=Depends(oauth2_schema), role=Depends(is_admin_or_lecturer)):
    await CourseManager.delete_course(id_)


