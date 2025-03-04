"""Initialize and configure the FastAPI application."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api import documents, rag
from app.core.config import settings
from app.core.exceptions import DocumentProcessingError, RAGError, exception_handler
from app.core.logging import setup_logging
from app.core.middleware import LoggingMiddleware

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API for document processing, search, and question answering",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "documents",
            "description": "Operations with documents: upload, retrieve, and search",
        },
        {
            "name": "health",
            "description": "API health check endpoints",
        },
    ],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Register exception handlers
app.add_exception_handler(DocumentProcessingError, exception_handler)
app.add_exception_handler(RAGError, exception_handler)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Custom API documentation endpoints
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html() -> HTMLResponse:
    """Serve custom Swagger UI documentation."""
    if app.openapi_url is None:
        raise HTTPException(status_code=404, detail="OpenAPI URL not found")
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html() -> HTMLResponse:
    """Serve ReDoc documentation."""
    if app.openapi_url is None:
        raise HTTPException(status_code=404, detail="OpenAPI URL not found")
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


# Include routers
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(rag.router, prefix=settings.API_V1_STR)


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    """Return welcome message and API version.

    Returns:
        dict[str, str]: Welcome message and version information
    """
    return {
        "message": "Welcome to the Document Q&A API",
        "version": "1.0.0",
    }


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Check API health status.

    Returns:
        dict[str, str]: Health status information
    """
    return {"status": "healthy"}


@app.post("/documents")
async def upload_document() -> JSONResponse:
    """Upload a document to the system."""
    # TODO: Implement document upload logic
    return JSONResponse(content={"message": "Document upload endpoint"})


@app.post("/query")
async def query_documents() -> JSONResponse:
    """Query documents in the system."""
    # TODO: Implement document querying logic
    return JSONResponse(content={"message": "Query endpoint"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
