from typing import List
from datetime import datetime 

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.models.backtests as backtests_models
import app.schemas.backtests as backtests_schemas
import app.schemas.algos as algos_schemas
import app.models.algos as algos_models
import app.models.users as users_models  
from app.utils.security import JWTBearer
from app.utils.exceptions import UserNotFoundException
from app.db import get_db

router = APIRouter(
    prefix="/backtest",
    dependencies=[Depends(JWTBearer())]
)

@router.get("/", dependencies=[Depends(JWTBearer())])
def get_user_backtests(db: Session = Depends(get_db), user=Depends(users_models.Users.get_auth_user)):
    return backtests_models.Backtest.get_all_user_backtests(db, user.id)

@router.get("/all/", dependencies=[Depends(JWTBearer())])
def get_all_backtests(db: Session = Depends(get_db)):
    """
    Get all backtests for all users.
    """
    return backtests_models.Backtest.get_all_backtests(db)

@router.get("/{backtest_id}", dependencies=[Depends(JWTBearer())])
def get_backtest(backtest_id: int, db: Session = Depends(get_db)):
    result = backtests_models.Backtest.get_backtest(db, backtest_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Backtest not found")
    
    return result

@router.post("/", dependencies=[Depends(JWTBearer())])
def create_backtest( 
    algo_id: int,
    test_interval: str,
    test_start: datetime,
    test_end: datetime,
    user: users_models.Users = Depends(users_models.Users.get_auth_user),
    db: Session = Depends(get_db)
):
    algo = algos_models.Algorithm.get_algo_by_id(db=db, algo_id=algo_id, owner=user)
    if not algo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Algorithm not found")

    result = backtests_models.Backtest.create_backtest(
        db=db, 
        algo=algo, 
        owner=user.id,
        test_interval=test_interval, 
        test_start=test_start, 
        test_end=test_end)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create backtest")

    return result

@router.delete("/{backtest_id}", dependencies=[Depends(JWTBearer())])
def delete_backtest(
    backtest_id: int, 
    user: users_models.Users = Depends(users_models.Users.get_auth_user),
    db: Session = Depends(get_db)
):
    backtest = backtests_models.Backtest.get_backtest(db=db, backtest_id=backtest_id)
    if not backtest or backtest.owner != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Backtest not found")

    backtests_models.Backtest.delete_backtest(db=db, backtest_id=backtest_id, owner=user.id)
