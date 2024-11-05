from pydantic import BaseModel, EmailStr


class Base(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    middleName: str
    department: str

