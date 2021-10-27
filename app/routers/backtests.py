from typing import List
from datetime import datetime 

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
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

def placeholder_create_background_task(backtest_id: int):
    pass 

@router.post("/", dependencies=[Depends(JWTBearer())])
def create_backtest( 
    submitted: backtests_schemas.BacktestSubmit,
    user: users_models.Users = Depends(users_models.Users.get_auth_user),
    db: Session = Depends(get_db),
    background_task = BackgroundTasks 
):
    algo = algos_models.Algorithm.get_algo_by_id(db=db, algo_id=submitted.algo, owner=user)
    if not algo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Algorithm not found")

    result = backtests_models.Backtest.create_backtest(
        db=db, 
        algo=algo, 
        owner=user.id,
        test_interval=submitted.test_interval, 
        test_start=submitted.test_start, 
        test_end=submitted.test_end)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create backtest")

    background_task.add_task(placeholder_create_background_task, result.id)

    return result

@router.put("/", dependencies=[Depends(JWTBearer())])
def update_backtest(
    new_backtest: backtests_schemas.Backtest, 
    user = Depends(users_models.Users.get_auth_user),
    db: Session = Depends(get_db)
):

    if new_backtest.owner != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You must be owner")

    return backtests_models.Backtest.update_backtest(db, new_backtest, user.id)    

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
