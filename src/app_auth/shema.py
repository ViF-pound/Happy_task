import datetime

from pydantic import BaseModel, EmailStr


class Register(BaseModel):

    user_name: str
    email: EmailStr
    password: str

class Login(BaseModel):

    email: EmailStr
    password: str

class Update(BaseModel):

    user_name: str | None
    email: EmailStr | None
    password: str | None

class ReturnProfile(BaseModel):

    id: int
    user_name: str
    email: EmailStr
    created_at: datetime.date