from fastapi import Depends, status, HTTPException, APIRouter

from ..controllers.position import PositionManager
from ..schemas.requests import UpdateUserPosition
from ..utils.utils import is_admin_or_lecturer

router = APIRouter(prefix="/api/users", tags=["Position"])


@router.post("/{id_}/position", status_code=status.HTTP_201_CREATED)
async def put_user_in_position(id_: str, position_data: UpdateUserPosition, role=Depends(is_admin_or_lecturer)):
    return await PositionManager.put_position(user_id=id_, position_data=position_data)


@router.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
async def strip_position(id_: str, role=Depends(is_admin_or_lecturer)):
    await PositionManager.strip_position(user_id=id_)
