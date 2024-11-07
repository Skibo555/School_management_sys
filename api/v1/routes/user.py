from fastapi import APIRouter, status, Depends
from typing import List

from ..schemas.response import UserOut
from ..utils.utils import oauth2_schema, is_admin_or_lecturer, is_admin
from ..controllers.user import UserManager
from ..schemas.requests import UserUpdateForm

router = APIRouter(prefix='/api/user', tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserOut])
async def get_users(user=Depends(oauth2_schema), role=Depends(is_admin_or_lecturer)):
    return await UserManager.get_users()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user_by_id(id_: str, user=Depends(oauth2_schema)):
    users = await UserManager.get_user_by_id(id_)
    return users


@router.patch("/", status_code=status.HTTP_200_OK, response_model=UserOut)
async def update_user(user_data: UserUpdateForm, user=Depends(oauth2_schema), role=Depends(is_admin_or_lecturer)):
    users = await UserManager.update_user_data(update_form_data=user_data, user_id=user.id)
    return users


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def update_user_role(user_id: str, user_role, user=Depends(oauth2_schema), role=Depends(is_admin_or_lecturer)):
    return await UserManager.update_user_role(user_id, user_role)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, user=Depends(oauth2_schema), role=Depends(is_admin_or_lecturer)):
    await UserManager.delete_user(user_id)


@router.patch("/{user_id}/status", status_code=status.HTTP_200_OK, response_model=UserOut)
async def change_user_status(user_id: str, user_status, user=Depends(oauth2_schema), role=Depends(is_admin)):
    return await UserManager.change_user_status(user_id, user_status)


# @router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_all_users():
#     return await UserManager.delete_all_users()
