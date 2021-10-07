from typing import Optional 

from pydantic import BaseModel 

class UserBase(BaseModel):
    email: str 

# so password used when creating user, but never again accessed
class UserCreate(UserBase): 
    password: str 

class User(UserBase):
    id: int 

    class Config:
        orm_mode = True 