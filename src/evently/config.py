from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str      # DB connection URL
    SECRET_KEY: str        # JWT secret
    ALGORITHM: str         # Token algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int  # Token expiry (minutes)

    class Config:
        env_file = ".env"  # Load from .env file

settings = Settings()