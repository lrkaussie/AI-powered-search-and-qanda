import fitz  # PyMuPDF
from docx import Document as DocxDocument
from pathlib import Path
from typing import List, Dict, Any
import uuid

from app.models.document import Document

class DocumentProcessor:
    """Service for processing different types of documents"""
    
    supported_formats = {'.pdf', '.docx', '.txt'}
    
    @staticmethod
    async def process_document(file_path: Path) -> Document:
        """Process a document and return its content"""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_extension = file_path.suffix.lower()
        if file_extension not in DocumentProcessor.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
            
        if file_extension == '.pdf':
            content = await DocumentProcessor._process_pdf(file_path)
        elif file_extension == '.docx':
            content = await DocumentProcessor._process_docx(file_path)
        else:  # .txt
            content = await DocumentProcessor._process_txt(file_path)
            
        return Document(
            id=str(uuid.uuid4()),
            title=file_path.stem,
            content=content,
            doc_type=file_extension[1:],  # Remove the dot
            metadata={"original_filename": file_path.name}
        )
    
    @staticmethod
    async def _process_pdf(file_path: Path) -> str:
        """Extract text from PDF file"""
        text = []
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text.append(page.get_text())
        return "\n".join(text)
    
    @staticmethod
    async def _process_docx(file_path: Path) -> str:
        """Extract text from DOCX file"""
        doc = DocxDocument(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    @staticmethod
    async def _process_txt(file_path: Path) -> str:
        """Read text from TXT file"""
        return file_path.read_text(encoding='utf-8') 