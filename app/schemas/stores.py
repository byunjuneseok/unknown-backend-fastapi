from typing import Optional

from datetime import datetime

from pydantic import BaseModel


class StoreCreateSchema(BaseModel):
    closed_on: str
    creation_date_time: datetime = datetime.utcnow()
    description: str
    location: str
    name: str
    opening_hours: str
    phone: str
    rating: float
    update_date_time: datetime = datetime.utcnow()


class StoreUpdateSchema(BaseModel):
    closed_on: Optional[str]
    description: Optional[str]
    location: Optional[str]
    name: Optional[str]
    opening_hours: Optional[str]
    phone: Optional[str]
    rating: Optional[float]
