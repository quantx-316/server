from sqlalchemy import Column, String, Integer, Float, TIMESTAMP
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql.schema import PrimaryKeyConstraint 

from datetime import datetime

from app.db import Base

from app.utils.constants import IntervalName

# Note:
#   This is implemented as a mixin, Quote_1m etc inherit from Quote.
#   I do not believe there is a cleaner way to do this other than 
#   generating and validating SQL at runtime.

class Quote_1m(Base):
    __tablename__ = 'quote_1m'

    candle = Column(TIMESTAMP(timezone=True), nullable=False)
    symbol = Column(String)

    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_close = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(symbol, candle),
        {},
    )

    @staticmethod
    def get_all_quotes_for_symbol(db: Session, symbol: str):
        return db.query(Quote_1m).filter(Quote_1m.symbol == symbol).all()

    @staticmethod 
    def get_single_quote(db: Session, symbol: str, time: datetime):
        return db.query(Quote_1m)               \
            .filter(Quote_1m.symbol == symbol)  \
            .filter(Quote_1m.candle == time)      \
            .first()


class Quote_5m(Base):
    __tablename__ = 'quote_5m'

    candle = Column(TIMESTAMP(timezone=True), nullable=False)
    symbol = Column(String)

    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_close = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(symbol, candle),
        {},
    )

    @staticmethod
    def get_all_quotes_for_symbol(db: Session, symbol: str):
        return db.query(Quote_5m).filter(Quote_5m.symbol == symbol).all()
    
    @staticmethod
    def get_single_quote(db: Session, symbol: str, time: datetime):
        return db.query(Quote_5m)               \
            .filter(Quote_5m.symbol == symbol)  \
            .filter(Quote_5m.candle == time)      \
            .first()


class Quote_15m(Base):
    __tablename__ = 'quote_15m'

    candle = Column(TIMESTAMP(timezone=True), nullable=False)
    symbol = Column(String)

    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_close = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(symbol, candle),
        {},
    )

    @staticmethod
    def get_all_quotes_for_symbol(db: Session, symbol: str):
        return db.query(Quote_15m).filter(Quote_15m.symbol == symbol).all()
    
    @staticmethod
    def get_single_quote(db: Session, symbol: str, time: datetime):
        return db.query(Quote_15m)               \
            .filter(Quote_15m.symbol == symbol)  \
            .filter(Quote_15m.candle == time)      \
            .first()


class Quote_30m(Base):
    __tablename__ = 'quote_30m'

    candle = Column(TIMESTAMP(timezone=True), nullable=False)
    symbol = Column(String)

    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_close = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(symbol, candle),
        {},
    )

    @staticmethod
    def get_all_quotes_for_symbol(db: Session, symbol: str):
        return db.query(Quote_30m).filter(Quote_30m.symbol == symbol).all()
    
    @staticmethod
    def get_single_quote(db: Session, symbol: str, time: datetime):
        return db.query(Quote_30m)               \
            .filter(Quote_30m.symbol == symbol)  \
            .filter(Quote_30m.candle == time)      \
            .first()


class Quote_1h(Base):
    __tablename__ = 'quote_1h'

    candle = Column(TIMESTAMP(timezone=True), nullable=False)
    symbol = Column(String)

    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_close = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(symbol, candle),
        {},
    )

    @staticmethod
    def get_all_quotes_for_symbol(db: Session, symbol: str):
        return db.query(Quote_1h).filter(Quote_1h.symbol == symbol).all()
    
    @staticmethod
    def get_single_quote(db: Session, symbol: str, time: datetime):
        return db.query(Quote_1h)               \
            .filter(Quote_1h.symbol == symbol)  \
            .filter(Quote_1h.candle == time)      \
            .first()


class Quote_1d(Base):
    __tablename__ = 'quote_1d'

    candle = Column(TIMESTAMP(timezone=True), nullable=False)
    symbol = Column(String)

    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_close = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(symbol, candle),
        {},
    )

    @staticmethod
    def get_all_quotes_for_symbol(db: Session, symbol: str):
        return db.query(Quote_1d).filter(Quote_1d.symbol == symbol).all()
    
    @staticmethod
    def get_single_quote(db: Session, symbol: str, time: datetime):
        return db.query(Quote_1d)               \
            .filter(Quote_1d.symbol == symbol)  \
            .filter(Quote_1d.candle == time)      \
            .first()


class Quote_1w(Base):
    __tablename__ = 'quote_1w'

    candle = Column(TIMESTAMP(timezone=True), nullable=False)
    symbol = Column(String)

    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_close = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint(symbol, candle),
        {},
    )

    @staticmethod
    def get_all_quotes_for_symbol(db: Session, symbol: str):
        return db.query(Quote_1w).filter(Quote_1w.symbol == symbol).all()
    
    @staticmethod
    def get_single_quote(db: Session, symbol: str, time: datetime):
        return db.query(Quote_1w)               \
            .filter(Quote_1w.symbol == symbol)  \
            .filter(Quote_1w.candle == time)      \
            .first()
