from fastapi import APIRouter
from app.connectors.elasticsearchconnector import search_documents
from app.connectors.openaiconnector import generate_response


router = APIRouter()

@router.get("/generate-response/", response_model=str)
def generate_response_based_on_relevant_documents(query: str, k: int = 5):
    response = search_documents(query,k)
    documents = [result["content"] for result in response]
    try:
        result = generate_response(query, documents)
        return result
    except Exception as e:
        return(f"An error occured :  {str(e)}")
