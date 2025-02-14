from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

class DocumentProcessingError(Exception):
    """Raised when there's an error processing a document."""
    pass

class RAGError(Exception):
    """Raised when there's an error in the RAG pipeline."""
    pass

async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Generic exception handler for custom exceptions."""
    status_code = 500
    if isinstance(exc, DocumentProcessingError):
        status_code = 400
    elif isinstance(exc, RAGError):
        status_code = 422
    
    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)}
    ) 