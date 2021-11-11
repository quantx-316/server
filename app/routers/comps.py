from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params 
from fastapi_pagination.ext.sqlalchemy import paginate 

import app.schemas.comps as comps_schemas 
import app.models.users as users_models
import app.models.comps as comps_models 
from app.utils.security import JWTBearer
from app.utils.querying import BacktestQuery, CompetitionQuery
from app.db import get_db

router = APIRouter(
    prefix="/comps",
    dependencies=[Depends(JWTBearer())]
)

@router.post("/", response_model=comps_schemas.Competition)
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
@router.get("/finished", response_model=Page[comps_schemas.Competition])
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


@router.get("/pending", response_model=Page[comps_schemas.Competition])
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


# eligible backtests
@router.get("/{comp_id}/eligible-backtests")
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


# COMPETITION ENTRIES


