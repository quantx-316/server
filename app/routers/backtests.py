from typing import List
from datetime import datetime 
import json
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from fastapi_pagination import Page, Params 
from fastapi_pagination.ext.sqlalchemy import paginate 

import app.models.backtests as backtests_models
import app.schemas.backtests as backtests_schemas
import app.schemas.algos as algos_schemas
import app.models.algos as algos_models
import app.models.users as users_models  
from app.utils.security import JWTBearer
from app.utils.exceptions import UserNotFoundException
from app.utils.time import datetime_to_unix
from app.db import get_db
# from app.routers.notifs import send_notification
from app.utils.sorting import sort_encapsulate_query
from app.utils.search import search_encapsulate_query
from app.utils.querying import BacktestQuery 
import app.backtest_engine.backtest as bt_engine

router = APIRouter(
    prefix="/backtest",
    dependencies=[Depends(JWTBearer())]
)

# backtests by user or by algo_id or by backtest_id
@router.get("/", dependencies=[Depends(JWTBearer())]) # Page[Backtest] or Backtest
def get_specific_backtests(
        algo_id: int = None,
        backtest_id: int = None,
        db: Session = Depends(get_db),
        user=Depends(users_models.Users.get_auth_user),
        params: Params = Depends(),
        sort_by: str = None,
        sort_direction: str = None,
        search_by: str = None, 
        search_query: str = None, 
        exclusive: bool = None, 
):
    if algo_id is not None:
        algo = algos_models.Algorithm.get_algo_by_id(db, algo_id)

        if not user.id == algo.owner and not algo.public: 
            raise HTTPException(status_code=401)

        query = backtests_models.Backtest.get_all_algo_backtests(db, algo_id)
    elif backtest_id is not None:

        backtest = backtests_models.Backtest.get_backtest_by_id(db, backtest_id)
        algo = algos_models.Algorithm.get_algo_by_id(db, backtest.algo)
        if not user.id == algo.owner and not algo.public:
            raise HTTPException(status_code=401)

        return backtest
    else:
        query = backtests_models.Backtest.get_all_user_backtests(db, user.id)

    return BacktestQuery().execute_encapsulated_query(
        query, 
        params, 
        sort_by, 
        sort_direction, 
        search_by, 
        search_query, 
        exclusive,
    )

# we don't want this endpt till we have some fine-grained private/unprivate
# @router.get("/all/", dependencies=[Depends(JWTBearer())])
# def get_all_backtests(db: Session = Depends(get_db), params: Params = Depends()):
#     """
#     Get all backtests for all users.
#     """
#     query = backtests_models.Backtest.get_all_backtests(db)
#     return paginate(query, params)

# this below is not used yet
@router.get("/pending/")
def get_pending_backtests(db: Session = Depends(get_db), user=Depends(users_models.Users.get_auth_user)):
    return backtests_models.Backtest.get_all_pending_user_backtests(db, user.id)


def mock_backtest_bg_task(backtest_id: int, owner: int, db: Session):

    from app.tests.constants import DEFAULT_FAKE_BACKTEST_ERR, DEFAULT_FAKE_BACKTEST_RESULT
    import time, random

    with open(DEFAULT_FAKE_BACKTEST_RESULT) as f:
        test_result = json.load(f)
        test_str_res = json.dumps(test_result, indent=4)

    with open(DEFAULT_FAKE_BACKTEST_ERR) as f:
        test_error = json.load(f)
        test_str_err = json.dumps(test_error, indent=4)

    backtest: backtests_schemas.Backtest = backtests_models.Backtest.get_backtest(db, backtest_id, owner)

    score = 0

    num = random.randint(0,100)
    is_err = num < 50

    new_backtest = {
        "id": backtest.id,
        "algo": backtest.algo,
        "owner": backtest.owner,
        "result": test_str_err if is_err else test_str_res,
        "score": -1 if is_err else score,
        "code_snapshot": backtest.code_snapshot,
        "test_interval": backtest.test_interval,
        "test_start": datetime_to_unix(backtest.test_start),
        "test_end": datetime_to_unix(backtest.test_end),
        "created": backtest.created,
    }

    new_backtest = backtests_schemas.Backtest(**new_backtest)

    start = end = time.time()
    while (end-start) < 20:
        end = time.time()

    backtests_models.Backtest.update_backtest(
        db,
        new_backtest,
        owner
    )


def create_backtest_bg_task(backtest_id: int, owner: int, db: Session):
    # Fetch backtest object
    backtest: backtests_schemas.Backtest = backtests_models.Backtest.get_backtest(db, backtest_id, owner)

    # Run backtest
    result = bt_engine.run_backtest(backtest, db)

    # Place result into database
    score = 0

    new_backtest = {
        "id": backtest.id,
        "algo": backtest.algo,
        "owner": backtest.owner,
        "result": result,
        "score": score,
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


@router.get("/leaderboard/", dependencies=[Depends(JWTBearer())])
def get_backtest_leaderboard(
    sort_by: str,
    sort_direction: str,
    db: Session = Depends(get_db),
    params: Params = Depends(),
    username_query: str = None,
):
    res = backtests_models.Backtest.backtest_leaderboard(
        db, params.page, params.size, sort_by, sort_direction, username_query,
    )

    return res


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

    background_task.add_task(create_backtest_bg_task, result.id, user.id, db)   # Real
    # background_task.add_task(mock_backtest_bg_task, result.id, user.id, db)   # Mock

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
