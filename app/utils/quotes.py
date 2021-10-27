from app.db import get_db, db as app_db 
from sqlalchemy.orm import Session
from app.utils.exceptions import FailedRetrievalException

def get_min_max_times(db: Session):
    res = db.execute(app_db.validate_sqlstr("""
        SELECT MIN(time), MAX(time) FROM Quote
    """))
    rows = [row for row in res]

    if not rows:
        raise FailedRetrievalException

    min_, max_ = rows[0]
    return (min_, max_)
