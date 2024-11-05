from fastapi import HTTPException, status

from ..models.courses import Course
from ..database.database import get_db
from ..schemas.requests import CourseUpdateForm


class CourseManager:
    @staticmethod
    async def create_course(course_info, user_id):
        db = get_db()
        course_info["course_owner_id"] = user_id
        new_course = Course(**course_info)
        return await db.save(new_course)

    @staticmethod
    async def get_course():
        db = get_db()
        result = await db.find(Course)
        return result

    @staticmethod
    async def get_course_by_id(course_id):
        db = get_db()
        course = await db.find_one(Course, Course.ObjectId == course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="course not found")
        return course

    @staticmethod
    async def update_course(course_id, data):
        db = get_db()
        course = await db.find_one(Course, Course.ObjectId == course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="course not found")
        course_update = CourseUpdateForm(**data)
        updated = await db.model_update(course_update)
        return await db.save(updated)

    @staticmethod
    async def update_course_status(course_id, course_status):
        db = get_db()
        course = await db.find_one(Course, Course.ObjectId == course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="course not found")
        course.status = course_status
        return await db.save(course)

    @staticmethod
    async def delete_course(course_id):
        db = get_db()
        course = await db.find_one(Course, Course.ObjectId == course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="course not found")
        db.delete(course)




