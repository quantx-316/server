from sqlalchemy import Column, String, Integer, Float, TIMESTAMP
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql.schema import PrimaryKeyConstraint 

from datetime import datetime

from app.db import Base 


class Quote(Base):
    __tablename__ = "quotes"

    time = Column(TIMESTAMP(timezone=True), nullable=False)
    symbol = Column(String)

    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_close = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(symbol, time),
        {},
    )

    @staticmethod
    def get_all_quotes_for_symbol(db: Session, symbol: str):
        return db.query(Quote).filter(Quote.symbol == symbol).all()

    @staticmethod 
    def get_single_quote(db: Session, symbol: str, time: datetime):
        return db.query(Quote)               \
            .filter(Quote.symbol == symbol)  \
            .filter(Quote.time == time)      \
            .first()
