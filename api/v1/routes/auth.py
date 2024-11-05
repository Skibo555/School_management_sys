from fastapi import APIRouter, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.requests import UserIn
from ..models.user import Education

from ..controllers.user import UserManager

router = APIRouter(prefix="api/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: UserIn, eduction_data: Education):
    request.education = eduction_data
    user_data = request
    access_token = await UserManager.register_user(user_data)
    return {
        "access_token": access_token
    }


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: OAuth2PasswordRequestForm):
    access_token = await UserManager.login(data)
    return {
        "access_token": access_token
    }

