from pydantic import BaseModel, EmailStr
from typing import Optional


class UsersBase(BaseModel):
    email: EmailStr
    username: str 
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    description: Optional[str] = None


class LimitedUser(BaseModel):
    username: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    description: Optional[str] = None

# so password used when creating/authorizing user, but not saved
class UserLogin(BaseModel):
    email: EmailStr 
    password: str 

class UserRegister(BaseModel):
    email: EmailStr 
    username: str 
    password: str 

class Users(UsersBase):
    id: int

    class Config:
        orm_mode = True


class AuthUser(Users):
    hashed_password: str
