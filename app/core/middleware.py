"""Middleware for request/response processing."""

import logging
import time
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)

# Store client request counts and timestamps
request_store: dict[str, tuple[int, datetime]] = {}


class RateLimiter:
    """Rate limiting implementation for API endpoints."""

    def __init__(self, requests_per_minute: int = 60):
        """Initialize rate limiter.

        Args:
            requests_per_minute: Maximum number of requests allowed per minute
        """
        self.requests_per_minute = requests_per_minute
        self.window = 60  # 1 minute window

    async def is_rate_limited(self, request: Request) -> tuple[bool, int]:
        """Check if request should be rate limited.

        Args:
            request: FastAPI request object

        Returns:
            tuple[bool, int]: A tuple containing:
                - bool: True if request should be limited, False otherwise
                - int: Current request count for the client
        """
        client_ip = request.client.host if request.client else "unknown"

        # Get current timestamp
        now = datetime.now()

        if client_ip in request_store:
            count, window_start = request_store[client_ip]

            # Reset counter if window has expired
            if now - window_start > timedelta(seconds=self.window):
                request_store[client_ip] = (1, now)
                return False, 1
            else:
                # Check if limit exceeded
                if count >= self.requests_per_minute:
                    return True, count
                request_store[client_ip] = (count + 1, window_start)
                return False, count + 1
        else:
            # First request from this client
            request_store[client_ip] = (1, now)
            return False, 1

    async def __call__(self, request: Request) -> None:
        """Check if request is within rate limits.

        Args:
            request: FastAPI request object

        Raises:
            HTTPException: If rate limit is exceeded
        """
        is_limited, count = await self.is_rate_limited(request)
        if is_limited:
            raise HTTPException(
                status_code=429, detail="Rate limit exceeded. Please try again later."
            )


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging request/response information."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process the request and log timing information.

        Args:
            request: The incoming request
            call_next: The next middleware in the chain

        Returns:
            Response: The response from the next middleware
        """
        start_time = time.time()

        # Process the request
        response = await call_next(request)

        # Calculate request duration
        duration = time.time() - start_time

        # Log request information
        logger.info(
            f"{request.method} {request.url.path} "
            f"completed in {duration:.2f}s with status {response.status_code}"
        )

        return response
