from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from app.config import settings 

class DB:
    """Hosts all functions for querying the database."""
    def __init__(self, settings):
        self.engine = create_engine(settings.DATABASE_URI)
        self.session = None 

    def connect(self):
        return self.engine.connect()
    
    def get_singleton_session(self):
        if self.session is None:
            self.session = self.get_session()
        return self.session

    def get_session(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)()

    def execute(self, sqlstr, **kwargs):
        """Execute sqlstr and return"""

        with self.engine.connect() as conn:
            return conn.execute(self.validate_sqlstr(sqlstr))
            # return list(conn.execute(text(sqlstr), kwargs).fetchall())

    def validate_sqlstr(self, sqlstr):
        return text(sqlstr)

Base = declarative_base()

db = DB(settings)

def get_db():
    session = db.get_session()
    try: 
        yield session
    finally:
        session.close()