from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from ..models.user import Base

db_path = "Users/mac/Desktop/Projects/JODNA/school_management/School_management_sys/api/school_management.db"

engine = create_engine(f"sqlite:////{db_path}", echo=True)
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)


async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
