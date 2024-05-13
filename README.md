Overview
--------
This application serves as a demonstration of building a FastAPI-based API that integrates with Elasticsearch for document indexing and searching, and utilizes the OpenAI API for generating responses based on user queries.

Project Structure
-----------------
Project Structure
main.py: Entry point of the FastAPI application. Defines the FastAPI instance, includes routers, and sets up global exception handling.
- app:
   - api: Contains API endpoint definitions.
      - create_document_api.py: Defines API endpoints related to uploading documents.
      - search_document_apis.py: Defines API endpoints related to searching documents.
   - connectors:
      - elasticsearchconnector.py: Contains functions to interact with Elasticsearch for indexing and searching documents.
      - openaiconnector.py: Contains function that is responsible for interacting with the OpenAI API to generate responses based on user queries and   document content.
   - models:
      - schema.py: Defines Pydantic models for request and response data.

How to Run
----------
- Clone the repository
- Setup Elasticsearch locally on your system
- Install dependencies with pip install -r requirements.txt
- Set up environment variables:
  - ES_INDEX: Elasticsearch index name
  - ES_URL: Elasticsearch instance URL : "http://localhost:9200"
  - OPENAI_API_KEY : Openai api key
- Run the FastAPI application with uvicorn main:app --reload
- Go to http://127.0.0.1:8000/docs to run the application through Swagger

API Endpoints
-------------
- POST /upload-documents/: Endpoint for uploading documents. Expects a JSON payload with the document content.
- GET /search-doc-by-id/: Endpoint for searching documents by document ID.
- GET /search-documents/: Endpoint for searching documents by content.
- GET /generate-response/ : Endpoint to get answers for user query. Answerswill be specific to the documents stored in Elasticsearch.

Quick Examples
--------------
Uploading Documents
-------------------
To upload a document, send a POST request to /upload-documents/ with the document content in the request body.

Example:

POST /upload-documents/
{
"content": "This is a sample document."
}

Searching Documents by content
------------------------------
To search for documents, send a GET request to /search-documents/ with the query parameter.

Example:
GET /search-documents/?query=sample&k=5

Searching Documents by id
------------------------------
To search for documents, send a GET request to /search-doc-by-id/ with the query parameter.

Example:
GET /search-doc-by-id/?query=id

Generating Response
-------------------
To generate a response based on a query, send a GET request to /generate-response/ with the query parameter.

Example:
GET /generate-response/?query=What is a sample document?&k=5

Testing
-------
Unit tests are provided to ensure the functionality of the API endpoints. Run tests with pytest.
