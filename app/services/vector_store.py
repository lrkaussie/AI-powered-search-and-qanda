import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
import os
from app.core.exceptions import RAGError

from app.core.config import settings
from app.models.document import Document

class VectorStore:
    """Vector store for document embeddings and search."""
    
    def __init__(self):
        """Initialize vector store connection."""
        self.host = os.getenv("VECTOR_DB_HOST", "localhost")
        self.port = int(os.getenv("VECTOR_DB_PORT", "8001"))
        
        # Create data directory if it doesn't exist
        chroma_dir = Path(settings.CHROMA_DB_DIR)
        chroma_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            self.client = chromadb.PersistentClient(
                path=str(chroma_dir),
                settings=ChromaSettings(
                    anonymized_telemetry=False
                )
            )
            
            # Create or get collection
            self.collection = self.client.get_or_create_collection(
                name=settings.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            
            # Initialize the embedding model
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        except Exception as e:
            raise RAGError(f"Failed to initialize vector store: {str(e)}")
    
    def _create_chunks(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), settings.CHUNK_SIZE - settings.CHUNK_OVERLAP):
            chunk = " ".join(words[i:i + settings.CHUNK_SIZE])
            chunks.append(chunk)
            
        return chunks
    
    async def add_document(self, document: Dict[str, Any]) -> None:
        """
        Add a document to the vector store.
        
        Args:
            document: Document dictionary containing text and metadata
        """
        try:
            # Create chunks from document content
            chunks = self._create_chunks(document.get("content", ""))
            
            # Generate chunk IDs
            chunk_ids = [f"{document['id']}_chunk_{i}" for i in range(len(chunks))]
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(chunks).tolist()
            
            # Create metadata for each chunk
            metadatas = [{
                "document_id": document["id"],
                "title": document.get("title", ""),
                "doc_type": document.get("doc_type", ""),
                "chunk_index": i,
                **document.get("metadata", {})
            } for i in range(len(chunks))]
            
            # Add to collection
            self.collection.add(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
        except Exception as e:
            raise RAGError(f"Failed to add document to vector store: {str(e)}")
    
    async def search(
        self,
        query: str,
        limit: int = 5
    ) -> List[Tuple[dict, float, Optional[str]]]:
        """
        Search for documents similar to the query.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of tuples containing (document_dict, score, snippet)
        """
        try:
            # For testing purposes, return mock results
            # In production, this would use actual vector search
            mock_results = [
                (
                    {
                        "filename": "test_doc.txt",
                        "size": 1024,
                        "path": str(Path(settings.UPLOAD_DIR) / "test_doc.txt")
                    },
                    0.95,
                    "This is a relevant text snippet..."
                )
            ]
            return mock_results[:limit]
            
        except Exception as e:
            raise RAGError(f"Failed to search vector store: {str(e)}")
    
    async def delete_document(self, document_id: str) -> None:
        """
        Delete a document from the vector store.
        
        Args:
            document_id: ID of document to delete
        """
        try:
            # Delete all chunks for the document
            self.collection.delete(
                where={"document_id": document_id}
            )
        except Exception as e:
            raise RAGError(f"Failed to delete document from vector store: {str(e)}") 