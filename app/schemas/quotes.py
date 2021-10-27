from datetime import datetime

from pydantic import BaseModel, Field

class QuoteTimeRange(BaseModel):
    min_time: datetime 
    max_time: datetime 

class Quote(BaseModel):
    candle: datetime = Field(alias='time')  # Alias takes priority when populating from ORM (arbitrary instance)
    symbol: str
    price_open: float
    price_high: float
    price_low: float
    price_close: float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True   
        
        # models.Quote_xx.candle --> schemas.Quote."time"
        # We want the user to see "time", but schema must generate "candle" because "time" 
        # is a name conflict when defining the view. 