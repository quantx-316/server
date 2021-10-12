from sqlalchemy.orm import Session
from pydantic import BaseModel


def update_db_instance(db_instance, old_model: BaseModel, new_model: BaseModel):

    diffs = []

    for key in db_instance.__table__.columns.keys():
        old_val = getattr(old_model, key, None)
        new_val = getattr(new_model, key, None)
        if old_val != new_val:
            diffs.append((key, new_val))
    
    if not diffs:
        return db_instance 

    for key, val in diffs:
        setattr(db_instance, key, val)
    
    return db_instance 

# also need delete user 