from typing import List
from datetime import datetime 
import json
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

import app.models.backtests as backtests_models
import app.schemas.backtests as backtests_schemas
import app.schemas.algos as algos_schemas
import app.models.algos as algos_models
import app.models.users as users_models  
from app.utils.security import JWTBearer
from app.utils.exceptions import UserNotFoundException
from app.utils.time import datetime_to_unix
from app.db import get_db

router = APIRouter(
    prefix="/backtest",
    dependencies=[Depends(JWTBearer())]
)

# backtests by user or by algo_id
@router.get("/", dependencies=[Depends(JWTBearer())])
def get_specific_backtests(algo_id: int = None, db: Session = Depends(get_db), user=Depends(users_models.Users.get_auth_user)):

    if algo_id is None: 
        return backtests_models.Backtest.get_all_user_backtests(db, user.id)
    
    return backtests_models.Backtest.get_all_algo_backtests(db, algo_id)

@router.get("/all/", dependencies=[Depends(JWTBearer())])
def get_all_backtests(db: Session = Depends(get_db)):
    """
    Get all backtests for all users.
    """
    return backtests_models.Backtest.get_all_backtests(db)

@router.get("/", dependencies=[Depends(JWTBearer())])
def get_backtest(backtest_id: int, db: Session = Depends(get_db), owner=Depends(users_models.Users.get_auth_user)):
    result = backtests_models.Backtest.get_backtest(db, backtest_id, owner.id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Backtest not found")
    
    return result

def placeholder_create_background_task(backtest_id: int, owner: int, db: Session):
    backtest = backtests_models.Backtest.get_backtest(db, backtest_id, owner)
    new_backtest = {
        "id": backtest.id,
        "algo": backtest.algo,
        "owner": backtest.owner,
        "result": json.dumps({"message": "test"}, indent=4),
        "code_snapshot": backtest.code_snapshot,
        "test_interval": backtest.test_interval,
        "test_start": datetime_to_unix(backtest.test_start),
        "test_end": datetime_to_unix(backtest.test_end),
        "created": backtest.created,
    }
    new_backtest = backtests_schemas.Backtest(**new_backtest)
    backtests_models.Backtest.update_backtest(
        db,
        new_backtest,
        owner
    ) 

@router.post("/", dependencies=[Depends(JWTBearer())])
def create_backtest( 
    submitted: backtests_schemas.BacktestSubmit,
    background_task: BackgroundTasks,
    user: users_models.Users = Depends(users_models.Users.get_auth_user),
    db: Session = Depends(get_db),
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

    background_task.add_task(placeholder_create_background_task, result.id, user.id, db)

    return result

@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_backtest(
    backtest_id: int, 
    user: users_models.Users = Depends(users_models.Users.get_auth_user),
    db: Session = Depends(get_db)
):
    backtest = backtests_models.Backtest.get_backtest(db=db, backtest_id=backtest_id, owner=user.id)
    if not backtest or backtest.owner != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Backtest not found")

    backtests_models.Backtest.delete_backtest(db=db, backtest_id=backtest_id, owner=user.id)
