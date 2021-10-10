from fastapi import Header, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_token_header(x_token: str = Header(...)):
    pass 