from datetime import datetime, timedelta

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from passlib.context import CryptContext
from jose import jwt

from app.config import settings
from app.utils.exceptions import AuthenticationException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def password_matching(pwd: str, hashed: str) -> bool:
    return pwd_context.verify(pwd, hashed)


def hash_password(pwd: str) -> str:
    return pwd_context.hash(pwd)


def generate_access_token(user_id: dict, expiry_time=timedelta(settings.ACCESS_TOKEN_TTL)):
    encode_data = user_id.copy()
    encode_data['exp'] = datetime.now() + expiry_time
    return jwt.encode(encode_data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_jwt(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


class JWTBearer(HTTPBearer):
    """
    To add security dependency to routes
    """
    def __init__(self):
        super().__init__(auto_error=True)

    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        if not creds:
            raise AuthenticationException("Invalid creds")
        if not creds.scheme == "Bearer":
            raise AuthenticationException("Invalid auth scheme")
        if not self.token_is_jwt(creds.credentials):
            raise AuthenticationException("Invalid token")
        return creds.credentials

    def token_is_jwt(self, token: str):
        try:
            res = decode_jwt(token)
        except:
            return False
        return True