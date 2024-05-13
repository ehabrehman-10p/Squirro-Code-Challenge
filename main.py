
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api import create_document_api,search_document_apis,generate_response_api

app = FastAPI(title="Code Challenge")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": exc})

app.include_router(create_document_api.router)
app.include_router(search_document_apis.router)
app.include_router(generate_response_api.router)
