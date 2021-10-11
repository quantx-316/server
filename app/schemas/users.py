from pydantic import BaseModel, EmailStr

class UsersBase(BaseModel):
    email: EmailStr

# so password used when creating user, but never again accessed
class UserAuth(UsersBase): 
    password: str 

class Users(UsersBase):
    id: int 

    class Config:
        orm_mode = True 

class AuthUser(Users):
    hashed_password: str 

class Profile(BaseModel):
    uid: int 
    firstname: str 
    lastname: str 
    description: str 

    class Config: 
        orm_mode = True 