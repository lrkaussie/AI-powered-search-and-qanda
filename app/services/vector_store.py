import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any
from pathlib import Path

from app.core.config import settings
from app.models.document import Document

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_DIR,
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
    
    def _create_chunks(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), settings.CHUNK_SIZE - settings.CHUNK_OVERLAP):
            chunk = " ".join(words[i:i + settings.CHUNK_SIZE])
            chunks.append(chunk)
            
        return chunks
    
    async def add_document(self, document: Document) -> None:
        """Add a document to the vector store"""
        # Create chunks from document content
        chunks = self._create_chunks(document.content)
        
        # Generate chunk IDs
        chunk_ids = [f"{document.id}_chunk_{i}" for i in range(len(chunks))]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(chunks).tolist()
        
        # Create metadata for each chunk
        metadatas = [{
            "document_id": document.id,
            "title": document.title,
            "doc_type": document.doc_type,
            "chunk_index": i,
            **document.metadata
        } for i in range(len(chunks))]
        
        # Add to collection
        self.collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )
    
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant document chunks"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results["ids"][0])):
            formatted_results.append({
                "chunk": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
            
        return formatted_results 