from datetime import datetime
from typing import TypeVar

from pynamodb.attributes import JSONAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from app.core.config import settings


_T = TypeVar('_T', bound='CollaborativeFilteringCache')


class CollaborativeFilteringCache(Model):
    class Meta:
        table_name = settings.DYNAMODB_RECOMMANDATION_CACHE_TABLE_NAME
        region = settings.DYNAMODB_RECOMMANDATION_CACHE_TABLE_REGION
    
    user_id = NumberAttribute(hash_key=True)
    cached_time = UTCDateTimeAttribute(default=datetime.utcnow())

    value = JSONAttribute(null=True)

    def set_values(cls, user_id: str, value: dict):
        try:
            item = cls.get(user_id)
        except cls.DoesNotExist:
            item = cls(user_id=user_id)
        
        item.value = value
        item.save()
        return item
