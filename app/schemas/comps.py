
from datetime import datetime 
from pydantic import BaseModel, validator, ValidationError

from app.utils.time import unix_to_utc_datetime

class CompetitionSubmit(BaseModel):

    title: str 
    description: str 
    end_time: datetime 
    test_start: datetime 
    test_end: datetime 

    @validator("end_time", pre=True)
    def end_time_validate(cls, end_time):
        return unix_to_utc_datetime(end_time)

    @validator("test_start", pre=True)
    def test_start_validate(cls, test_start):
        return unix_to_utc_datetime(test_start)
    
    @validator("test_end", pre=True)
    def test_end_validate(cls, test_end):
        return unix_to_utc_datetime(test_end)

class Competition(CompetitionSubmit):

    id: int 
    owner: str 
    created: datetime 
    edited_at: datetime 
