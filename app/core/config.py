from pydantic import BaseSettings, validator
from pydantic.networks import AnyUrl, RedisDsn

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

    DYNAMODB_CURATION_COLLABORATIVE_FILTERING_CACHE_TABLE_NAME: str
    DYNAMODB_CURATION_COLLABORATIVE_FILTERING_CACHE_REGION: str = 'ap-northeast-2'
    DYNAMODB_CURATION_CONTENT_BASED_FILTERING_CACHE_TABLE_NAME: str
    DYNAMODB_CURATION_CONTENT_BASED_FILTERING_CACHE_REGION: str = 'ap-northeast-2'
    
    CELERY_REDIS_PASSWORD: str
    CELERY_REDIS_HOST: str
    CELERY_REDIS_PORT: str
    CELERY_REDIS_DB_INDEX: str

    CELERY_RABBITMQ_HOST: str
    CELERY_RABBITMQ_PORT: str
    CELERY_RABBITMQ_USERNAME: str
    CELERY_RABBITMQ_PASSWORD: str


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

    @property
    def get_celery_broker_uri(self) -> str:
        return f'amqp://{self.CELERY_RABBITMQ_USERNAME}:{self.CELERY_RABBITMQ_PASSWORD}@{self.CELERY_RABBITMQ_HOST}:{self.CELERY_RABBITMQ_PORT}'

    @property
    def get_backend_uri(self) -> str:
        return f'redis://:{self.CELERY_REDIS_PASSWORD}@{self.CELERY_REDIS_HOST}:{self.CELERY_REDIS_PORT}/{self.CELERY_REDIS_DB_INDEX}'

settings = Settings()
