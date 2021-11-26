from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db import Base 
from app.utils.exceptions import CreateException, UpdateException


def add_obj_to_db(db: Session, obj: Base):
    db.add(obj)
    db.commit()
    db.refresh(obj)

def update_db_instance_directly(db_instance, new_model: BaseModel, ignore_keys=[]):

    diffs = []

    ignores = set(ignore_keys)

    for key in db_instance.__table__.columns.keys():
        if key in ignores:
            continue 
        new_val = getattr(new_model, key, None)
        if new_val != getattr(db_instance, key, None):
            diffs.append((key, new_val))
        
    if not diffs:
        return db_instance

    for key, val in diffs: 
        setattr(db_instance, key, val)
    
    return db_instance 

def update_db_instance(db_instance, old_model: BaseModel, new_model: BaseModel, ignore_keys=[]):

    diffs = []

    ignores = set(ignore_keys)

    for key in db_instance.__table__.columns.keys():
        if key in ignores:
            continue 
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