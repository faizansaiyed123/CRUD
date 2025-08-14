from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv(), override=True)

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    PORT: int = 8000
    SERVER_TIMEOUT: int = 60

    class Config:
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()
