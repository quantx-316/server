from datetime import datetime, timedelta 
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import Session 

from app.db import Base, db as app_db
import app.schemas.backtests as backtests_schema
import app.schemas.algos as algos_schema
import app.schemas.comps as comps_schema
import app.schemas.users as users_schema
import app.models.backtests as backtests_models
import app.models.users as users_models 
from app.utils.crud import update_db_instance_directly
from app.utils.exceptions import NotOwnerException, UpdateException, CompNotFoundException, BadRequestException
from app.utils.time import validate_test_intervals
from app.utils.general import subquery_encapsulate


class CompetitionEntry(Base):
    __tablename__ = 'competitionentry'

    # comp_id, backtest_id is primary key 
    comp_id = Column(Integer, ForeignKey("competition.id"), primary_key=True)
    owner = Column(String, ForeignKey("users.username"), primary_key=True)

    backtest_id = Column(Integer, ForeignKey("backtest.id"))
    backtest_algo = Column(Integer, ForeignKey("algorithm.id"))

    result = Column(String)
    score = Column(Integer)
    code_snapshot = Column(String)
    test_interval = Column(String)
    test_start = Column(String)
    test_end = Column(String)

    created = Column(DateTime)

    @staticmethod 
    def get_user_comp_submission(
        db: Session, 
        comp_id: int,
        username: str, 
    ):
        return db.query(CompetitionEntry).filter(
            CompetitionEntry.owner == username, 
            CompetitionEntry.comp_id == comp_id
        ).first()

    @staticmethod 
    def get_user_entry_comps(
        db: Session, 
        username: str, 
    ): 
        # gets comp ids associated with user entries 
        return db.query(CompetitionEntry.comp_id).filter(CompetitionEntry.owner == username).distinct()
    
    @staticmethod 
    def get_comp_entries_excluding(
        db: Session, 
        comp_id: int, 
        exclude_user: str, 
    ):
        return CompetitionEntry.get_comp_entries(db, comp_id).filter(CompetitionEntry.owner != exclude_user)
    
    @staticmethod 
    def get_comp_entries(
        db: Session, 
        comp_id: int, 
    ):
        return db.query(CompetitionEntry).filter(CompetitionEntry.comp_id==comp_id)
    
    @staticmethod 
    def get_backtest_entries(
        db: Session, 
        backtest_id: int,
    ):
        return db.query(CompetitionEntry.comp_id).filter(CompetitionEntry.backtest_id==backtest_id).distinct()

    @staticmethod 
    def get_algo_entries(
        db: Session, 
        algo_id: int, 
    ):
        return db.query(CompetitionEntry.comp_id).filter(CompetitionEntry.backtest_algo==algo_id).distinct()

    @staticmethod 
    def sorting_attributes_to_col():

        return {
            "score": CompetitionEntry.score, 
            "test_start": CompetitionEntry.test_start,
            "test_end": CompetitionEntry.test_end,
            "created": CompetitionEntry.created,
        }

    @staticmethod 
    def searching_attributes_to_col():
        
        return {
            "code_snapshot": CompetitionEntry.code_snapshot, 
            "username": CompetitionEntry.owner, 
        }


