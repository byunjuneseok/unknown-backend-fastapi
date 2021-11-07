from sqlalchemy import Column, String, Integer, BigInteger

from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    age = Column(Integer)
    sex = Column(String)
