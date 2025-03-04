"""Custom exceptions and exception handlers for the application."""

from starlette.requests import Request
from starlette.responses import JSONResponse


class DocumentProcessingError(Exception):
    """Raised when there's an error processing a document."""

    pass


class RAGError(Exception):
    """Raised when there's an error in the RAG pipeline."""

    pass


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle custom exceptions and return appropriate JSON responses.

    Args:
        request: The incoming request
        exc: The exception that was raised

    Returns:
        JSONResponse: A JSON response with appropriate status code and error message
    """
    status_code = 500
    if isinstance(exc, DocumentProcessingError):
        status_code = 400
    elif isinstance(exc, RAGError):
        status_code = 422

    return JSONResponse(status_code=status_code, content={"detail": str(exc)})