class Competition(Base):
    __tablename__ = 'competition'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String) 
    description = Column(String)
    owner = Column(String, ForeignKey("users.username"))
    created = Column(DateTime)
    edited_at = Column(DateTime)
    end_time = Column(DateTime)
    test_start = Column(DateTime)
    test_end = Column(DateTime)


    # COMPETITION LIST QUERYING / SPECIFIC INFORMATION QUERYING 
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
        return db.query(Competition).filter(datetime.now() >= Competition.end_time)

    @staticmethod 
    def get_pending_comps(db: Session):
        return db.query(Competition).filter(Competition.end_time > datetime.now())

    @staticmethod 
    def get_comp_by_id(db: Session, comp_id: int, owner: users_schema.Users):
        comp = Competition.get_comp_by_id_verified(db, comp_id)
        
        if owner is None: 
            return comp 

        if comp.owner != owner.username: 
            raise NotOwnerException

        return comp 
    

    # COMPETITIONS CREATED BY A CERTAIN USER 
    @staticmethod 
    def get_comps_by_owner_username(db: Session, username: str):
        # competitions a given user (username) has created
        return db.query(Competition).filter(Competition.owner == username)
    


    # COMPETITIONS SUBMITTED TO BY A CERTAIN USER 
    @staticmethod 
    def get_comp_submitted_by_username(db: Session, username: str):
        # competitions user (username) has submitted to 
        subquery = subquery_encapsulate(CompetitionEntry.get_user_entry_comps(db, username))

        # query for competitions user has submitted to: 
        query = db.query(Competition).filter(Competition.id.in_(subquery))

        return query 



    # USERS WHO SUBMITTED TO A CERTAIN COMPETITION 

    # users who have submitted to a competition, also competitionentry has submitted time 

    @staticmethod 
    def get_comp_exclusive_submitted_users(
        db: Session, 
        comp_id: int, 
        exclude_username: str, 
    ): 
        return CompetitionEntry.get_comp_entries_excluding(db, comp_id, exclude_username)

    @staticmethod 
    def get_comp_submitted_users(
        db: Session, 
        comp_id: int
    ): 
        # users who have submitted to a competition   
        query = CompetitionEntry.get_comp_entries(db, comp_id)
        return query 
    
    # user's submission to a competition
    @staticmethod 
    def get_user_comp_submission(
        db: Session, 
        comp_id: int, 
        username: str, 
    ):
        query = CompetitionEntry.get_user_comp_submission(
            db,
            comp_id, 
            username, 
        )
        return query 

    # ETC...

    # competitions that algorithm has been submitted to 
    @staticmethod 
    def get_comp_submitted_algo(
        db: Session, 
        algo_id: int,
    ):
        subquery = subquery_encapsulate(CompetitionEntry.get_algo_entries(db, algo_id))
        query = db.query(Competition).filter(Competition.id.in_(subquery))
        return query 

    # competitions that backtest has been submitted to 
    @staticmethod 
    def get_comp_submitted_backtest(
        db: Session, 
        backtest_id: int, 
    ):
        subquery = subquery_encapsulate(CompetitionEntry.get_backtest_entries(db, backtest_id))
        query = db.query(Competition).filter(Competition.id.in_(subquery))
        return query 

    @staticmethod 
    def create_competition(db: Session, comp: comps_schema.CompetitionSubmit, owner: users_schema.Users):

        if comp.end_time < (datetime.now() + timedelta(days=7)):
            raise BadRequestException("End time must be greater than a week from today")
        
        validate_test_intervals(db, comp.test_start, comp.test_end)
        
        res = db.execute(app_db.validate_sqlstr("""
        INSERT INTO COMPETITION (owner, title, description, end_time, test_start, test_end)
        VALUES (:username, :title, :desc, :end_time, :test_start, :test_end)
        RETURNING id 
        """).bindparams(
                username=owner.username, title=comp.title, desc=comp.description,
                end_time=comp.end_time, test_start=comp.test_start, test_end=comp.test_end,
            )   
        )
        db.commit() 
        comp_id = res.first()[0]
        return Competition.get_comp_by_id(db, comp_id, owner)


    # ELIGIBLE BACKTESTS FOR THE USER REQUESTING 
    @staticmethod 
    def get_eligible_backtests(
        db: Session, 
        comp_id: int, 
        owner: users_schema.Users, 
    ):
        comp = Competition.get_comp_by_id_verified(db, comp_id)
        if comp.end_time <= datetime.now():
            raise BadRequestException("Competition is finished")
        
        if comp.owner == owner.username: 
            raise BadRequestException("No eligible backtests for owner of competition")

        query = db.query(backtests_models.Backtest).filter(
            backtests_models.Backtest.owner == owner.id, 
            backtests_models.Backtest.test_end <= comp.test_end, 
            backtests_models.Backtest.test_start >= comp.test_start, 
            backtests_models.Backtest.created >= comp.created, 
            backtests_models.Backtest.score >= 0,
        )

        return query 


    @staticmethod 
    def submit_backtest(db: Session, comp_id: int, backtest_id: int, owner: users_schema.Users):
        
        comp = Competition.get_comp_by_id_verified(db, comp_id)

        # is comp even still going
        if comp.end_time <= datetime.now():
            raise BadRequestException("Competition is finished")

        # owner cant submit to his own competition
        if owner.username == comp.owner:
            raise BadRequestException("Owner can't submit to own competition")

        # verify owner is owner of backtest and get up to date backtest info
        db_backtest = backtests_models.Backtest.get_backtest(db, backtest_id, owner.id)

        # check start, end ranges 
        if db_backtest.test_start < comp.test_start or db_backtest.test_end > comp.test_end: 
            raise BadRequestException("Test start, test end ranges not valid")
        
        # check created date 
        if db_backtest.created < comp.created: 
            raise BadRequestException("Backtest created before competition")
        
        # check backtest succeeded // not in progress
        if not db_backtest.result or db_backtest.score < 0: # SCORE < 0 TO INDICATE FATAL ERROR 
            raise BadRequestException("Backtest did not succeed or did not finish yet")

        # backtest can be submitted
            # if already existing entry for (comp_id, uid), remove and then allow insertion
        res = db.execute(app_db.validate_sqlstr("""
            SELECT * FROM CompetitionEntry WHERE
            comp_id = :comp_id AND owner = :username
        """).bindparams(
            comp_id=comp.id, 
            username=owner.username,
        ))
        rows = [row for row in res]
        if len(rows) > 0:

            first = rows[0]
            if first.backtest_id == db_backtest.id: 
                raise BadRequestException("This backtest is already your submission")

            db.execute(app_db.validate_sqlstr("""
            DELETE FROM CompetitionEntry WHERE 
            comp_id = :comp_id AND owner = :username
            """).bindparams(
                comp_id=comp.id,
                username=owner.username, 
            )) # this will commit with the insertion if both are successful

        # insert new 
        db.execute(app_db.validate_sqlstr("""
        INSERT INTO CompetitionEntry (comp_id, owner, backtest_id, backtest_algo, result, score, code_snapshot, test_interval, test_start, test_end)
        VALUES (:comp_id, :username, :back_id, :back_algo, :result, :score, :code, :test_int, :test_start, :test_end)
        """).bindparams(
            comp_id=comp.id, 
            username=owner.username, 
            back_id=db_backtest.id,
            back_algo=db_backtest.algo,
            result=db_backtest.result, 
            score=db_backtest.score, 
            code=db_backtest.code_snapshot, 
            test_int=db_backtest.test_interval, 
            test_start=db_backtest.test_start,
            test_end=db_backtest.test_end,
        ))
        db.commit()

        return Competition.get_user_comp_submission(
            db, 
            comp.id, 
            owner.username, 
        )

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
