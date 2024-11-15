import uvicorn
from decouple import config
# from v1.app import app


if __name__ == "__main__":
    uvicorn.run("api.v1.app:app", host=config("HOST"), port=int(config("PORT")), reload=True)
