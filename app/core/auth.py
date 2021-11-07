from datetime import datetime

import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def encode_access_token(id: str, exp: int, username: str, password: str) -> str:
    payload = {
        'id': id,
        'exp': exp,
        'username': username,
        'password': password
    }

    encoded_jwt = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str):
    decoded_token = jwt.decode(
        jwt=token,
        key=settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM]
    )
    return decoded_token


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
