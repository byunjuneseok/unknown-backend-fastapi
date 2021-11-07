from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app import crud

from app.dependencies.database import get_database
from app.dependencies.permission import get_current_user
from app.models.user import User
from app.schemas.users import UserGetSchema


router = APIRouter(prefix='/users')

@router.get(path='/')
async def get_user(request: Request):
    
    return {'hello': 'world'}


@router.get(path='/me')
async def get_user_me(current_user: User = Depends(get_current_user)):
    
    return UserGetSchema(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        age=current_user.age,
        sex=current_user.sex
    )
