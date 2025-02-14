from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
import shutil
import tempfile

from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStore
from app.models.document import Document

router = APIRouter()

# Dependency for vector store
async def get_vector_store():
    store = VectorStore()
    return store

@router.post("/upload", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    vector_store: VectorStore = Depends(get_vector_store)
):
    """Upload, process, and store a document"""
    # Verify file extension
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in DocumentProcessor.supported_formats:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Supported formats: {DocumentProcessor.supported_formats}"
        )
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = Path(tmp_file.name)
    
    try:
        # Process the document
        document = await DocumentProcessor.process_document(tmp_path)
        # Store in vector database
        await vector_store.add_document(document)
        return document
    finally:
        # Clean up temporary file
        tmp_path.unlink()

@router.post("/search")
async def search_documents(
    query: str,
    limit: int = 5,
    vector_store: VectorStore = Depends(get_vector_store)
):
    """Search through documents"""
    results = await vector_store.search(query, limit)
    return results 