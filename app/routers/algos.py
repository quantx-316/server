from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.schemas.algos as algos_schemas
import app.models.algos as algos_models
import app.models.users as users_models  
from app.utils.security import JWTBearer
from app.utils.exceptions import UserNotFoundException
from app.db import get_db

router = APIRouter(
    prefix="/algo",
    dependencies=[Depends(JWTBearer())],
)


@router.post("/", response_model=algos_schemas.AlgoDB)
def create_algo(
    algo: algos_schemas.AlgoSubmit, 
    user = Depends(users_models.Users.get_auth_user), 
    db: Session = Depends(get_db)
):
    return algos_models.Algorithm.create_algo(db, algo, user)


@router.put("/", response_model=algos_schemas.AlgoDB)
def update_algo(
    old_algo: algos_schemas.AlgoDB, 
    new_algo: algos_schemas.AlgoDB, 
    user = Depends(users_models.Users.get_auth_user), 
    db: Session = Depends(get_db)
):
    return algos_models.Algorithm.update_algo(db, old_algo, new_algo, user)


@router.delete("/")
def delete_algo(
    algo: algos_schemas.AlgoSubmit, 
    user = Depends(users_models.Users.get_auth_user), 
    db: Session = Depends(get_db)
):
    return algos_models.Algorithm.delete_algo(db, algo, user)


@router.get("/all/", response_model=List[algos_schemas.AlgoDB])
def get_algos(user=Depends(users_models.Users.get_auth_user), db: Session = Depends(get_db)):
    return algos_models.Algorithm.get_algo_by_user_id(db, user)


@router.get("/", response_model=algos_schemas.AlgoDB)
def get_algo(algo_id: int, user=Depends(users_models.Users.get_auth_user), db: Session = Depends(get_db)):
    return algos_models.Algorithm.get_algo_by_id(db, algo_id, user)

