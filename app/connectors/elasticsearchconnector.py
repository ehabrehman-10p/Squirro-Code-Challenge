import os
from config import config
from fastapi import HTTPException,status
from elasticsearch import Elasticsearch

es = Elasticsearch(config.ES_URL)
index = config.ES_INDEX
def index_document(document_content: str) -> dict:
    if document_content.strip():
        query = {"query": {"match_phrase": {"content": document_content}}}
        try:
            existing_docs = es.search(index=index, body=query)
            if existing_docs['hits']['total']['value'] > 0:
                return {"detail": "This document already exists", "document_id": existing_docs['hits']['hits'][0]['_id']}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        doc = {"content": document_content}
        try:
            res = es.index(index=index, body=doc)
            if res:
                return {"document_id": res['_id']}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='bad request')

def search_documents(query: str, k: int):
    status_code =''
    error_message =''
    if (k<1):
        error_message = "K cannot be less than or equal to 0"
        status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=error_message)
    try:
        res = es.search(index=index, body={ "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "content": query
                        }
                    },
                    {
                        "match": {
                            "content": {
                                "query": query,
                                "fuzziness": "2"
                            }
                        }
                    }
                ],
                "minimum_should_match": 1  # At least one of the conditions must match
            }
        },"size": k,"sort": [{"_score": {"order": "desc"}}] })
        hits = res['hits']['hits']
        if hits:
            results = [{"document_id": hit['_id'], "score": hit['_score'], "content": hit['_source'].get("content", "")} for hit in hits]
            return results
        error_message = 'Document not Found'
        status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=error_message)
    except Exception as e:
        raise HTTPException(status_code if status_code else status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


def search_document_by_id(doc_id: str) -> dict:
    status_code =''
    error_message = ''
    try:
        query = {"query": {"match": {"_id": doc_id}}}
        result = es.search(index=index, body=query)
        if result["hits"]["total"]["value"] > 0:
            doc = result["hits"]["hits"][0]["_source"]
            return doc
        status_code = status.HTTP_404_NOT_FOUND
        error_message = 'Document not Found'
        raise HTTPException(status_code=status_code, detail=error_message)
    except Exception as e:
        raise HTTPException(status_code if status_code else status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
