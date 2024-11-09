from fastapi import APIRouter, status

from ..schemas.requests import UserCreateSchema, LoginForm, PasswordResetEmailIn, PasswordResetIn
from ..models.user import Education

from ..controllers.user import UserManager

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: UserCreateSchema):
    # request.education = eduction
    user_data = request
    access_token = await UserManager.register_user(user_data)
    return {
        "access_token": access_token
    }


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: LoginForm):
    access_token = await UserManager.login(data)
    return {
        "access_token": access_token
    }


@router.post("/change_password")
async def request_reset_password(email: PasswordResetEmailIn):
    user_email = email.email
    message = await UserManager.request_reset_password(user_email)
    return message


@router.post("/reset-password/{token}")
async def reset_password(password: PasswordResetIn, token: str):
    return await UserManager.reset_password(token, password)

