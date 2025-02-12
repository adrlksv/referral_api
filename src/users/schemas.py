from pydantic import BaseModel, EmailStr


class SUserRegister(BaseModel):
    email: EmailStr
    login: str
    password: str


class SUserLogin(BaseModel):
    email: EmailStr
    password: str
