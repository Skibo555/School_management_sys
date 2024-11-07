from bson import ObjectId

from fastapi import HTTPException, status
from passlib.context import CryptContext

from ..database.database import engine
from ..models.user import User
from ..models.enums import Roles, StudentStatus
from .auth import AuthManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:

    @staticmethod
    async def register_user(user_info):
        user_info.password = pwd_context.hash(user_info.password)
        check = await engine.find_one(User, User.email == user_info.email)
        if check:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        user_info = User(**user_info.dict())
        new_user = await engine.save(user_info)
        return AuthManager.encode_token(new_user)

    @staticmethod
    async def login(user_info):
        check_user = await engine.find_one(User, User.email == user_info.email)
        if not check_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password or email.")
        if not pwd_context.verify(user_info.password, check_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password or email.")
        return AuthManager.encode_token(check_user)

    @staticmethod
    async def create_user(user_data):
        pass

    @staticmethod
    async def get_users():
        result = await engine.find(User)
        return result

    @staticmethod
    async def get_user_by_id(user_id):

        try:
            user_id = ObjectId(user_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
        check_id = await engine.find_one(User, User.id == user_id)

        if not check_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return check_id

    @staticmethod
    async def update_user_data(update_form_data, user_id):
        try:
            user_obj_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

        # Find the existing user by ID
        existing_user = await engine.find_one(User, User.id == user_obj_id)
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Get only the fields provided in the update request
        update_data = update_form_data.dict(exclude_unset=True)

        # Update the existing user object with new values
        for field, value in update_data.items():
            setattr(existing_user, field, value)

        # Save the updated user directly
        updated_user = await engine.save(existing_user)
        return updated_user

    @staticmethod
    async def update_user_role(user_id, user_role):
        try:
            user_obj_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
        if user_role not in [Roles.student.name, Roles.admin.name, Roles.lecturer.name, Roles.supper_admin.name]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't assign such role")
        user = await engine.find_one(User, User.id == user_obj_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.role = user_role

        return await engine.save(user)

    @staticmethod
    async def delete_user(user_id):
        try:
            user_obj_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
        user = await engine.find_one(User, User.id == user_obj_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        await engine.delete(user)

    @staticmethod
    async def change_user_status(user_id, user_status):
        try:
            user_obj_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
        if user_status not in [StudentStatus.active.name, StudentStatus.inactive.name]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't assign such status")
        user = await engine.find_one(User, User.id == user_obj_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.status = user_status
        return await engine.save(user)

    # @staticmethod
    # async def delete_all_users():
    #     users = await engine.find(User)
    #     dele = [await engine.delete(user) for user in users]
