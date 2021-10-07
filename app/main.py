from typing import List 
from datetime import datetime 
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session 
from . import models, schemas 
from .db import DB
from .config import settings 

app = FastAPI()
db = DB(settings) 

def get_db():
    session = db.get_session()
    try: 
        yield session
    finally:
        session.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User.get_user_by_email(db, email=user.email)
    if db_user: 
        raise HTTPException(status_code=400, detail="Email already registered")
    return models.User.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = models.User.get_users(db, skip=skip, limit=limit)
    return users 

@app.get("/user/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = models.User.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user 

@app.get("/quote/{symbol}/all", response_model=List[schemas.Quote])
def get_all_quotes_for_symbol(symbol: str, db: Session = Depends(get_db)):
    quotes = models.Quote.get_all_quotes_for_symbol(db, symbol=symbol)
    if quotes is None:
        raise HTTPException(status_code=404, detail='Symbol not found')
    return quotes

@app.get("/quote/{symbol}", response_model=schemas.Quote)
def get_single_quote(symbol: str, time: datetime, db: Session = Depends(get_db)):
    quote = models.Quote.get_single_quote(db, symbol=symbol, time=time)
    if quote is None:
        raise HTTPException(status_code=404, detail='Quote not found')
    return quote