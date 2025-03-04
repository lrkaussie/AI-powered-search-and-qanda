# Coding Standards and Guidelines

## Python Code Style

### 1. Code Formatting
- Use **Black** for code formatting with a line length of 88 characters
- Use **isort** for import sorting
- Use **flake8** for linting

```bash
# Format code
black .

# Sort imports
isort .

# Check code quality
flake8
```

### 2. Naming Conventions
- **Files/Modules**: Lowercase with underscores (e.g., `document_processor.py`)
- **Classes**: PascalCase (e.g., `DocumentProcessor`)
- **Functions/Methods**: Lowercase with underscores (e.g., `process_document`)
- **Variables**: Lowercase with underscores (e.g., `document_count`)
- **Constants**: Uppercase with underscores (e.g., `MAX_UPLOAD_SIZE`)
- **Private Methods/Variables**: Prefix with underscore (e.g., `_private_method`)

### 3. Documentation
- Use docstrings for all modules, classes, and functions
- Follow Google-style docstring format:

```python
def process_document(file_path: Path) -> Dict[str, Any]:
    """Process a document and extract its content.

    Args:
        file_path (Path): Path to the document file.

    Returns:
        Dict[str, Any]: Processed document with metadata.

    Raises:
        DocumentProcessingError: If processing fails.
    """
```

### 4. Type Hints
- Use type hints for all function parameters and return values
- Use `Optional` for parameters that can be None
- Use `Any` sparingly and only when necessary
- Use `TypeVar` for generic types

### 5. Error Handling
- Use custom exceptions for domain-specific errors
- Always include error messages that are user-friendly
- Log exceptions with appropriate log levels
- Handle exceptions at the appropriate level

### 6. Testing
- Write tests for all new functionality
- Follow AAA pattern (Arrange, Act, Assert)
- Use descriptive test names that explain the test case
- Use fixtures for common test setup
- Aim for >80% test coverage

```python
def test_upload_empty_file_raises_error():
    """Test that uploading an empty file raises an error."""
    # Arrange
    empty_file = create_empty_file()

    # Act & Assert
    with pytest.raises(DocumentProcessingError):
        upload_document(empty_file)
```

### 7. API Design
- Use RESTful principles
- Version all APIs
- Use appropriate HTTP methods and status codes
- Include comprehensive API documentation
- Validate all inputs using Pydantic models

### 8. Logging
- Use appropriate log levels:
  - DEBUG: Detailed information for debugging
  - INFO: General operational events
  - WARNING: Unexpected but handled events
  - ERROR: Errors that need attention
  - CRITICAL: System-level failures
- Include relevant context in log messages
- Use structured logging when possible

### 9. Code Organization
```
app/
├── api/          # API endpoints
├── core/         # Core functionality
├── models/       # Data models
├── services/     # Business logic
└── utils/        # Utility functions
```

### 10. Git Workflow
- Use feature branches for new development
- Branch naming: `feature/`, `bugfix/`, `hotfix/`
- Write clear commit messages:
  ```
  feat: add document processing functionality

  - Implement PDF processing
  - Add text extraction
  - Create document model
  ```
- Keep commits focused and atomic
- Squash commits before merging

### 11. Environment Variables
- Never commit sensitive data
- Use `.env` for local development
- Document all environment variables
- Provide `.env.example` with dummy values

### 12. Dependencies
- Pin dependency versions in requirements.txt
- Use virtual environments
- Document dependency purposes in requirements.txt
- Regular security updates for dependencies

### 13. Performance Guidelines
- Use async/await for I/O operations
- Implement caching where appropriate
- Optimize database queries
- Use connection pooling
- Implement rate limiting
- Monitor memory usage

### 14. Security Guidelines
- Input validation on all endpoints
- Sanitize file uploads
- Implement rate limiting
- Use secure headers
- Regular dependency updates
- Proper error handling without leaking details

### 15. Code Review Guidelines
#### What to Look For
- Code correctness
- Test coverage
- Documentation completeness
- Security considerations
- Performance implications
- Error handling
- Type safety

#### Review Process
1. Run automated checks (tests, linting)
2. Review documentation updates
3. Check for security implications
4. Verify error handling
5. Test locally if needed
6. Provide constructive feedback

### 16. Monitoring and Logging
- Use structured logging
- Include request IDs
- Log appropriate context
- Monitor performance metrics
- Set up alerting

### 17. Documentation Requirements
- README.md for each component
- API documentation
- Setup instructions
- Troubleshooting guides
- Architecture diagrams
- Update docs with code changes
