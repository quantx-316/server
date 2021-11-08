from pydantic import BaseModel 
from datetime import datetime 


class AlgoBase(BaseModel):
    title: str 
    code: str 

class AlgoSubmit(AlgoBase):
    pass 

class AlgoDB(AlgoBase):
    id: int 
    owner: int 
    created: datetime 
    edited_at: datetime 
    public: bool

    class Config: 
        orm_mode = True 
