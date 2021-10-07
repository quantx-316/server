from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, Session 

from . import models, schemas 
from .db import Base 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) 
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String) 

    @staticmethod 
    def get_user(db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    @staticmethod 
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()
    
    @staticmethod 
    def get_user_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()
    
    @staticmethod 
    def create_user(db: Session, user: schemas.UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
