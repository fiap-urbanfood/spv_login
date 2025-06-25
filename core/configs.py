from typing import List, ClassVar
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "sqlite+aiosqlite:///local.db"
    DBBaseModel: ClassVar = declarative_base()

    JWT_SECRET: str = "P7pK6xHhw04VMybl0VqeYIaGXWnJuADzQQw-pY1rwP8"
    """
    P7pK6xHhw04VMybl0VqeYIaGXWnJuADzQQw-pY1rwP8
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = "HS256"
    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
