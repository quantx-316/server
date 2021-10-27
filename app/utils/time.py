from datetime import datetime 
from sqlalchemy.orm import Session
from app.utils.quotes import get_min_max_times
from app.utils.exceptions import BadRequestException

def get_current_time():
    return datetime.now() 

def validate_test_intervals(db: Session, start, end):

    if start >= end:
        raise BadRequestException("End must be strictly greater than start time")

    # time_start < time_end 

    min_, max_ = get_min_max_times(db)

    if start < min_ or end > max_:
        raise BadRequestException("Given start/end times are out of min/max range")

