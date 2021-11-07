from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserGenderEnum(str, Enum):
    M = 'Male'
    F = 'Female'
    B = 'b'

class UserGetSchema(BaseModel):
    email: str
    name: str
    age: int
    sex: UserGenderEnum


class UserCreateSchema(BaseModel):
    id: int
    name: str
    age: int
    sex: UserGenderEnum


class UserUpdateSchema(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
