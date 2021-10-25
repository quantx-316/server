from os import stat
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.users as schemas
import app.models.users as models
from app.utils.security import JWTBearer
from app.utils.exceptions import AuthenticationException, UserNotFoundException
from app.db import get_db

router = APIRouter(
    prefix="/user"
)


# if you do GET id/email paths separately it WILL fail 
# whether path or query parameter, one will overlap with the other in path parsing
@router.get("/", dependencies=[Depends(JWTBearer())], response_model=schemas.Users)
def get_user(username: str = None, db: Session = Depends(get_db)):
    if username is None:
        raise HTTPException(
            status_code=422,
            msg="user_id or user_email required"
        )
    if username is not None: 
        db_user = models.Users.get_user_by_username(db, username)
    if db_user is None:
        raise UserNotFoundException
    return db_user


@router.post("/", response_model=schemas.Users)
def create_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = models.Users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return models.Users.create_user(db=db, user=user)


@router.put("/", dependencies=[Depends(JWTBearer())], response_model=schemas.Users)
def update_user(new_user: schemas.Users, db: Session = Depends(get_db), old_user = Depends(models.Users.get_auth_user)):

    if old_user.email != new_user.email or old_user.username != new_user.username or old_user.id != new_user.id: 
        raise AuthenticationException(f"Not owner of requested update users {old_user.email} vs {new_user.email}, {old_user.username} vs {new_user.username}, {old_user.id} vs {new_user.id}")

    return models.Users.update_user(db, old_user, new_user) 


@router.get("/all/", dependencies=[Depends(JWTBearer())], response_model=List[schemas.Users])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = models.Users.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/current/", dependencies=[Depends(JWTBearer())], response_model=schemas.Users)
def get_current_user(user = Depends(models.Users.get_auth_user)):
    return user 
