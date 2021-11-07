from datetime import datetime
from typing import TypeVar

from pynamodb.attributes import JSONAttribute, NumberAttribute, UTCDateTimeAttribute, UnicodeAttribute
from pynamodb.models import Model

from app.core.config import settings


_T = TypeVar('_T', bound='CollaborativeFilteringCache')


class CollaborativeFilteringCache(Model):
    class Meta:
        table_name = settings.DYNAMODB_CURATION_COLLABORATIVE_FILTERING_CACHE_TABLE_NAME
        region = settings.DYNAMODB_CURATION_COLLABORATIVE_FILTERING_CACHE_REGION
    
    user_id = NumberAttribute(hash_key=True)
    cached_time = UTCDateTimeAttribute(default=datetime.utcnow())

    value = JSONAttribute(null=True)


class ContentBasedFilteringCache(Model):
    class Meta:
        table_name = settings.DYNAMODB_CURATION_CONTENT_BASED_FILTERING_CACHE_TABLE_NAME
        region = settings.DYNAMODB_CURATION_CONTENT_BASED_FILTERING_CACHE_REGION

    store_id = UnicodeAttribute(hash_key=True)
    cached_time = UTCDateTimeAttribute(default=datetime.utcnow())

    value = JSONAttribute(null=True)
