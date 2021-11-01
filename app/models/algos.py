from pydantic.errors import NotNoneError
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import TextClause 

from app.db import Base, db as app_db
import app.schemas.algos as algos_schema 
import app.schemas.users as users_schema 
from app.models.users import Users
from app.models.backtests import Backtest
from app.utils.crud import add_obj_to_db, update_db_instance, update_db_instance_directly
from app.utils.exceptions import NotOwnerException, AlgoNotFoundException, UpdateException
from app.models.backtests import BestAlgoBacktest


class Algorithm(Base):
    __tablename__ = "algorithm"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    code = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    edited_at = Column(DateTime, nullable=False)
    public = Column(Boolean, nullable=False)

    @staticmethod
    def get_algo_by_id(db: Session, algo_id: int, owner: users_schema.Users):
        algo = db.query(Algorithm).filter(Algorithm.id == algo_id).first()

        if not algo: 
            raise AlgoNotFoundException

        if algo.owner != owner.id: 
            raise NotOwnerException
        
        return algo 
    
    @staticmethod 
    def get_algo_by_user_email(db: Session, user_email: str, owner: users_schema.Users):
        user = Users.get_user_by_email(user_email)
        return Algorithm.get_algo_by_user(db, user)

    @staticmethod 
    def get_algo_by_user(db: Session, owner: users_schema.Users):
        # returns QUERY to you, not the results 
        return db.query(Algorithm).filter(Algorithm.owner == owner.id)

    @staticmethod 
    def create_algo(db: Session, algo: algos_schema.AlgoSubmit, owner: users_schema.Users):

        # db_algo = Algorithm(**{
        #     'owner': owner.id,
        #     'title': algo.title, 
        #     'code': algo.code, 
        # })

        res = db.execute(app_db.validate_sqlstr(f"""
        INSERT INTO ALGORITHM (owner, title, code)
        VALUES (:_id, :title, :code)
        RETURNING id
        """).bindparams(
                _id=owner.id, title=algo.title, code=algo.code
            )
        )
        db.commit() 
        algo_id = res.first()[0]
        return Algorithm.get_algo_by_id(db, algo_id, owner)

    @staticmethod 
    def update_algo(db: Session, new_algo: algos_schema.AlgoDB, owner: users_schema.Users):

        db_algo = Algorithm.get_algo_by_id(db, new_algo.id, owner)
        if not db_algo: 
            raise AlgoNotFoundException
        
        try: 
            db_algo = update_db_instance_directly(db_algo, new_algo, ignore_keys=['id'])
            db.commit()
        except:
            raise UpdateException

        db.refresh(db_algo)
        return db_algo

    @staticmethod
    def best_public_algo_backtests(
            db: Session,
            username: str,
            page: int,
            size: int,
            sort_by: str,
            sort_direction: str,
    ):
        # TODO: same as leaderboard in models/backtests.py need better exception handling
        if page < 1 or size < 0:
            raise Exception("Invalid params")

        if sort_by not in Backtest.sorting_attributes_to_col():
            raise Exception("Invalid sort_by attr")

        if sort_direction not in ['asc', 'desc']:
            raise Exception("Invalid sort direction")

        limit = size
        offset = size * (page - 1)

        user = Users.get_user_by_username(db, username)

        if not user:
            raise Exception("No user")

        sort_by = f"back.{sort_by}"
        sort_direction = sort_direction.upper()

        ordering = f" ORDER BY {sort_by} {sort_direction} "

        query = app_db.validate_sqlstr(f"""
                SELECT * FROM Backtest AS back JOIN 
                (SELECT backtest_id AS id 
                FROM BestAlgoBacktest AS best JOIN Algorithm AS algo 
                ON best.algo_id = algo.id WHERE algo.owner = :user_id AND algo.public = True) 
                AS backtest_ids 
                ON backtest_ids.id = back.id 
                """ + ordering + " LIMIT :limit OFFSET :offset ").bindparams(
            user_id=user.id, limit=limit, offset=offset,
        )

        count_query = app_db.validate_sqlstr(f"""
                SELECT COUNT(*) FROM Backtest AS back JOIN 
                (SELECT backtest_id AS id 
                FROM BestAlgoBacktest AS best JOIN Algorithm AS algo 
                ON best.algo_id = algo.id WHERE algo.owner = :user_id AND algo.public = True) 
                AS backtest_ids 
                ON backtest_ids.id = back.id 
                """).bindparams(
            user_id=user.id
        )

        res = db.execute(query)
        count_res = db.execute(count_query).first()[0]

        return {
            'items': [row for row in res],
            'pagination': {
                'page': page,
                'size': size,
                'total': count_res,
            }
        }
    
    @staticmethod 
    def delete_algo(db: Session, algo_id: int, owner: users_schema.Users):

        db_algo = Algorithm.get_algo_by_id(db, algo_id, owner)
        db.delete(db_algo)
        db.commit()

    @staticmethod
    def sorting_attributes_to_col():

        return {
            "created": Algorithm.created,
            "edited_at": Algorithm.edited_at,
            "title": Algorithm.title,
        }
