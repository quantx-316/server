from datetime import datetime, timedelta 

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext 
from jose import jwt 

from app.config import settings 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def password_matching(pwd: str, hashed: str) -> bool:
    return pwd_context.verify(pwd, hashed)

def hash_password(pwd: str) -> str:
    return pwd_context.hash(pwd)

def generate_access_token(user_id: dict, expiry_time = timedelta(settings.ACCESS_TOKEN_TTL)):
    encode_data = user_id.copy()
    encode_data['exp'] = datetime.now() + expiry_time
    return jwt.encode(encode_data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
