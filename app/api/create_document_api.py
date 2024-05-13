from fastapi import APIRouter
from app.connectors.elasticsearchconnector import index_document
from app.models.schema import CreateDocument

router = APIRouter()

@router.post("/upload-documents/", response_model=dict)
def create_document_endpoint(document: CreateDocument):
    return index_document(document.content)
