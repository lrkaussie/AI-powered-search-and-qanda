"""Service for handling document storage and retrieval operations."""

from pathlib import Path

from fastapi import UploadFile

from app.core.exceptions import DocumentProcessingError


class DocumentService:
    """Service for managing document storage and retrieval."""

    def __init__(self, upload_dir: str = "data/uploads") -> None:
        """Initialize the document service.

        Args:
            upload_dir: Directory path for storing uploaded documents
        """
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def process_document(self, file: UploadFile) -> dict[str, str | int]:
        """Process and store an uploaded document.

        Args:
            file: The uploaded file to process

        Returns:
            dict[str, str | int]: Document information containing:
                - filename: Name of the stored file
                - size: Size of the file in bytes
                - path: Path where the file is stored

        Raises:
            DocumentProcessingError: If there's an error processing the document
        """
        try:
            # Create safe filename
            if file.filename is None:
                raise DocumentProcessingError("Filename is required")
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
                "path": str(file_path),
            }
        except DocumentProcessingError as e:
            raise e
        except Exception as e:
            raise DocumentProcessingError(f"Error processing document: {str(e)}")

    async def get_document(self, filename: str) -> Path:
        """Retrieve a document by filename.

        Args:
            filename: Name of the document to retrieve

        Returns:
            Path: Path to the requested document

        Raises:
            DocumentProcessingError: If the document is not found
        """
        file_path = self.upload_dir / filename
        if not file_path.exists():
            raise DocumentProcessingError(f"Document not found: {filename}")
        return file_path
