from fastapi_pagination.ext.sqlalchemy import paginate
from app.utils.search import search_encapsulate_query
from app.utils.sorting import sort_encapsulate_query

import app.models.backtests as backtests_models 
import app.models.comps as comps_models 
import app.models.algos as algos_models 

from fastapi_pagination import Params 
from fastapi import Depends

def paginate_query(
    query,
    params: Params, 
):
    return paginate(query, params)

class GenericQuery:

    def __init__(self, model):
        self.model = model 

    def execute_encapsulated_query(
        self,
        query: str, 
        params: Params = Depends(),
        *args, 
    ):
        return paginate(
            self.backtest_encapsulate_query(
                query, 
                *args, 
            ),
            params, 
        )

    def backtest_encapsulate_query(
        self,
        query: str, 
        sort_by: str = None,
        sort_direction: str = None,
        search_by: str = None, 
        search_query: str = None, 
        exclusive: bool = None, 
    ):
        return self.search_query(
                self.sort_query(
                    query, sort_by, sort_direction
                ),
                search_by,
                search_query, 
                exclusive, 
            )

    def sort_query(
        self,
        query: str, 
        *args, 
    ):
        return sort_encapsulate_query(
            *args, 
            self.model.sorting_attributes_to_col(),
            query, 
        )
    
    def search_query(
        self,
        query,
        *args,
    ):
        return search_encapsulate_query(
            *args,
            self.model.searching_attributes_to_col(),
            query,
        )

class AlgorithmQuery(GenericQuery):

    def __init__(self):
        super().__init__(algos_models.Algorithm)

class BacktestQuery(GenericQuery):

    def __init__(self):
        super().__init__(backtests_models.Backtest)

class CompetitionQuery(GenericQuery):

    def __init__(self):
        super().__init__(comps_models.Competition)

class CompetitionEntryQuery(GenericQuery):

    def __init__(self):
        super().__init__(comps_models.CompetitionEntry)
