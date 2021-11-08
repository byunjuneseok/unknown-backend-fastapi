from elasticsearch.client import Elasticsearch
from fastapi import APIRouter, Depends, Request

from app.core.config import settings
from app.dependencies.elastic import get_elasticsearch

router = APIRouter(prefix='/search')

@router.get(path='/stores/')
async def search_store(query: str, elasticsearch: Elasticsearch = Depends(get_elasticsearch)):
    
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": [
                    "name",
                    "description"
                ]
            }
        }
    }
    
    result = elasticsearch.search(index=settings.ELASTICSEARCH_STORE_SEARCH_INDEX, body=body)
    
    return result
