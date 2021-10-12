from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session

from app.db import Base
import app.schemas.users as schemas
from app.utils.security import password_matching, hash_password


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    description = Column(String)
    hashed_password = Column(String, nullable=False)

    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(Users).filter(Users.id == user_id).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Users).offset(skip).limit(limit).all()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(Users).filter(Users.email == email).first()

    @staticmethod
    def create_user(db: Session, user: schemas.UserAuth):
        hashed_pw = hash_password(user.password)
        db_user = Users(email=user.email, hashed_password=hashed_pw)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def auth_user(db: Session, user: schemas.UserAuth):
        """
        Returns None if no authenticated user, otherwise
        returns the user from database 
        """
        db_user = Users.get_user_by_email(db, user.email)
        if not db_user:
            return
        if not password_matching(user.password, db_user.hashed_password):
            return
        return db_user
