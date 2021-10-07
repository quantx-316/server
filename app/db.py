from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

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
        """Execute sqlstr and return a list of result tuples.  sqlstr will be
        wrapped automatically in a
        sqlalchemy.sql.expression.TextClause.  You can use :param
        inside sqlstr and supply its value as a kwarg.  See
        https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.execute
        https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text
        https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.CursorResult
        for additional details.  See models/*.py for examples of
        calling this function."""
        with self.engine.connect() as conn:
            return list(conn.execute(text(sqlstr), kwargs).fetchall())

Base = declarative_base()