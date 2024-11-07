from motor.motor_asyncio import AsyncIOMotorClient

from odmantic import AIOEngine

client = AsyncIOMotorClient("mongodb://localhost:27017/")
engine = AIOEngine(client=client, database="example2_db")


async def get_db():
    yield engine


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
#
# from ..models.user import Base
#
# db_path = "Users/mac/Desktop/Projects/JODNA/school_management/School_management_sys/api/school_management.db"
#
# engine = create_engine(f"sqlite:////{db_path}", echo=True)
# Base.metadata.create_all(engine)
#
# DBSession = sessionmaker(bind=engine)
#
#
# async def get_db():
#     db = DBSession()
#     try:
#         yield db
#     finally:
#         db.close()
