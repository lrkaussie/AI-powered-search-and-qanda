from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
import time
import logging
from typing import List

from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStore
from app.models.document import (
    DocumentResponse,
    SearchQuery,
    SearchResponse,
    SearchResult,
    DocumentBase
)
from app.services.document_service import DocumentService
from app.core.exceptions import DocumentProcessingError
from app.core.config import settings

router = APIRouter()
document_service = DocumentService(str(settings.UPLOAD_DIR))
logger = logging.getLogger(__name__)

# Dependency for vector store
async def get_vector_store():
    store = VectorStore()
    return store

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document.
    """
    try:
        logger.info(f"Processing upload request for file: {file.filename}")
        result = await document_service.process_document(file)
        return DocumentResponse(
            message="Document uploaded successfully",
            **result
        )
    except DocumentProcessingError as e:
        logger.error(f"Document processing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during document upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{filename}", response_model=DocumentBase)
async def get_document(filename: str):
    """
    Retrieve a document by filename.
    """
    try:
        logger.info(f"Retrieving document: {filename}")
        file_path = await document_service.get_document(filename)
        return DocumentBase(
            filename=filename,
            path=str(file_path),
            size=file_path.stat().st_size
        )
    except DocumentProcessingError as e:
        logger.error(f"Document retrieval error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during document retrieval: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/search", response_model=SearchResponse)
async def search_documents(
    query: SearchQuery,
    vector_store: VectorStore = Depends(get_vector_store)
):
    """Search through documents"""
    try:
        logger.info(f"Processing search query: {query.query}")
        start_time = time.time()
        
        results = await vector_store.search(query.query, query.limit)
        
        # Convert results to response model
        search_results = [
            SearchResult(
                document=DocumentBase(
                    filename=Path(doc["path"]).name,
                    path=str(doc["path"]),
                    size=doc["size"]
                ),
                score=score,
                snippet=snippet
            )
            for doc, score, snippet in results
        ]
        
        query_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return SearchResponse(
            results=search_results,
            total=len(search_results),
            query_time_ms=query_time
        )
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Search operation failed") 