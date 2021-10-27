from typing import Any, Optional
from pydantic import BaseModel, validator, ValidationError 
from datetime import datetime 

from app.utils.constants import IntervalName 

intervals = [interval.value for interval in IntervalName]
intervals_set = set(intervals)

class BacktestSubmit(BaseModel):
    algo: int 
    test_interval: str 
    test_start: datetime 
    test_end: datetime 

    @validator("test_interval")
    def test_interval_validate(cls, test_interval):
        if test_interval not in intervals_set:
            raise ValidationError("Interval is not valid")
        return test_interval 

    # may or may not need 
    # @validator("test_start", pre=True)
    # def test_start_validate(cls, test_start):
    #     return datetime.utcfromtimestamp(test_start)
    
    # @validator("test_end", pre=True)
    # def test_end_validate(cls, test_end):
    #     return datetime.utcfromtimestamp(test_end) 

class Backtest(BacktestSubmit):
    id: int 
    owner: int
    result: Optional[str]
    code_snapshot: str
    created: datetime
