# security.py
import time
from collections import defaultdict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# In-memory store for rate limiting (use Redis in production)
request_history = defaultdict(list)

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def __call__(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        current_time = time.time()
        
        # Clean up old requests outside the window
        request_history