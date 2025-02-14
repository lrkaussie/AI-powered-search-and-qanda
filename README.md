# AI-Powered Document Search & Q&A System

A powerful document search and question-answering system built with FastAPI, utilizing advanced LLM and RAG techniques.

## Features

- Document upload and processing (PDF, DOCX)
- Vector-based semantic search
- Question answering using RAG (Retrieval Augmented Generation)
- Real-time document processing
- REST API interface
- Streamlit-based UI (coming soon)

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- Git

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-powered-search-qanda
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

3. Start the application using Docker:
   ```bash
   docker-compose up --build
   ```

The application will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Vector DB Interface: http://localhost:8001

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Documents
- `POST /documents/upload` - Upload a document
- `GET /documents/{filename}` - Retrieve document info
- `POST /documents/search` - Search through documents

## Testing

Run the test suite:
```bash
pytest
```

## Project Structure

```
.
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core functionality
│   ├── models/         # Pydantic models
│   └── services/       # Business logic
├── tests/              # Test suite
├── docs/               # Documentation
└── docker/            # Docker configuration
```

## Environment Variables

Key environment variables:
- `ENVIRONMENT` - development/production
- `DEBUG` - Enable debug mode (1/0)
- `APP_PORT` - Application port
- `VECTOR_DB_HOST` - Vector database host
- `MAX_UPLOAD_SIZE` - Maximum upload size in bytes

See `.env.example` for all available options.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 