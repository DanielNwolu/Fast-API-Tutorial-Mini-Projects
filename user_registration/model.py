from pydantic import BaseModel, EmailStr, constr, ValidationError,validator
import re

class UserRegistration(BaseModel):
    username: constr(min_length=4, max_length=20)
    email: EmailStr

    password: constr(
        min_length=8,
    )

    @validator('password')
    def validate_password(cls, v):
        if not re.match("^(?=.*[A-Z])(?=.*[!@#$%^&*()])(?=.*[0-9]).*$", v):
            raise ValueError(
                "Password must contain at least one uppercase letter, one special character, and one digit"
            )
        return v