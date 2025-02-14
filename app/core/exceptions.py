from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Union

class DocumentProcessingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class RAGError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)

async def exception_handler(request: Request, exc: Union[DocumentProcessingError, RAGError]):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "type": exc.__class__.__name__,
            "path": request.url.path
        }
    ) 