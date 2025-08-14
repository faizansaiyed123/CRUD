
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os.path import join, dirname, abspath


env_file = join(dirname(abspath(__file__)), "..", ".env")  
load_dotenv(env_file, override=True)  


class Settings(BaseSettings):
    """
    Use this class for adding constants from .env file
    """
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PORT: int = 8000
    SERVER_TIMEOUT: int = 60
    DATABASE_URL: str



    class Config:
        env_file = env_file 
        extra = "allow"

settings = Settings()

