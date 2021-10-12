from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.users as schemas
import app.models.users as models
from app.utils.security import JWTBearer
from app.utils.exceptions import UserNotFoundException
from app.db import get_db

router = APIRouter()


# if you do GET id/email paths separately it WILL fail 
# whether path or query parameter, one will overlap with the other in path parsing
@router.get("/user/", dependencies=[Depends(JWTBearer)], response_model=schemas.Users)
def get_user(user_id: int = None, user_email: str = None, db: Session = Depends(get_db)):
    if user_id is None and user_email is None:
        raise HTTPException(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            msg="user_id or user_email required"
        )
    if user_id is not None: 
        db_user = models.Users.get_user(db, user_id=user_id)
    if user_email is not None:
        db_user = models.Users.get_user_by_email(db, user_email)
    if db_user is None:
        raise UserNotFoundException
    return db_user


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


@router.get("user/current", response_model=schemas.Users)
def get_current_user(user = Depends(models.Users.get_auth_user)):
    return user 
