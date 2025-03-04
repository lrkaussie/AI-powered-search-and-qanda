"""Route handlers for the frontend application."""

import logging
from typing import Any

from fastapi import Form, Request, UploadFile
from fastapi.responses import HTMLResponse

from app.services.document_service import DocumentService
from app.services.rag_service import RAGService
from app.services.vector_store import VectorStore

# Configure logging
logger = logging.getLogger(__name__)

# Initialize services
document_service = DocumentService()
vector_store = VectorStore()
rag_service = RAGService(vector_store)


async def index(request: Request) -> HTMLResponse:
    """Render the main page.

    Args:
        request: The incoming request

    Returns:
        HTMLResponse: The rendered index page
    """
    from frontend.main import templates

    return templates.TemplateResponse("index.html", {"request": request})


async def upload_document(request: Request, file: UploadFile) -> dict[str, Any]:
    """Handle document upload.

    Args:
        request: The incoming request
        file: The uploaded file

    Returns:
        dict[str, Any]: Upload status and document information
    """
    try:
        result = await document_service.process_document(file)
        return {
            "success": True,
            "message": "Document uploaded successfully",
            "filename": result["filename"],
        }
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return {"success": False, "message": str(e)}


async def search_documents(
    request: Request, query: str = Form(...), limit: int = Form(5)
) -> dict[str, Any]:
    """Search through uploaded documents.

    Args:
        request: The incoming request
        query: Search query string
        limit: Maximum number of results to return

    Returns:
        dict[str, Any]: Search results with relevance scores
    """
    try:
        results = await vector_store.search(query, limit)
        return {"success": True, "results": results}
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return {"success": False, "message": str(e)}


async def ask_question(
    request: Request, question: str = Form(...), context: str = Form(None)
) -> dict[str, Any]:
    """Answer a question using RAG.

    Args:
        request: The incoming request
        question: User's question
        context: Optional context to consider

    Returns:
        dict[str, Any]: Generated answer with supporting context
    """
    try:
        response = await rag_service.query(question)
        return {"success": True, "answer": response}
    except Exception as e:
        logger.error(f"Question answering error: {str(e)}")
        return {"success": False, "message": str(e)}
