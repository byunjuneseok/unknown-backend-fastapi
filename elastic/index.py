# TODO: Remove this file.

from elasticsearch import Elasticsearch

client = Elasticsearch('localhost', timeout=60*1)

client.indices.create(
    index='store_search',
    body={
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "my_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer"
                        }
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {
                    "type": "text",
                },
                "name": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "description": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                }
            }
        }
    }
)