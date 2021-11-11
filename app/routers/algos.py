from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params 
from fastapi_pagination.ext.sqlalchemy import paginate 

import app.schemas.algos as algos_schemas
import app.models.algos as algos_models
import app.models.users as users_models  
from app.utils.security import JWTBearer
from app.utils.querying import AlgorithmQuery
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
    new_algo: algos_schemas.AlgoDB, 
    user = Depends(users_models.Users.get_auth_user), 
    db: Session = Depends(get_db)
):
    return algos_models.Algorithm.update_algo(db, new_algo, user)


@router.delete("/")
def delete_algo(
    algo_id: int, 
    user = Depends(users_models.Users.get_auth_user), 
    db: Session = Depends(get_db)
):
    return algos_models.Algorithm.delete_algo(db, algo_id, user)

@router.get("/public/")
def get_public_algos(
    username: str,
    sort_by: str,
    sort_direction: str,
    db: Session = Depends(get_db),
    params: Params = Depends(),
    code_query: str = None, 
):

    res = algos_models.Algorithm.best_public_algo_backtests(
        db,
        username,
        params.page,
        params.size,
        sort_by,
        sort_direction,
        code_query, 
    )

    return res

@router.get("/all/", response_model=Page[algos_schemas.AlgoDB])
def get_algos(
    user=Depends(users_models.Users.get_auth_user), 
    db: Session = Depends(get_db),
    params: Params = Depends(),
    sort_by: str = None,
    sort_direction: str = None,
    search_by: str = None, 
    search_query: str = None, 
    exclusive: bool = None
):

    query = algos_models.Algorithm.get_algo_by_user(db, user)

    return AlgorithmQuery().execute_encapsulated_query(
        query, params, sort_by, sort_direction, 
        search_by, search_query, exclusive, 
    )


@router.get("/", response_model=algos_schemas.AlgoDB)
def get_algo(algo_id: int, user=Depends(users_models.Users.get_auth_user), db: Session = Depends(get_db)):
    return algos_models.Algorithm.get_algo_by_id(db, algo_id, user)
