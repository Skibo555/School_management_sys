from fastapi import HTTPException, status
from passlib.context import CryptContext

from ..database.database import get_db
from ..models.user import User
from .auth import AuthManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:

    @staticmethod
    async def register_user(user_info):
        db = get_db()
        user_info["password"] = pwd_context.hash(user_info["password"])
        check = await db.find_one(User, User.email == user_info.email)
        if check:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        new_user = await db.save(user_info)
        return AuthManager.encode_token(new_user)

    @staticmethod
    async def login(user_info):
        db = get_db()
        check_user = await db.find_one(User, User.email == user_info.email)
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
        db = get_db()
        users = await db.find(User)
        return users

    @staticmethod
    async def get_user_by_id(user_id):
        db = get_db()
        check_id = await db.find_one(User, User.ObjectId == user_id)
        if not check_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        return check_id

    @staticmethod
    async def update_user_data(user_id, data):
        db = get_db()
        check_id = await db.find_one(User, User.ObjectId == user_id)
        if not check_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        to_update = User(**data)
        updated = db.model_update(to_update)
        return updated

    @staticmethod
    async def update_user_status(user_id, user_status):
        db = get_db()
        user = await db.find_one(User, User.ObjectId == user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        user.status = user_status

        return await db.save(user)

    @staticmethod
    async def delete_user(user_id):
        db = get_db()
        user = await db.find_one(User, User.ObjectId == user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        db.delete(user)

    @staticmethod
    async def change_user_role(user_id, role):
        db = get_db()
        user = await db.find_one(User, User.ObjectId == user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        user.role = role
        return await db.save(user)

