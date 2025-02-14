from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
from typing import Dict, Tuple
import asyncio

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
        self._cleanup_task = None

    async def _cleanup_old_requests(self):
        while True:
            current_time = time.time()
            for ip in list(self.requests.keys()):
                self.requests[ip] = [t for t in self.requests[ip] if current_time - t < 60]
                if not self.requests[ip]:
                    del self.requests[ip]
            await asyncio.sleep(60)

    async def start(self):
        self._cleanup_task = asyncio.create_task(self._cleanup_old_requests())

    async def stop(self):
        if self._cleanup_task:
            self._cleanup_task.cancel()

    async def is_rate_limited(self, request: Request) -> Tuple[bool, int]:
        client_ip = request.client.host
        current_time = time.time()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        self.requests[client_ip].append(current_time)
        request_count = len(self.requests[client_ip])

        if request_count > self.requests_per_minute:
            return True, request_count
        return False, request_count