"""RAG (Retrieval-Augmented Generation) API endpoints for question answering."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from app.api.documents import get_vector_store
from app.core.middleware import RateLimiter
from app.services.rag_service import RAGService
from app.services.vector_store import VectorStore

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=60)


async def get_rag_service(
    request: Request, vector_store: VectorStore = Depends(get_vector_store)
) -> RAGService:
    """Get an instance of the RAG service with rate limiting.

    Args:
        request: The incoming request for rate limiting
        vector_store: The vector store instance for document retrieval

    Returns:
        RAGService: A configured RAG service instance

    Raises:
        HTTPException: If rate limit is exceeded
    """
    # Check rate limit
    is_limited, count = await rate_limiter.is_rate_limited(request)
    if is_limited:
        error_msg = (
            f"Rate limit exceeded. Maximum {rate_limiter.requests_per_minute} "
            "requests per minute."
        )
        raise HTTPException(status_code=429, detail=error_msg)
    return RAGService(vector_store)


@router.post("/ask")
async def ask_question(
    query: str, num_chunks: int = 3, rag_service: RAGService = Depends(get_rag_service)
) -> dict[str, Any]:
    """Ask a question and get a response using RAG.

    Args:
        query: The question to ask
        num_chunks: Number of document chunks to retrieve
        rag_service: The RAG service instance

    Returns:
        dict[str, Any]: The generated response with context
    """
    response = await rag_service.generate_response(query, num_chunks)
    return response


@router.post("/ask/stream")
async def ask_question_stream(
    query: str, num_chunks: int = 3, rag_service: RAGService = Depends(get_rag_service)
) -> StreamingResponse:
    """Ask a question and get a streaming response.

    Args:
        query: The question to ask
        num_chunks: Number of document chunks to retrieve
        rag_service: The RAG service instance

    Returns:
        StreamingResponse: A streaming response with generated text
    """
    return StreamingResponse(
        rag_service.generate_streaming_response(query, num_chunks),
        media_type="text/event-stream",
    )
