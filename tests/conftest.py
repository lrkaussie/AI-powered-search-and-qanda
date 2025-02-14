import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Test client fixture for FastAPI application."""
    return TestClient(app)

@pytest.fixture
def test_document_path(tmp_path):
    """Create a test document for upload testing."""
    doc = tmp_path / "test.txt"
    doc.write_text("This is a test document for testing purposes.")
    return str(doc) 