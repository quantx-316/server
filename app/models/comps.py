from datetime import datetime 
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import Session 

from app.db import Base, db as app_db
import app.schemas.backtests as backtests_schema
import app.schemas.algos as algos_schema
import app.schemas.comps as comps_schema
import app.schemas.users as users_schema
import app.models.backtests as backtests_models
from app.utils.crud import update_db_instance_directly
from app.utils.exceptions import NotOwnerException, UpdateException, CompNotFoundException, BadRequestException
from app.utils.time import validate_test_intervals

class CompetitionEntry(Base):
    __tablename__ = 'competitionentry'

    # comp_id, backtest_id is primary key 
    comp_id = Column(Integer, ForeignKey("competition.id"))
    backtest_id = Column(Integer, ForeignKey("backtest.id"))
    uid = Column(Integer, ForeignKey("users.id"))

class Competition(Base):
    __tablename__ = 'competition'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String) 
    description = Column(String)
    owner = Column(Integer, ForeignKey("users.id"))
    created = Column(DateTime)
    edited_at = Column(DateTime)
    end_time = Column(DateTime)
    test_start = Column(DateTime)
    test_end = Column(DateTime)

    @staticmethod 
    def get_comp_by_id_verified(db: Session, comp_id: int):
        comp = db.query(Competition).filter(Competition.id == comp_id).first()

        if not comp: 
            raise CompNotFoundException
        
        return comp 
    
    @staticmethod 
    def get_comps(db: Session):
        return db.query(Competition)    
     
    @staticmethod 
    def get_finished_comps(db: Session):
        return db.query(Competition).filter(Competition.end_time >= datetime.now())

    @staticmethod 
    def get_pending_comps(db: Session):
        return db.query(Competition).filter(Competition.created < datetime.now())

    @staticmethod 
    def get_comp_by_id(db: Session, comp_id: int, owner: users_schema.Users):
        comp = Competition.get_comp_by_id_verified(db, comp_id)
        
        if owner is None: 
            return comp 

        if comp.owner != owner.id: 
            raise NotOwnerException

        return comp 
    
    @staticmethod 
    def get_comps_by_owner(db: Session, owner: users_schema.Users): # competitions current user has created 
        return db.query(Competition).filter(Competition.owner == owner.id)

    # competitions current user has submitted to 
    @staticmethod 
    def get_comps_by_user(db: Session, owner: users_schema.Users):
        return Competition.get_comp_by_user_id(db, owner.id)
    
    @staticmethod # competitions another user has submitted to 
    def get_comp_by_user_id(db: Session, user_id):

        query = app_db.validate_sqlstr("""

        """)

        return db.query(CompetitionEntry.comp_id).filter(Competition.uid == user_id).distinct() 

    # users who have submitted to a competition
    

    # best user backtest for a competition (other user), can be reused for public profile comps. user has submitted to


    # user submissions to a competition (owner) 


    # backtests submitted to competition (will be sorted by endpt to get best) 


# CompetitionEntry 
    # comp_id int references Competition(id)
    # backtest_id int references Backtest(id)
    # uid INT References Users(id) 
    # submitted timestamp not null
    # primary key(comp_id, backtest_id)


    @staticmethod 
    def create_competition(db: Session, comp: comps_schema.Competition, owner: users_schema.Users):
        
        res = db.execute(app_db.validate_sqlstr("""
        INSERT INTO COMPETITION (owner, title, description, end_time, test_start, test_end)
        VALUES (:_id, :title, :desc, :end_time, :test_start, :test_end)
        RETURNING id 
        """).bindparams(
                _id=owner.id, title=comp.title, desc=comp.description,
                end_time=comp.end_time, test_start=comp.test_start, test_end=comp.test_end,
            )   
        )
        db.commit() 
        comp_id = res.first()[0]
        return Competition.get_comp_by_id(db, comp_id, owner)

    @staticmethod 
    def submit_backtest(db: Session, comp: comps_schema.Competition, backtest: backtests_schema.Backtest, owner: users_schema.Users):
        
        # is comp even still going
        if comp.end_time <= datetime.now():
            raise BadRequestException("Competition is finished")

        # verify owner is owner of backtest and get up to date backtest info
        db_backtest = backtests_models.Backtest.get_backtest(db, backtest.id, owner.id)

        # check start, end ranges 
        if db_backtest.test_start < comp.test_start or db_backtest.test_end > comp.test_end: 
            raise BadRequestException("Test start, test end ranges not valid")
        
        # check created date 
        if db_backtest.created < comp.created: 
            raise BadRequestException("Backtest created before competition")
        
        # check backtest succeeded // not in progress
        if not db_backtest.result or db_backtest.score < 0: # USE SCORE < 0 TO INDICATE ERROR 
            raise BadRequestException("Backtest did not succeed or did not finish yet")

        db.execute(app_db.validate_sqlstr("""
        INSERT INTO CompetitionEntry (comp_id, backtest_id)
        VALUES (:comp_id, :back_id)
        """).bindparams(
            comp_id=comp.id, back_id=db_backtest.id
        ))
        db.commit()

    @staticmethod 
    def update_competition(db: Session, new_comp: comps_schema.Competition, owner: users_schema.Users):
        
        db_comp = Competition.get_comp_by_id(db, new_comp.id, owner)
        
        try: 
            db_comp = update_db_instance_directly(db_comp, new_comp, ignore_keys=['id', 'owner', 'created', 'edited_at', 'end_time', 'test_start', 'test_end'])
            db.commit()
        except: 
            raise UpdateException
        
        db.refresh(db_comp)
        return db_comp 
    
    @staticmethod 
    def delete_competition(db: Session, comp_id: int, owner: users_schema.Users):
        
        db_comp = Competition.get_comp_by_id(db, comp_id, owner)
        db.delete(db_comp)
        db.commit()
    
    @staticmethod 
    def sorting_attributes_to_col():

        return {
            "created": Competition.created, 
            "edited_at": Competition.edited_at,
            "end_time": Competition.end_time,
            "test_start": Competition.test_start,
            "test_end": Competition.test_end,
        }

    @staticmethod 
    def searching_attributes_to_col():
        
        return {
            "title": Competition.title, 
            "description": Competition.description,
        }
