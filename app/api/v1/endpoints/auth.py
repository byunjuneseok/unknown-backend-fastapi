from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import crud
from app.core import const
from app.core.auth import encode_access_token
from app.core.config import settings
from app.dependencies.database import get_database
from app.dependencies.permission import get_current_user
from app.models import User
from app.schemas.auth import TokenResponseSchema


router = APIRouter(prefix='/auth')

@router.post('/token', response_model=TokenResponseSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_database)):
    user = crud.user.authenticate(database=database, email=form_data.username, password=form_data.password)
    
    if not user: 
        raise HTTPException(status_code=401, detail=const.USERS_ERROR_401_INVALID_USERNAME_OR_PASSWORD)

    expire_timestamp = int(datetime.now().timestamp()) + settings.JWT_EXPIRED_IN

    response = {
        'access_token': encode_access_token(id=user.id, exp=expire_timestamp, username=user.email, password=user.password),
        'expires_in': datetime.fromtimestamp(expire_timestamp).isoformat(),
        'token_type': 'bearer'
    }

    return response


@router.get('/token/test')
def test_token(current_user: User = Depends(get_current_user), database: Session = Depends(get_database)):
    return current_user
