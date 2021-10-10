from pydantic import BaseModel 

class UsersBase(BaseModel):
    email: str 

# so password used when creating user, but never again accessed
class UsersCreate(UsersBase): 
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