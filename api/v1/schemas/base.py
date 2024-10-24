from pydantic import BaseModel, EmailStr


class Base(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    department: str

