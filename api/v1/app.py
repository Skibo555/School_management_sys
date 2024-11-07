from fastapi import FastAPI, status, APIRouter

from .routes import user, course, auth, admin


app = FastAPI()

app.include_router(user.router)
app.include_router(course.router)
app.include_router(auth.router)
app.include_router(admin.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def index():
    message = {
        "message": "You are welcome to JODNA school management System home page.",
        "status_code": status.HTTP_200_OK
    }

    return message

