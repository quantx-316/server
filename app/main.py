from typing import List 
from datetime import datetime 
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session 
from . import models, schemas 
from app.db import get_db

app = FastAPI()

from .routers import users, security

app.include_router(users.router)
app.include_router(security.router)

# # get symbols endpoint 

# @app.get("/quote/{symbol}/all", response_model=List[schemas.Quote])
# def get_all_quotes_for_symbol(symbol: str, db: Session = Depends(get_db)):
#     quotes = models.Quote.get_all_quotes_for_symbol(db, symbol=symbol)
#     if quotes is None:
#         raise HTTPException(status_code=404, detail='Symbol not found')
#     return quotes

# @app.get("/quote/{symbol}", response_model=schemas.Quote)
# def get_single_quote(symbol: str, time: datetime, db: Session = Depends(get_db)):
#     quote = models.Quote.get_single_quote(db, symbol=symbol, time=time)
#     if quote is None:
#         raise HTTPException(status_code=404, detail='Quote not found')
#     return quote