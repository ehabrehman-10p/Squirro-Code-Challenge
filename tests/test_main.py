import os
import sys
from fastapi.testclient import TestClient
import pytest

# Adding parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def created_doc_id(client):
    document_data = {"content": "Sample document helps in understanding the structure of the document."}
    response = client.post("/upload-documents/", json=document_data)
    assert response.status_code == 200
    doc_id = response.json().get("document_id")
    assert doc_id is not None, "Could not retrieve doc_id from the response"
    return doc_id

def test_create_document_endpoint(client):
    document_data = {"content": "Sample document helps in understanding the structure of the document."}
    response = client.post("/upload-documents/", json=document_data)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_create_document_endpoint_400_status_code(client):
    document_data = {"content": ""}
    response = client.post("/upload-documents/", json=document_data)
    assert response.status_code == 400
    assert isinstance(response.json(), dict)

def test_search_doc_by_id_endpoint(client, created_doc_id):
    response = client.get(f"/search-doc-by-id/?doc_id={created_doc_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_search_doc_by_id_endpoint_status_code_404(client):
    doc_id = "21ASf43564"
    response = client.get(f"/search-doc-by-id/?doc_id={doc_id}")
    assert response.status_code == 404
    assert isinstance(response.json(), dict)

def test_search_documents_endpoint(client):
    query = "sample document"
    k = 5
    response = client.get(f"/search-documents/?query={query}&k={k}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_documents_endpoint_404_status_code(client):
    query = " "
    k = 5
    response = client.get(f"/search-documents/?query={query}&k={k}")
    assert response.status_code == 404
    assert isinstance(response.json(), dict)

def test_generate_response_endpoint(client):
    query = "what is a Sample document?"
    response = client.get(f"/generate-response/?query={query}&k=5")
    assert response.status_code == 200
    assert isinstance(response.json(), str)
