from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Session

from app.db import Base
import app.schemas.algos as schemas
from app.models.users import Users

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
    def get_algo_by_user_id(db: Session, user_id: int):
        return 
    
    @staticmethod 
    def get_algo_by_user_email(db: Session, user_email: str):
        return 

    @staticmethod 
    def create_algo(db: Session, algo: schemas):
        pass 
    # @staticmethod
    # def create_user(db: Session, user: schemas.UserAuth):
    #     hashed_pw = hash_password(user.password)
    #     db_user = Users(email=user.email, hashed_password=hashed_pw)
    #     db.add(db_user)
    #     db.commit()
    #     db.refresh(db_user)
    #     return db_user

    # @staticmethod
    # def auth_user(db: Session, user: schemas.UserAuth):
    #     """
    #     Returns None if no authenticated user, otherwise
    #     returns the user from database 
    #     """
    #     db_user = Users.get_user_by_email(db, user.email)
    #     if not db_user:
    #         return
    #     if not password_matching(user.password, db_user.hashed_password):
    #         return
    #     return db_user
