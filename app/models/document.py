from datetime import datetime, UTC
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

def utc_now() -> datetime:
    """Return current UTC datetime with timezone information."""
    return datetime.now(UTC)

class Document(BaseModel):
    """Document model for storing document information."""
    id: str = Field(..., description="Unique identifier for the document")
    title: str = Field(..., description="Title of the document")
    content: str = Field(..., description="Full text content of the document")
    doc_type: str = Field(..., description="Type of document (pdf, docx, etc)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

class DocumentBase(BaseModel):
    """Base document model."""
    filename: str = Field(..., description="Name of the document file")
    size: int = Field(..., description="Size of the document in bytes")
    path: str = Field(..., description="Path to the stored document")

class DocumentResponse(DocumentBase):
    """Response model for document operations."""
    message: str = Field(..., description="Operation status message")
    created_at: datetime = Field(default_factory=utc_now)

class SearchQuery(BaseModel):
    """Search query model."""
    query: str = Field(..., min_length=1, description="Search query string")
    limit: int = Field(default=5, ge=1, le=20, description="Maximum number of results to return")

class SearchResult(BaseModel):
    """Search result model."""
    document: DocumentBase
    score: float = Field(..., description="Relevance score")
    snippet: Optional[str] = Field(None, description="Matching text snippet")

class SearchResponse(BaseModel):
    """Search response model."""
    results: List[SearchResult]
    total: int = Field(..., description="Total number of matching documents")
    query_time_ms: float = Field(..., description="Query execution time in milliseconds") 