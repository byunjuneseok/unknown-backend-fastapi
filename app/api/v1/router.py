from fastapi import APIRouter
from app import api


from app.api.v1.endpoints import auth, curation, search, stores, users

api_router = APIRouter(prefix='/v1')
api_router.include_router(auth.router, tags=['Auth'])
api_router.include_router(curation.router, tags=['Curation'])
api_router.include_router(search.router, tags=['Search'])
api_router.include_router(stores.router, tags=['Stores'])
api_router.include_router(users.router, tags=['Users'])
