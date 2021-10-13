from pydantic import BaseModel, EmailStr
from typing import Optional


class UsersBase(BaseModel):
    email: EmailStr
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    description: Optional[str] = None


# so password used when creating user, but never again accessed
class UserAuth(UsersBase):
    password: str


class Users(UsersBase):
    id: int

    class Config:
        orm_mode = True


class AuthUser(Users):
    hashed_password: str
