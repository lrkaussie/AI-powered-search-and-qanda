from fastapi import status
import pytest
from pathlib import Path

def test_upload_document(client, test_document_path):
    """Test successful document upload."""
    with open(test_document_path, "rb") as f:
        response = client.post(
            "/documents/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    assert response.json()["filename"] == "test.txt"

def test_upload_empty_file(client, tmp_path):
    """Test uploading an empty file."""
    empty_file = tmp_path / "empty.txt"
    empty_file.touch()
    
    with open(empty_file, "rb") as f:
        response = client.post(
            "/documents/upload",
            files={"file": ("empty.txt", f, "text/plain")}
        )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "empty file" in response.json()["detail"].lower()

def test_upload_no_file(client):
    """Test upload endpoint without file."""
    response = client.post("/documents/upload")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_nonexistent_document(client):
    """Test retrieving a non-existent document."""
    response = client.get("/documents/nonexistent.txt")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()

def test_search_documents_invalid_query(client):
    """Test search with invalid query."""
    response = client.post(
        "/documents/search",
        json={"query": "", "limit": 5}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_search_documents_invalid_limit(client):
    """Test search with invalid limit."""
    response = client.post(
        "/documents/search",
        json={"query": "test", "limit": 0}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_search_documents_valid_query(client):
    """Test search with valid query."""
    response = client.post(
        "/documents/search",
        json={"query": "test query", "limit": 5}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "results" in data
    assert "total" in data
    assert "query_time_ms" in data

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"} 