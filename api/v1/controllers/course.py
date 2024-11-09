from bson import ObjectId

from fastapi import HTTPException, status

from ..models.courses import Course, CourseStatus
from ..database.database import engine


class CourseManager:
    @staticmethod
    async def create_course(course_info, user_id):
        try:
            ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid course ID format")
        course_data = course_info.dict()
        course_data["course_owner_id"] = user_id
        new_course = Course(**course_data)
        return await engine.save(new_course)

    @staticmethod
    async def get_courses():
        courses = await engine.find(Course)
        return courses

    @staticmethod
    async def get_course_by_id(course_id):
        try:
            course_obj_id = ObjectId(course_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid course ID format")
        course = await engine.find_one(Course, Course.id == course_obj_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="course not found")
        return course

    @staticmethod
    async def update_course(course_id, data):
        try:
            course_obj_id = ObjectId(course_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid course ID format")
        course = await engine.find_one(Course, Course.id == course_obj_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="course not found")
        course_data = data.dict(exclude_unset=True)
        for field, value in course_data.items():
            setattr(course, field, value)

        # Save the updated user directly
        updated_user = await engine.save(course)

        return updated_user

    @staticmethod
    async def update_course_status(course_id, course_status):
        if course_status not in [CourseStatus.normal.name, CourseStatus.suspended.name, CourseStatus.withdrawn.name]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid course status")
        try:
            course_obj_id = ObjectId(course_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid course ID format")
        course = await engine.find_one(Course, Course.id == course_obj_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="course not found")
        course.course_status = course_status
        return await engine.save(course)

    @staticmethod
    async def delete_course(course_id):
        try:
            course_obj_id = ObjectId(course_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid course ID format")
        course = await engine.find_one(Course, Course.id == course_obj_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="course not found")
        await engine.delete(course)
