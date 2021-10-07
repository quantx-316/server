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

settings = Settings() 