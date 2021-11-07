from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    url=settings.get_main_database_mysql_url,
    encoding='utf-8',
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_database() -> Generator:
    try:
        database = SessionLocal()
        yield database
    finally:
        database.close()
