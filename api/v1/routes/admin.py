from fastapi import APIRouter, status, Depends

from ..schemas.requests import UserCreateSchema
from ..schemas.response import UserOut
from ..models.user import Education

from ..controllers.user import UserManager
from ..utils.utils import oauth2_schema, is_admin

router = APIRouter(prefix='/api/admin', tags=["Admin Panel"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register(request: UserCreateSchema, eduction_data: Education, role=Depends(is_admin), user=Depends(oauth2_schema)):
    password = request.password
    request.education = eduction_data
    user_data = request
    await UserManager.register_user(user_data)
    new_user_data = {
        "password": password,
        "email": request.email
    }
    return {
        "message": "You have successfully created a new user",
        "login details": new_user_data
    }


