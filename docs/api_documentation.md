# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API uses API key authentication. Include the API key in the request header:
```
X-API-Key: your-api-key
```

## Endpoints

### Health Check
#### GET /health
Check the health status of the API.

**Response**
```json
{
    "status": "healthy"
}
```

### Document Management

#### POST /documents/upload
Upload and process a new document.

**Request**
- Content-Type: multipart/form-data
- Body:
  - file: (binary) The document file to upload (PDF, DOCX, or TXT)

**Response**
```json
{
    "message": "Document uploaded successfully",
    "filename": "example.pdf",
    "size": 1024,
    "path": "data/uploads/example.pdf",
    "created_at": "2024-02-14T12:00:00Z"
}
```

**Error Responses**
- 400: Invalid file or processing error
- 413: File too large
- 415: Unsupported file type
- 500: Server error

#### GET /documents/{filename}
Retrieve information about a specific document.

**Parameters**
- filename (string): Name of the document file

**Response**
```json
{
    "filename": "example.pdf",
    "size": 1024,
    "path": "data/uploads/example.pdf"
}
```

**Error Responses**
- 404: Document not found
- 500: Server error

#### POST /documents/search
Search through documents using natural language queries.

**Request**
```json
{
    "query": "What are the key findings in the research paper?",
    "limit": 5
}
```

**Parameters**
- query (string, required): The search query
- limit (integer, optional): Maximum number of results to return (default: 5, max: 20)

**Response**
```json
{
    "results": [
        {
            "document": {
                "filename": "research_paper.pdf",
                "size": 1024,
                "path": "data/uploads/research_paper.pdf"
            },
            "score": 0.95,
            "snippet": "The key findings indicate that..."
        }
    ],
    "total": 1,
    "query_time_ms": 125.45
}
```

**Error Responses**
- 400: Invalid query parameters
- 500: Search operation failed

## Rate Limiting
The API implements rate limiting to ensure fair usage:
- 100 requests per hour per API key
- Rate limit headers are included in responses:
  - X-RateLimit-Limit: Maximum requests per hour
  - X-RateLimit-Remaining: Remaining requests
  - X-RateLimit-Reset: Time until limit resets (Unix timestamp)

## Error Responses
All error responses follow this format:
```json
{
    "detail": "Error message describing what went wrong"
}
```

Common HTTP Status Codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 413: Payload Too Large
- 415: Unsupported Media Type
- 429: Too Many Requests
- 500: Internal Server Error

## File Support
Supported file formats:
- PDF (.pdf)
- Microsoft Word (.docx)
- Plain Text (.txt)

Maximum file size: 10MB

## Best Practices
1. Always check response status codes
2. Implement proper error handling
3. Respect rate limits
4. Use appropriate content types
5. Keep API keys secure
