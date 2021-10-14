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
    editedd_at: datetime 

    class Config: 
        orm_mode = True 
