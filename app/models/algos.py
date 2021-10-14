from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Session

from app.db import Base
import app.schemas.algos as algos_schema 
import app.schemas.users as users_schema 
from app.models.users import Users
from app.utils.crud import add_obj_to_db


class Algorithm(Base):
    __tablename__ = "algorithm"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(Integer, ForeignKey(Users))
    title = Column(String, nullable=False)
    code = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    edited_at = Column(DateTime, nullable=False)

    @staticmethod
    def get_algo_by_id(db: Session, algo_id: int):
        return db.query(Algorithm).filter(Algorithm.id == algo_id).first()
    
    @staticmethod 
    def get_algo_by_user_email(db: Session, user_email: str):
        user_id = Users.get_user_id_from_email(user_email)
        return Algorithm.get_algo_by_user_id(user_id)

    @staticmethod 
    def get_algo_by_user_id(db: Session, user_id: int):
        return db.query(Algorithm).filter(Algorithm.owner == user_id).first() 

    @staticmethod 
    def create_algo(db: Session, algo: algos_schema.AlgoSubmit, owner: users_schema.Users):

        db_algo = Algorithm(**{
            'owner': owner.id,
            'title': algo.title, 
            'code': algo.code, 
        })
        add_obj_to_db(db, db_algo)
        return db_algo 
