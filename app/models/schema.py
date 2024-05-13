from pydantic import BaseModel

class CreateDocument(BaseModel):
    content: str

class SearchResult(BaseModel):
    document_id: str
    content: str
    score: float
