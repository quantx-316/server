from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.users import Users
from app.schemas.security import AuthToken
from app.schemas.users import UserAuth
from app.utils.security import generate_access_token
from app.utils.exceptions import AuthenticationException
from app.db import get_db

router = APIRouter()


@router.post("/token", response_model=AuthToken)
async def get_access_token(db=Depends(get_db), form: OAuth2PasswordRequestForm = Depends()):
    user = Users.auth_user(db, UserAuth(**{"email": form.username, "password": form.password}))
    if not user:
        raise AuthenticationException(
            "Incorrect credentials"
        )
    access_token = generate_access_token(
        {"sub": user.email}  # this is JSON specification to use 'sub' for user id
    )
    return AuthToken(**{
        "access_token": access_token,
        "token_type": "bearer",
    })
