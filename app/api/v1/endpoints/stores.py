from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.core import const
from app.dependencies.database import get_database
from app.models.store import Store, StoreCategory, StoreStoreCategoryMap
from app.schemas.stores import StoreCreateSchema, StoreUpdateSchema


router = APIRouter(prefix='/stores')


@router.get(path='/{store_id}/')
async def retrieve(store_id: UUID, database: Session = Depends(get_database)):
    store_id = str(store_id)
    store = crud.store.get(database=database, id=store_id)
    if not store:
        raise HTTPException(status_code=404, detail=const.STORES_ERROR_404)
    
    return store

@router.post(path='/')
async def create(store_create_request: StoreCreateSchema, database: Session = Depends(get_database)):
    store = crud.store.create(database=database, obj_in=store_create_request)
    return store

@router.put(path='/{store_id}/')
async def update(store_id: UUID, store_update_request: StoreUpdateSchema, database: Session = Depends(get_database)):
    store_id = str(store_id)
    store = crud.store.get(database=database, id=store_id)
    if not store:
        raise HTTPException(status_code=404, detail=const.STORES_ERROR_404)
    item = crud.store.update(database=database, db_obj=store, obj_in=store_update_request)
    return item


@router.get(path='/{store_id}/categories/')
def list_categories(store_id: UUID, database: Session = Depends(get_database)):
    store_id = str(store_id)

    categories = crud.store.get_store_categories_by_store_id(database=database, id=store_id)

    return categories
