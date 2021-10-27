from typing import Any, Optional
from pydantic import BaseModel
from datetime import datetime 

class Backtest(BaseModel):
    id: int 
    algo: int
    owner: int
    result: Optional[str]
    code_snapshot: str
    test_interval: str
    test_start: datetime
    test_end: datetime
    created: datetime
