from typing import List 

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2

from app.models.security import AuthToken

router = APIRouter() 

@router.post("/token", response_model=AuthToken)
async def get_access_token(form: OAuth2PasswordRequestForm = Depends()):
    user = None 
    

    pass 