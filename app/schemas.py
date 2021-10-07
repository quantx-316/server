from typing import Optional 
from datetime import datetime

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


class Quote(BaseModel):
    time: datetime
    symbol: str
    price_open: float
    price_high: float
    price_low: float
    price_close: float

    class Config:
        orm_mode = True
