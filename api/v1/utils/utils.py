from typing import Optional

import jwt
from decouple import config
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from starlette.requests import Request

from ..database.database import get_db
from ..models.enums import Roles
from ..models.user import User

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = config('ALGORITHM')
JWT_SECRET_KEY = config('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = config('JWT_REFRESH_SECRET_KEY')

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)
        db = get_db()

        try:
            token = jwt.decode(res.credentials, config("JWT_SECRET_KEY"), algorithms=[ALGORITHM])
            user_id = token["ObjectId"]
            if not user_id:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User Not Found")
            user_data_from_db = await db.find_one(User, User.OjectId == user_id)
            request.state.user = user_data_from_db
            return user_data_from_db
        except jwt.InvalidSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Expired signature")
        except jwt.InvalidTokenError as ex:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Token {ex}")


oauth2_schema = CustomHTTPBearer()


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password_hash(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def is_student(request: Request):
    if not request.state.user["role"] == Roles.student:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this operation")


def is_lecturer(request: Request):
    if not request.state.user["role"] == Roles.lecturer:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this operation")


def is_admin(request: Request):
    if not request.state.user["role"] == Roles.admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this operation")

