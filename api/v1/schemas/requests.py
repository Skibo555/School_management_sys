from .base import Base


class StudentIn(Base):
    level: str
    password: str

    # @field_validator("password")
    # def check_password(self, value):
    #     # Check if password meets the length requirement
    #     if len(value) < 8:
    #         raise ValueError("Password must have at least 8 characters")
    #
    #     # Check for at least one uppercase, one lowercase, one digit, and one special character
    #     if not any(c.isupper() for c in value):
    #         raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    #     if not any(c.islower() for c in value):
    #         raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    #     if not any(c.isdigit() for c in value):
    #         raise HTTPException(status_code=400, detail="Password must contain at least one digit.")
    #     if not any(c in punctuation for c in value):
    #         raise HTTPException(status_code=400, detail="Password must contain at least one special character.")
    #
    #     return value


class StaffIn(Base):
    course: str
    password: str

    # @field_validator("password")
    # def check_password(self, value):
    #     # Check if password meets the length requirement
    #     if len(value) < 8:
    #         raise ValueError("Password must have at least 8 characters")
    #
    #     # Check for at least one uppercase, one lowercase, one digit, and one special character
    #     if not any(c.isupper() for c in value):
    #         raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    #     if not any(c.islower() for c in value):
    #         raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    #     if not any(c.isdigit() for c in value):
    #         raise HTTPException(status_code=400, detail="Password must contain at least one digit.")
    #     if not any(c in punctuation for c in value):
    #         raise HTTPException(status_code=400, detail="Password must contain at least one special character.")
    #
    #     return value


class StudentUpdateFormIn(Base):
    level: str
