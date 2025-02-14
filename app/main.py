from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import documents
from app.core.exceptions import DocumentProcessingError, RAGError, exception_handler
from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title="AI Document Search & Q&A System",
    description="An AI-powered system for document search and question answering",
    version="1.0.0"
)

# Add exception handlers
app.add_exception_handler(DocumentProcessingError, exception_handler)
app.add_exception_handler(RAGError, exception_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix="/documents", tags=["documents"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to AI Document Search & Q&A API"}

@app.post("/documents")
async def upload_document():
    # TODO: Implement document upload logic
    return {"message": "Document upload endpoint"}

@app.post("/query")
async def query_documents():
    # TODO: Implement document querying logic
    return {"message": "Query endpoint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 