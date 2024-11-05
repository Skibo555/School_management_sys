from fastapi import APIRouter, Request, status, Depends

from ..utils.utils import is_admin, is_student, is_lecturer
from ..controllers.user import UserManager
from ..schemas.requests import UserUpdateForm

router = APIRouter(prefix='/api/user', tags=["Staffs Panel"])


@router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(is_admin), Depends(is_lecturer)])
async def get_users():
    users = await UserManager.get_users()
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(is_admin), Depends(is_lecturer)])
async def get_user_by_id(id_: str):
    users = await UserManager.get_user_by_id(id_)
    return users


@router.patch("/", status_code=status.HTTP_200_OK, dependencies=[Depends(is_admin), Depends(is_lecturer)])
async def update_user(user_data: UserUpdateForm, request: Request):
    users = await UserManager.update_user_data(user_data, request.user.state)
    return users


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(is_admin), Depends(is_lecturer)])
async def update_user_status(user_id: str, user_status):
    users = await UserManager.update_user_data(user_id, user_status)
    return users


@router.patch("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(is_admin), Depends(is_lecturer)])
async def delete_user(user_id: str):
    await UserManager.delete_user(user_id)


@router.patch("/{user_id}/status", status_code=status.HTTP_200_OK, dependencies=[Depends(is_admin), Depends(is_lecturer)])
async def change_user_status(user_id: str, user_status):
    users = await UserManager.update_user_status(user_id, user_status)
    return users

