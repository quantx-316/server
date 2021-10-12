from sqlalchemy.orm import Session
from pydantic import BaseModel


def update_db_instance(db_instance, old_model: BaseModel, new_model: BaseModel):

    diffs = []
    for var, val in vars(old_model).items():
        if getattr(new_model, var) != val:
            diffs.append((var, getattr(new_model, var)))
    
    if not diffs:
        return db_instance 
    
    for var, val in diffs:
        setattr(db_instance, var, val)
    
    return db_instance 

# also need delete user 