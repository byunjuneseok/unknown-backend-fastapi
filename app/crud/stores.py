from typing import List, Optional
from sqlalchemy.orm.session import Session

from app.models.store import StoreCategory, StoreStoreCategoryMap
from .base import CRUDBase

from app.models import Store
from app.schemas.stores import StoreCreateSchema, StoreUpdateSchema


class CRUDStore(CRUDBase[Store, StoreCreateSchema, StoreUpdateSchema]):

    def get_store_categories_by_store_id(self, database: Session, *, id: str) -> List[Store]:
        store = self.get(database=database, id=id)
        if not store:
            return list()
        
        result_category_map_ids = database.query(StoreStoreCategoryMap.store_category_id).filter(
            StoreStoreCategoryMap.store_id == id
        ).all()
        
        result_category_map = (item.store_category_id for item in result_category_map_ids)
        result_category = database.query(StoreCategory).filter(
            StoreCategory.id.in_(result_category_map)
        ).all()

        return result_category


store = CRUDStore(Store)
