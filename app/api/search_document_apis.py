from typing import List
from fastapi import APIRouter
from app.connectors.elasticsearchconnector import search_document_by_id,search_documents
from app.models.schema import SearchResult

router = APIRouter()

@router.get("/search-doc-by-id/", response_model=dict)
async def search_doc_by_id(doc_id: str):
    return search_document_by_id(doc_id)

@router.get("/search-documents/", response_model=List[SearchResult])
def search_documents_endpoint(query: str, k: int = 5):
    return search_documents(query, k)
