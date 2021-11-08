from typing import final
from elasticsearch import Elasticsearch

from app.core.config import settings


def get_elasticsearch() -> Elasticsearch:
    try:
        client = Elasticsearch(hosts=settings.get_elasticsearch_url)
        yield client
    finally:
        client.close()
