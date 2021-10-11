from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2

from app.models.users import Users
from app.schemas.security import AuthToken
from app.schemas.users import UserAuth
from app.utils.security import generate_access_token
from app.db import get_db

router = APIRouter() 

@router.post("/token", response_model=AuthToken)
async def get_access_token(db = Depends(get_db), form: OAuth2PasswordRequestForm = Depends()):
    user = Users.auth_user(db, UserAuth({"username": form.username, "password": form.password}))
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = generate_access_token(user) 
    return AuthToken({
        "access_token": access_token, 
        "token_type": "bearer",
    })