"""API endpoints for document management and search functionality."""

import logging
import time
from pathlib import Path as FilePath

from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile, status

from app.core.config import settings
from app.core.exceptions import DocumentProcessingError
from app.models.document import (
    DocumentBase,
    DocumentResponse,
    SearchQuery,
    SearchResponse,
    SearchResult,
)
from app.services.document_service import DocumentService
from app.services.vector_store import VectorStore

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing or invalid API key",
            "content": {"application/json": {"example": {"detail": "Invalid API key"}}},
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "description": "Rate limit exceeded",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Rate limit exceeded. Try again in 60 seconds."
                    }
                }
            },
        },
    },
)

document_service = DocumentService(str(settings.UPLOAD_DIR))
logger = logging.getLogger(__name__)


# Dependency for vector store
async def get_vector_store() -> VectorStore:
    """Get an instance of the vector store.

    Returns:
        VectorStore: A configured vector store instance
    """
    store = VectorStore()
    return store


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document",
    description="Upload and process a document file (PDF, DOCX, or TXT).",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Document uploaded successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Document uploaded successfully",
                        "filename": "example.pdf",
                        "size": 1024,
                        "path": "data/uploads/example.pdf",
                        "created_at": "2024-02-14T12:00:00Z",
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid file or processing error",
            "content": {
                "application/json": {"example": {"detail": "Empty file is not allowed"}}
            },
        },
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
            "description": "File too large",
            "content": {
                "application/json": {
                    "example": {"detail": "File size exceeds maximum limit of 10MB"}
                }
            },
        },
    },
)
async def upload_document(
    file: UploadFile = File(
        ..., description="The document file to upload (PDF, DOCX, or TXT)"
    )
) -> DocumentResponse:
    """
    Upload and process a document.

    The file will be validated, processed, and stored for later retrieval and searching.
    Supported formats are PDF, DOCX, and TXT files.

    - Validates file format and size
    - Processes document content
    - Stores the document for future access
    """
    try:
        logger.info(f"Processing upload request for file: {file.filename}")
        result = await document_service.process_document(file)
        return DocumentResponse(
            filename=str(result["filename"]),
            size=int(result["size"]),
            path=str(result["path"]),
            message="Document uploaded successfully",
        )
    except DocumentProcessingError as e:
        logger.error(f"Document processing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during document upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{filename}",
    response_model=DocumentBase,
    summary="Get document information",
    description="Retrieve information about a specific document by filename.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Document not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Document not found: example.pdf"}
                }
            },
        }
    },
)
async def get_document(
    filename: str = Path(
        ..., description="Name of the document file to retrieve", example="example.pdf"
    )
) -> FilePath:
    """
    Retrieve document information by filename.

    Returns metadata about the document including:
    - Filename
    - File size
    - File path
    """
    try:
        logger.info(f"Retrieving document: {filename}")
        return await document_service.get_document(filename)
    except DocumentProcessingError as e:
        logger.error(f"Document retrieval error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during document retrieval: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search documents",
    description="Search through documents using natural language queries.",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid search parameters",
            "content": {
                "application/json": {
                    "example": {"detail": "Search query cannot be empty"}
                }
            },
        }
    },
)
async def search_documents(
    query: SearchQuery, vector_store: VectorStore = Depends(get_vector_store)
) -> SearchResponse:
    """
    Search through documents using natural language queries.

    The search uses semantic similarity to find relevant documents and returns:
    - Matching document information
    - Relevance scores
    - Text snippets showing matches
    """
    try:
        logger.info(f"Processing search query: {query.query}")
        start_time = time.time()

        results = await vector_store.search(query.query, query.limit)

        # Convert results to response model
        search_results = [
            SearchResult(
                document=DocumentBase(
                    filename=FilePath(doc["path"]).name,
                    path=str(doc["path"]),
                    size=doc["size"],
                ),
                score=score,
                snippet=snippet,
            )
            for doc, score, snippet in results
        ]

        query_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        return SearchResponse(
            results=search_results, total=len(search_results), query_time_ms=query_time
        )
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Search operation failed")
