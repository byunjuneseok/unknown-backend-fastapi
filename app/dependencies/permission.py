from typing import Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session

from app import crud
from app.core import config, const
from app.core.auth import decode_access_token
from app.models import User

from .database import get_database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/token')

def get_current_user(token: str = Depends(oauth2_scheme), database: Session = Depends(get_database)) -> User:
    try:
        payload = decode_access_token(token=token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail=const.USERS_ERROR_401_TIMESTAMP_HAS_EXPIRED)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail=const.USERS_ERROR_401_INVALID_TOKEN)

    if 'id' not in payload:
        raise HTTPException(status_code=401, detail=const.USERS_ERROR_401_INVALID_TOKEN)

    user = crud.user.get(database=database, id=payload.get('id'))

    return user
