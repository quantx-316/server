from datetime import datetime

from pydantic import BaseModel 

class Quote(BaseModel):
    time: datetime
    symbol: str
    price_open: float
    price_high: float
    price_low: float
    price_close: float

    class Config:
        orm_mode = True