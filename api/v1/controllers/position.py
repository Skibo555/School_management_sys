from bson import ObjectId
from fastapi import HTTPException, status

from ..database.database import engine
from ..models.enums import PositionHeld
from ..models.user import User, Position


class PositionManager:
    @staticmethod
    async def put_position(user_id: str, position_data):
        try:
            user_obj_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

        # Retrieve the User instance from the database
        user = await engine.find_one(User, User.id == user_obj_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        current_position = await engine.find_one(Position, Position.user_id == user_obj_id)
        if not current_position:
            position_user_id = user.id
            create_position = Position(user_id=position_user_id, **position_data.dict())
            save_position = await engine.save(create_position)
            return save_position
        notice = []
        if current_position.class_ == position_data.class_:
            if current_position.course == position_data.course:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="This user is already assigned this position")
            message = "This user has a position in this class. But you can go ahead to give him/her another position"
            notice.append(message)

        position_user_id = user.id

        # Create the Position instance with the User instance
        create_position = Position(user_id=position_user_id, **position_data.dict())
        save_position = await engine.save(create_position)
        return {
            "position": save_position,
            "notice": str(notice[0])
        }

    @staticmethod
    async def strip_position(user_id):
        try:
            user_obj_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
        check_user = await engine.find_one(Position, Position.user_id == user_obj_id)
        if not check_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user has not position yet.")

        return await engine.delete(check_user)
