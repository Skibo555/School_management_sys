from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from ..models.user import Base

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)


async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
