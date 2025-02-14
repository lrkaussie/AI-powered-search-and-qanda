from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import StreamingResponse
from typing import Dict, Any

from app.services.vector_store import VectorStore
from app.services.rag_service import RAGService
from app.core.middleware import RateLimiter
from app.api.documents import get_vector_store

router = APIRouter()
rate_limiter = RateLimiter(requests_per_minute=60)

# Dependency for RAG service
async def get_rag_service(
    request: Request,
    vector_store: VectorStore = Depends(get_vector_store)
):
    # Check rate limit
    is_limited, count = await rate_limiter.is_rate_limited(request)
    if is_limited:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {rate_limiter.requests_per_minute} requests per minute."
        )
    return RAGService(vector_store)

@router.post("/ask")
async def ask_question(
    query: str,
    num_chunks: int = 3,
    rag_service: RAGService = Depends(get_rag_service)
) -> Dict[str, Any]:
    """Ask a question and get a response using RAG"""
    response = await rag_service.generate_response(query, num_chunks)
    return response

@router.post("/ask/stream")
async def ask_question_stream(
    query: str,
    num_chunks: int = 3,
    rag_service: RAGService = Depends(get_rag_service)
):
    """Ask a question and get a streaming response"""
    return StreamingResponse(
        rag_service.generate_streaming_response(query, num_chunks),
        media_type="text/event-stream"
    )