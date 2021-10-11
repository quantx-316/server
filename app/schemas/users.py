from pydantic import BaseModel, EmailStr


class UsersBase(BaseModel):
    email: EmailStr


# so password used when creating user, but never again accessed
class UserAuth(UsersBase):
    password: str


class Users(UsersBase):
    id: int
    firstname: str = None
    lastname: str = None
    description: str = None

    class Config:
        orm_mode = True


class AuthUser(Users):
    hashed_password: str
