from pathlib import Path
from typing import BinaryIO
from fastapi import UploadFile
from app.core.exceptions import DocumentProcessingError

class DocumentService:
    def __init__(self, upload_dir: str = "data/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def process_document(self, file: UploadFile) -> dict:
        """Process and store an uploaded document."""
        try:
            # Create safe filename
            safe_filename = Path(file.filename).name
            file_path = self.upload_dir / safe_filename

            # Read and validate content
            content = await file.read()
            if len(content) == 0:
                raise DocumentProcessingError("Empty file is not allowed")

            # Save the file
            with open(file_path, "wb") as f:
                f.write(content)

            return {
                "filename": safe_filename,
                "size": len(content),
                "path": str(file_path)
            }
        except DocumentProcessingError as e:
            raise e
        except Exception as e:
            raise DocumentProcessingError(f"Error processing document: {str(e)}")

    async def get_document(self, filename: str) -> Path:
        """Retrieve a document by filename."""
        file_path = self.upload_dir / filename
        if not file_path.exists():
            raise DocumentProcessingError(f"Document not found: {filename}")
        return file_path 