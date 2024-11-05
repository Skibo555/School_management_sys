from fastapi import FastAPI, status, APIRouter

from .routes import staff, user


app = FastAPI()

# app.include_router(admins.router)
app.include_router(staff.router)
# app.include_router(students.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def index():
    message = {
        "message": "You are welcome to JODNA school management System home page.",
        "status_code": status.HTTP_200_OK
    }

    return message

