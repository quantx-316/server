from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db import Base, get_db 
import app.schemas.users as schemas
from app.utils.security import password_matching, hash_password, decode_jwt, JWTBearer
from app.utils.exceptions import AuthenticationException, UserNotFoundException, UpdateException, CreateException, BadRequestException
from app.utils.crud import update_db_instance, add_obj_to_db

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    description = Column(String)
    hashed_password = Column(String, nullable=False)

    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(Users).filter(Users.id == user_id).first()

    @staticmethod
    def get_users(db: Session):
        return db.query(Users)
    
    @staticmethod 
    def get_user_id_from_email(db: Session, email: str):
        return db.query(Users).filter(Users.email == email).first().id 
    
    @staticmethod 
    def get_user_by_username(db: Session, username: str):
        return db.query(Users).filter(Users.username == username).first() 

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(Users).filter(Users.email == email).first()

    @staticmethod
    def create_user(db: Session, user: schemas.UserRegister):
        hashed_pw = hash_password(user.password)
        user_attrs = vars(user)
        del user_attrs['password']
        db_user = Users(**user_attrs, hashed_password=hashed_pw)
        try: 
            add_obj_to_db(db, db_user)
        except: 
            raise CreateException
        return db_user
    
    @staticmethod 
    def update_user(db: Session, old_user: schemas.Users, new_user: schemas.Users):
        db_user = Users.get_user_by_email(db, old_user.email)
        if not db_user:
            raise UserNotFoundException
        try: 
            db_user = update_db_instance(db_user, old_user, new_user, ignore_keys=['hashed_password'])
            db.commit() 
        except:
            raise UpdateException
        db.refresh(db_user)
        return db_user 

    @staticmethod
    def auth_user(db: Session, user: schemas.UserLogin):
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

    @staticmethod 
    def get_auth_user(db: Session = Depends(get_db), token: str = Depends(JWTBearer())):

        auth_exception = AuthenticationException("Could not validate credentials")
        try:
            data = decode_jwt(token)
        except:
            raise auth_exception
        
        email: str = data.get("sub")
        if email is None:
            raise auth_exception
        db_user = Users.get_user_by_email(db, email)
        if db_user is None:
            raise auth_exception
        return db_user

    @staticmethod
    def query_restricted_to_limited(query):
        return query.with_entities(Users.username, Users.firstname, Users.lastname, Users.description)

    @staticmethod
    def model_to_limited_user(db_user):
        return {
            'username': db_user.username,
            'firstname': db_user.firstname,
            'lastname': db_user.lastname,
            'description': db_user.description,
        }