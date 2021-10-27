from datetime import datetime 
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime 
from sqlalchemy.orm import Session 

from app.db import Base, db as app_db
import app.schemas.backtests as backtests_schema
import app.schemas.algos as algos_schema

class Backtest(Base):
    __tablename__ = 'backtest'

    id = Column(Integer, primary_key=True, index=True)
    algo = Column(Integer, ForeignKey("algorithm.id"))
    owner = Column(Integer, ForeignKey("user.id"))
    result = Column(String)
    code_snapshot = Column(String)
    test_interval = Column(String)
    test_start = Column(DateTime)
    test_end = Column(DateTime)
    created = Column(DateTime)

    @staticmethod
    def get_all_backtests(db: Session):
        return db.query(Backtest).all()
    
    @staticmethod 
    def get_all_user_backtests(db: Session, owner: int):
        return db.query(Backtest).filter(Backtest.owner == owner).all()

    @staticmethod
    def get_backtest(db: Session, backtest_id: int):
        return db.query(Backtest).filter(Backtest.id == backtest_id).first()
    
    @staticmethod
    def create_backtest(db: Session, algo: algos_schema.AlgoDB, owner: int, test_interval: str, test_start: datetime, test_end: datetime):
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
        return Backtest.get_backtest(db, backtest_id)

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
