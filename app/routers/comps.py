from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params 
from fastapi_pagination.ext.sqlalchemy import paginate 

import app.schemas.comps as comps_schemas 
import app.schemas.backtests as back_schemas 
import app.models.users as users_models
import app.models.comps as comps_models 
from app.utils.exceptions import BadRequestException
from app.utils.security import JWTBearer
from app.utils.querying import BacktestQuery, CompetitionQuery
from app.db import get_db

router = APIRouter(
    prefix="/comps",
    dependencies=[Depends(JWTBearer())]
)

@router.post("/")
def create_competition(
    comp: comps_schemas.CompetitionSubmit,
    user = Depends(users_models.Users.get_auth_user),
    db: Session = Depends(get_db),
): 
    return comps_models.Competition.create_competition(db, comp, user)

@router.put("/", response_model=comps_schemas.Competition)
def update_competition(
    new_comp: comps_schemas.Competition, 
    user = Depends(users_models.Users.get_auth_user),
    db: Session = Depends(get_db),
):
    return comps_models.Competition.update_competition(db, new_comp, user)

@router.delete("/")
def delete_competition(
    comp_id: int, 
    user = Depends(users_models.Users.get_auth_user),
    db: Session = Depends(get_db)
):
    return comps_models.Competition.delete_competition(db, comp_id, user)

# GET COMPETITIONS 
@router.get("/finished/", response_model=Page[comps_schemas.Competition])
def get_finished_competitions(
    db: Session = Depends(get_db),
    params: Params = Depends(),
    sort_by: str = None,
    sort_direction: str = None,
    search_by: str = None, 
    search_query: str = None, 
    exclusive: bool = None
):
    query = comps_models.Competition.get_finished_comps(db)

    return CompetitionQuery().execute_encapsulated_query(
        query, params, sort_by, sort_direction, 
        search_by, search_query, 
        exclusive, 
    )


@router.get("/pending/", response_model=Page[comps_schemas.Competition])
def get_pending_competitions(
    db: Session = Depends(get_db),
    params: Params = Depends(),
    sort_by: str = None,
    sort_direction: str = None,
    search_by: str = None, 
    search_query: str = None, 
    exclusive: bool = None
):
    query = comps_models.Competition.get_pending_comps(db)

    return CompetitionQuery().execute_encapsulated_query(
        query, params, sort_by, sort_direction, 
        search_by, search_query, 
        exclusive, 
    )


# get competitions user submitted to, algo was submitted to, backtest was submitted to 
@router.get("/submitted/")
def get_comps_submitted_to_by_user(
    username: str = None, 
    algo_id: int = None, 
    backtest_id: int = None,
    params: Params = Depends(),
    sort_by: str = None,
    sort_direction: str = None,
    search_by: str = None,
    search_query: str = None,
    exclusive: bool = None,
    db: Session = Depends(get_db),
):

    if algo_id is None and backtest_id is None and username is None:
        raise BadRequestException("at least one query parameter required")

    query = None

    if algo_id is not None:
        query = comps_models.Competition.get_comp_submitted_algo(
            db, algo_id
        )
    if backtest_id is not None: 
        query = comps_models.Competition.get_comp_submitted_backtest(
            db, backtest_id
        )
    if username is not None: 
        query = comps_models.Competition.get_comp_submitted_by_username(
            db, 
            username, 
        )

    return CompetitionQuery().execute_encapsulated_query(
        query, params, sort_by, sort_direction,
        search_by, search_query,
        exclusive,
    )

# get competitions owned by user 
@router.get("/owned/")
def get_comps_owned_by_user(
    username: str,
    params: Params = Depends(),
    sort_by: str = None,
    sort_direction: str = None,
    search_by: str = None,
    search_query: str = None,
    exclusive: bool = None,
    db: Session = Depends(get_db),
):
    query = comps_models.Competition.get_comps_by_owner_username(
        db, 
        username, 
    )
    
    return CompetitionQuery().execute_encapsulated_query(
        query, params, sort_by, sort_direction,
        search_by, search_query,
        exclusive,
    )



# eligible backtests
@router.get("/{comp_id}/eligible-backtests/", response_model=Page[back_schemas.Backtest])
def get_eligible_backtests(
    comp_id: int, 
    db: Session = Depends(get_db),
    user = Depends(users_models.Users.get_auth_user),
    params: Params = Depends(),
    sort_by: str = None,
    sort_direction: str = None,
    search_by: str = None, 
    search_query: str = None, 
    exclusive: bool = None
):
    query = comps_models.Competition.get_eligible_backtests(
        db,
        comp_id, 
        user, 
    )

    return BacktestQuery().execute_encapsulated_query(
        query, params, sort_by, sort_direction, 
        search_by, search_query, exclusive, 
    )

# get all user entries to a competition
@router.get("/{comp_id}/entries/")
def get_comp_entries(
    comp_id: int, 
    db: Session = Depends(get_db),
):  
    return comps_models.Competition.get_comp_submitted_users(
        db, comp_id, 
    )

# get user's entry to a competition
@router.get("/{comp_id}/entry/")
def get_comp_entry_for_user(
    comp_id: int, 
    username: str, 
    db: Session = Depends(get_db),
):
    return comps_models.Competition.get_user_comp_submission(
        db, comp_id, username,
    )

# get specific competition
@router.get("/{comp_id}/", response_model=comps_schemas.Competition)
def get_competition(
    comp_id: int, 
    db: Session = Depends(get_db),
):
    return comps_models.Competition.get_comp_by_id_verified(
        db, comp_id, 
    )

# COMPETITION ENTRIES

# create entry 
@router.post("/{comp_id}/")
def submit_backtest(
    comp_id: int, 
    backtest_id: int, 
    db: Session = Depends(get_db),
    user = Depends(users_models.Users.get_auth_user),
):
    return comps_models.Competition.submit_backtest(
        db, 
        comp_id, 
        backtest_id, 
        user, 
    )
