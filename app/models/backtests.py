from datetime import datetime 
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime 
from sqlalchemy.orm import Session 

from app.db import Base, db as app_db
import app.schemas.backtests as backtests_schema
import app.schemas.algos as algos_schema
from app.utils.crud import update_db_instance_directly
from app.utils.exceptions import NotOwnerException, UpdateException
from app.utils.time import validate_test_intervals

class Backtest(Base):
    __tablename__ = 'backtest'

    id = Column(Integer, primary_key=True, index=True)
    algo = Column(Integer, ForeignKey("algorithm.id"))
    owner = Column(Integer, ForeignKey("users.id"))
    result = Column(String)
    code_snapshot = Column(String)
    test_interval = Column(String)
    test_start = Column(DateTime)
    test_end = Column(DateTime)
    created = Column(DateTime)

    @staticmethod
    def get_all_backtests(db: Session):
        # returns QUERY not results 
        return db.query(Backtest)
    
    @staticmethod 
    def get_all_algo_backtests(db: Session, algo_id: int):
        # returns QUERY not results 
        return db.query(Backtest).filter(Backtest.algo == algo_id)
    
    @staticmethod 
    def get_all_user_backtests(db: Session, owner: int):
        # returns QUERY not results 
        return db.query(Backtest).filter(Backtest.owner == owner)
    
    @staticmethod 
    def get_all_pending_user_backtests(db: Session, owner: int):
        return db.query(Backtest).filter(Backtest.owner == owner, Backtest.result == None).all()

    @staticmethod
    def get_backtest(db: Session, backtest_id: int, owner: int):
        backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
        if backtest and backtest.owner != owner:
            raise NotOwnerException
        return backtest 
    
    @staticmethod
    def create_backtest(db: Session, algo: algos_schema.AlgoDB, owner: int, test_interval: str, test_start: datetime, test_end: datetime):        

        validate_test_intervals(db, test_start, test_end)

        res = db.execute(app_db.validate_sqlstr(f"""
            INSERT INTO Backtest (algo, owner, code_snapshot, test_interval, test_start, test_end, created)
            VALUES (:algo, :owner, :code_snapshot, :test_interval, :test_start, :test_end, :created)
            RETURNING id
        """).bindparams(
            algo=algo.id,
            owner=owner,
            code_snapshot=algo.code,
            test_interval=test_interval,
            test_start=test_start,
            test_end=test_end,
            created=datetime.now()
        ))
        db.commit()

        backtest_id = res.first()[0]
        return Backtest.get_backtest(db, backtest_id, owner)
    
    @staticmethod 
    def update_backtest(db: Session, new_backtest: backtests_schema.Backtest, owner: int):

        db_backtest = Backtest.get_backtest(db, new_backtest.id, owner)
        if not db_backtest:
            raise Exception("Placeholder")
        
        if new_backtest.algo != db_backtest.algo:
            raise Exception("Cannot change algo it is related to")
        
        try:
            db_backtest = update_db_instance_directly(
                db_backtest, 
                new_backtest, 
                ignore_keys=['id', 'algo', 'owner', 'test_interval', 'test_start', 'test_end', 'created']
            )
            db.commit()
        except:
            raise UpdateException

        db.refresh(db_backtest)
        return db_backtest 

    @staticmethod
    def set_backtest_result(db: Session, backtest_id: int, result: str):
        db.execute(app_db.validate_sqlstr(f"""
            UPDATE Backtest
            SET result = :result
            WHERE id = :id
        """).bindparams(
            result=result,
            id=backtest_id
        ))
        db.commit()

    @staticmethod
    def delete_backtest(db: Session, backtest_id: int, owner: int):
        db.execute(app_db.validate_sqlstr(f"""
            DELETE FROM Backtest
            WHERE id = :id
        """).bindparams(
            id=backtest_id
        ))
        db.commit()
