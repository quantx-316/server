from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session 

from app.db import Base 
import schemas.users as schemas 

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) 
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String) 

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
    def create_user(db: Session, user: schemas.UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = Users(email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

class Profile(Base):
    __tablename__ = "profile"
    
    uid = Column(Integer, ForeignKey('users.id'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    description = Column(String)