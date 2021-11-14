from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.schemas.quotes as schemas
import app.models.quotes as models 
from app.utils.exceptions import FailedRetrievalException
from app.utils.security import JWTBearer
from app.db import get_db, db as app_db 
from app.utils.quotes import get_min_max_times 
from app.utils.constants import IntervalName

router = APIRouter()

@router.get("/quote/symbols/", dependencies=[Depends(JWTBearer())])
def get_quote_symbols(db: Session = Depends(get_db)):
    return models.Symbol.get_symbols(db)

@router.get("/quote/range/", dependencies=[Depends(JWTBearer())], response_model=schemas.QuoteTimeRange)
def get_allowed_quote_time_range(db: Session = Depends(get_db)):
    min_, max_ = get_min_max_times(db)        
    return {
        "min_time": min_,
        "max_time": max_, 
    }

@router.get("/quote/intervals/", dependencies=[Depends(JWTBearer())])
def get_intervals():
    return IntervalName.get_mapping()

# Note: interval refers to candle size, not a set of quotes 
@router.get("/quote/{interval}/{symbol}", response_model=schemas.Quote)
def get_single_quote(symbol: str, interval: IntervalName, time: datetime, db: Session = Depends(get_db)):
    # Get specific Quote_xxx model object from DB
    if interval == IntervalName.minute:
        quote = models.Quote_1m.get_single_quote(db, symbol=symbol, time=time)
    elif interval == IntervalName.fiveMinute:
        quote = models.Quote_5m.get_single_quote(db, symbol=symbol, time=time)
    elif interval == IntervalName.fifteenMinute:
        quote = models.Quote_15m.get_single_quote(db, symbol=symbol, time=time)
    elif interval == IntervalName.thirtyMinute:
        quote = models.Quote_30m.get_single_quote(db, symbol=symbol, time=time)
    elif interval == IntervalName.hour:
        quote = models.Quote_1h.get_single_quote(db, symbol=symbol, time=time)
    elif interval == IntervalName.day:
        quote = models.Quote_1d.get_single_quote(db, symbol=symbol, time=time)
    elif interval == IntervalName.week:
        quote = models.Quote_1w.get_single_quote(db, symbol=symbol, time=time)
    else:
        raise ValueError(f'Invalid interval {interval.value} (accepted: 1m, 5m, 15m, 30m, 1h, 1d, 1w)')

    if quote is None:
        raise HTTPException(status_code=404, detail='Quote not found')

    # Convert to general Quote schema object implicitly
    return quote


# broken due to pydantic validation BS
# @router.get("/quote/{interval}/{symbol}/all", response_model=schemas.Quote)
# def get_single_quote(symbol: str, interval: IntervalName, db: Session = Depends(get_db)):
    
#     if interval == IntervalName.minute:
#         quote = models.Quote_1m.get_all_quotes_for_symbol(db, symbol=symbol)
#     elif interval == IntervalName.fiveMinute:
#         quote = models.Quote_5m.get_all_quotes_for_symbol(db, symbol=symbol)
#     elif interval == IntervalName.fifteenMinute:
#         quote = models.Quote_15m.get_all_quotes_for_symbol(db, symbol=symbol)
#     elif interval == IntervalName.thirtyMinute:
#         quote = models.Quote_30m.get_all_quotes_for_symbol(db, symbol=symbol)
#     elif interval == IntervalName.hour:
#         quote = models.Quote_1h.get_all_quotes_for_symbol(db, symbol=symbol)
#     elif interval == IntervalName.day:
#         quote = models.Quote_1d.get_all_quotes_for_symbol(db, symbol=symbol)
#     elif interval == IntervalName.week:
#         quote = models.Quote_1w.get_all_quotes_for_symbol(db, symbol=symbol)
#     else:
#         raise ValueError(f'Invalid interval {interval.value} (accepted: 1m, 5m, 15m, 30m, 1h, 1d, 1w)')

#     if quote is None:
#         raise HTTPException(status_code=404, detail='Quote not found')

#     return quote