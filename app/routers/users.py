from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.schemas.users as schemas
import app.models.users as models
from app.utils.security import JWTBearer, get_auth_user
from app.utils.exceptions import UserNotFoundException
from app.db import get_db

router = APIRouter()

@router.post("/user/", response_model=schemas.Users)
def create_user(user: schemas.UserAuth, db: Session = Depends(get_db)):
    db_user = models.Users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return models.Users.create_user(db=db, user=user)


@router.get("/users/", dependencies=[Depends(JWTBearer())], response_model=List[schemas.Users])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = models.Users.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/user/{user_id}", response_model=schemas.Users)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = models.Users.get_user(db, user_id=user_id)
    if db_user is None:
        raise UserNotFoundException
    return db_user


@router.get("/user/{user_email}", response_model=schemas.Users) 
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
    db_user = models.Users.get_user_by_email(db, user_email)
    if db_user is None:
        raise UserNotFoundException
    return db_user 


@router.get("user/current", response_model=schemas.Users)
def get_current_user(user = Depends(get_auth_user)):
    return user 
