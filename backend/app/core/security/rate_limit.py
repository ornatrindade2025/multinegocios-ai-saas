import time
from collections import defaultdict

from app.core.security.exceptions import RateLimitExceeded


class RateLimiter:

    def __init__(self, max_calls: int = 20, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls = defaultdict(list)

    def check(self, tenant_id: str) -> None:
        now = time.time()
        window_start = now - self.window_seconds

        calls = self.calls[tenant_id]

        self.calls[tenant_id] = [
            t for t in calls if t > window_start
        ]

        if len(self.calls[tenant_id]) >= self.max_calls:
            raise RateLimitExceeded("AI rate limit exceeded")

        self.calls[tenant_id].append(now)


rate_limiter = RateLimiter()
