from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Document(BaseModel):
    id: str
    title: str
    content: str
    doc_type: str
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow) 