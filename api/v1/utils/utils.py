import datetime
from typing import Optional
from bson import ObjectId

import jwt
from decouple import config
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from starlette.requests import Request

from ..database.database import engine
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

        try:
            token = jwt.decode(res.credentials, JWT_SECRET_KEY, algorithms=["HS256"])
            user_id = token["id"]

            # Convert string ID to ObjectId
            user_id_obj = ObjectId(user_id)

            # Try to find the user and print the query
            user_data_from_db = await engine.find_one(User, User.id == user_id_obj)

            if not user_data_from_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found in database"
                )

            setattr(request.state, 'user', user_data_from_db)
            print("User role:", getattr(request.state.user, 'role', None))

            return user_data_from_db

        except jwt.InvalidSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Expired signature")
        except jwt.InvalidTokenError as ex:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"{ex}")


oauth2_schema = CustomHTTPBearer()


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password_hash(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def is_admin_or_lecturer(user=Depends(oauth2_schema)):
    # Check if the logged-in user's role is either admin or lecturer
    if user.role not in {Roles.admin.name, Roles.lecturer.name}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this operation"
        )


def is_student(user=Depends(oauth2_schema)):
    if not user.role == Roles.student.name:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to perform this operation as a student")


def is_lecturer(user=Depends(oauth2_schema)):
    if not user.role == Roles.lecturer.name:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to perform this operation as a lecturer")


def is_admin(user=Depends(oauth2_schema)):
    if not user.role == Roles.admin.name:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to perform this operation as an admin")


def create_reset_password_token(user):
    try:
        print(user.email)
        data = {
            "user_email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        encode_url = jwt.encode(payload=data, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
        return encode_url
    except Exception as Ex:
        raise Ex


def verify_reset_link(token):
    try:
        data = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_email = data["user_email"]
        exp_timestamp = data["exp"]

        if exp_timestamp:
            expiration_time = datetime.datetime.fromtimestamp(exp_timestamp)
            current_time = datetime.datetime.utcnow()
            if current_time > expiration_time:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
            return user_email
    except jwt.InvalidSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Expired signature")
    except jwt.InvalidTokenError as ex:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"{ex}")
