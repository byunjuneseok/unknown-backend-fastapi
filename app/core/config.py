from typing import Any
from pydantic import BaseSettings, validator
from pydantic.networks import AnyUrl

from app.core import const


class Settings(BaseSettings):
    TITLE: str = 'main-backend-fastapi'

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRED_IN: int = 12 * 60 * 60  # 12hours

    MAIN_DATABASE_MYSQL_USER: str = 'system'
    MAIN_DATABSAE_MYSQL_PASSWORD: str = 'admin123'
    MAIN_DATABASE_MYSQL_HOST: str = 'localhost'
    MAIN_DATABASE_MYSQL_PORT: str = '3306'
    MAIN_DATABASE_MYSQL_DATABASE_NAME: str = 'agd'

    DYNAMODB_RECOMMANDATION_CACHE_TABLE_NAME: str
    DYNAMODB_RECOMMANDATION_CACHE_TABLE_REGION: str = 'ap-northeast-2'

    @validator('JWT_SECRET')
    def validate_jwt_secret(cls, value: str):
        if len(value) < 32:
            raise ValueError(const.CONFIG_ERROR_JWT_SECRET_LENGTH)
        return value

    @property
    def get_main_database_mysql_url(self) -> str:
        return 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
            self.MAIN_DATABASE_MYSQL_USER,
            self.MAIN_DATABSAE_MYSQL_PASSWORD,
            self.MAIN_DATABASE_MYSQL_HOST,
            self.MAIN_DATABASE_MYSQL_PORT,
            self.MAIN_DATABASE_MYSQL_DATABASE_NAME
        )


settings = Settings()
