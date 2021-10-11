from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt 

from app.models.users import Users
from app.schemas.security import AuthToken
from app.schemas.users import UserAuth
from app.utils.security import generate_access_token, oauth2_scheme
from app.utils.exceptions import AuthenticationException
from app.db import get_db
from app.config import settings 

router = APIRouter() 

@router.post("/token", response_model=AuthToken)
async def get_access_token(db = Depends(get_db), form: OAuth2PasswordRequestForm = Depends()):
    user = Users.auth_user(db, UserAuth(**{"email": form.username, "password": form.password}))
    if not user: 
        raise AuthenticationException(
            "Incorrect credentials"
        )
    access_token = generate_access_token(
        {"sub": user.email} # this is JSON specification to use 'sub' for user id
    ) 
    return AuthToken(**{
        "access_token": access_token, 
        "token_type": "bearer",
    })

async def get_auth_user(db = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth_exception = AuthenticationException("Could not validate credentials")
    try: 
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except:
        raise auth_exception
    email: str = data.get("sub")
    if email is None: 
        raise auth_exception
    db_user = Users.get_user_by_email(db, email=email)
    if db_user is None: 
        raise auth_exception
    return db_user 

async def auth_user_required(db = Depends(get_db), token: str = Depends(oauth2_scheme)):
    get_auth_user(db, token)