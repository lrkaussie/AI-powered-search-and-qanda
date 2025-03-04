"""Test fixtures and configuration for pytest."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application.

    Returns:
        TestClient: A test client instance for making requests.
    """
    return TestClient(app)


@pytest.fixture
def test_document_path() -> str:
    """Create and return path to a test document.

    Returns:
        str: Path to the test document.
    """
    test_file = Path("tests/data/test.txt")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("Test content for document upload")
    return str(test_file)
