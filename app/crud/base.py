from typing import Any, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    def get(self, database: Session, id: Any) -> Optional[ModelType]:
        return database.query(self.model).filter(self.model.id == id).first()

    def list(self, database: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return database.query(self.model).offset(skip).limit(limit).all()

    def create(self, database: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        database_obj = self.model(**obj_in_data)
        database.add(database_obj)
        database.commit()
        database.refresh(database_obj)
        return database_obj

    def update(self, database: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        database.add(db_obj)
        database.commit()
        database.refresh(db_obj)
        return db_obj
