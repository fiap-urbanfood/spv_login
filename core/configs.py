from typing import List, ClassVar
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    
    # MySQL RDS Configuration
    DB_HOST: str = "rds-mysql.c8gkm8vsq6yc.us-east-1.rds.amazonaws.com"
    DB_NAME: str = "urbanfood"
    DB_USERNAME: str = "urbanfood"
    DB_PASSWORD: str = "Urbanf00dFiap"
    DB_PORT: int = 3306
    
    @property
    def DB_URL(self) -> str:
        return f"mysql+aiomysql://{self.DB_USERNAME}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
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
