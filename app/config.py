import os 

from pydantic import BaseSettings

class Settings(BaseSettings):

    DATABASE_URI: str = 'postgresql://{}:{}@{}:{}/{}'.format(
        os.environ.get("POSTGRES_USER"),
        os.environ.get("POSTGRES_PASSWORD"),
        os.environ.get("POSTGRES_HOST"),
        os.environ.get("POSTGRES_PORT"),
        os.environ.get("POSTGRES_DB")
    )

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "afc1c5cafdeddb51fdfb6e38217f13901f3d785b8b00e60c332241c583ef303b")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_TTL: int = 120 # minutes 


settings = Settings() 