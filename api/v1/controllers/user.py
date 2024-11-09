from bson import ObjectId

from decouple import config
from fastapi import HTTPException, status, Request
from passlib.context import CryptContext

from ..database.database import engine
from ..models.user import User, Position
from ..models.enums import Roles, StudentStatus, PositionHeld
from .auth import AuthManager
from ..services.send_email import send_email
from ..utils.utils import create_reset_password_token, verify_reset_link


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:

    @staticmethod
    async def register_user(user_info):
        user_info.password = pwd_context.hash(user_info.password)
        check = await engine.find_one(User, User.email == user_info.email)
        if check:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        if user_info.role not in [Roles.student.name, Roles.admin.name, Roles.lecturer.name, Roles.supper_admin.name]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't assign such role")
        user_info = User(**user_info.dict())
        new_user = await engine.save(user_info)
        return AuthManager.encode_token(new_user)

    @staticmethod
    async def login(user_info):
        check_user = await engine.find_one(User, User.email == user_info.email)
        if not check_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password or email. User might not be in our record.")
        if not pwd_context.verify(user_info.password, check_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password or email. password issues")
        return AuthManager.encode_token(check_user)

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

    # @staticmethod
    # async def update_user_role(user_id, user_role):
    #     try:
    #         user_obj_id = ObjectId(user_id)
    #     except Exception:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
    #     if user_role not in [Roles.student.name, Roles.admin.name, Roles.lecturer.name, Roles.supper_admin.name]:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't assign such role")
    #     user = await engine.find_one(User, User.id == user_obj_id)
    #     if not user:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    #     user.role = user_role
    #
    #     return await engine.save(user)

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

    @staticmethod
    async def request_reset_password(email):
        check_user = await engine.find_one(User, User.email == email)
        if not check_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
        token = create_reset_password_token(email)
        forget_password_url = f"{config('BASE_URL')}:{config('PORT')}/api/user/reset-password?token={token}"
        message = (f"Hi\nYou requested to change your password fon our website\nPlease click this"
                   f"the link below to reset your password\n\nLink {forget_password_url}\nPlease note that this link"
                   f"will expire in the next 30 minutes.")
        send_email(subject="Reset Password Link From Jodna", recipient=email, body=message)
        return "A link has been sent to your email, follow the link to reset your password"

    @staticmethod
    async def reset_password(token, password):
        password_data = password.dict()
        if password_data["new_password"] != password_data["confirm_password"]:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Your new_password and confirm_password must match")
        user_email = verify_reset_link(token)
        user = await engine.find_one(User, User.email == user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        hashed_password = pwd_context.hash(password_data["new_password"])
        user.password = hashed_password
        await engine.save(user)
        message = "You have successfully changed your password"
        return message

    # @staticmethod
    # async def delete_all_users():
    #     users = await engine.find(User)
    #     dele = [await engine.delete(user) for user in users]
