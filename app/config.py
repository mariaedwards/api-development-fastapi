""" Setting and type checking of env variables
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Env variables
    """
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    SECRET_KEY: str

    class Config:
        """Env variables source
        """
        env_file = ".env"


settings = Settings()
