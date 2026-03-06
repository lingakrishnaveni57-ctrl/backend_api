from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

