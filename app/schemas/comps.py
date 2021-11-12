
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


# from pydantic import BaseModel, validator, ValidationError 
# from app.utils.time import unix_to_utc_datetime
# from app.utils.constants import IntervalName 

# intervals = [interval.value for interval in IntervalName]
# intervals_set = set(intervals)

# class BacktestSubmit(BaseModel):
#     algo: int 
#     test_interval: str 
#     test_start: datetime 
#     test_end: datetime 

#     @validator("test_interval")
#     def test_interval_validate(cls, test_interval):
#         if test_interval not in intervals_set:
#             raise ValidationError("Interval is not valid")
#         return test_interval 

#     # may need extra validation on the allowed min / max dates 
#     @validator("test_start", pre=True)
#     def test_start_validate(cls, test_start):
#         return unix_to_utc_datetime(test_start)
    
#     @validator("test_end", pre=True)
#     def test_end_validate(cls, test_end):
#         return unix_to_utc_datetime(test_end)

# class Backtest(BacktestSubmit):
#     id: int 
#     owner: int
#     result: Optional[str]
#     score: Optional[int]
#     code_snapshot: str
#     created: datetime
