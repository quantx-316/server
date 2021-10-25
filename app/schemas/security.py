from pydantic import BaseModel
from app.schemas.users import Users

class AuthToken(BaseModel):
    access_token: str
    user: Users 


class AuthTokenInfo(BaseModel):
    email: str
