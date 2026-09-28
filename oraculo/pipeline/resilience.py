"""
Resilience module: Circuit Breaker and Exponential Backoff for Oráculo.
Prevents burning user quotas on upstream failures or invalid credentials.
"""

import asyncio
import random
import time
from typing import Callable, Any, Optional


class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self, is_fatal: bool = False):
        self.failure_count += 1
        self.last_failure_time = time.monotonic()
        if is_fatal or self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def allow_request(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if time.monotonic() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
            return False
        return True  # HALF_OPEN allows test request


async def retry_with_backoff(
    coro_func: Callable[[], Any],
    max_retries: int = 2,
    base_delay: float = 1.0,
    max_delay: float = 5.0
) -> Any:
    retries = 0
    while True:
        try:
            return await coro_func()
        except Exception as e:
            retries += 1
            if retries > max_retries:
                raise e
            delay = min(max_delay, base_delay * (2 ** (retries - 1)) + random.uniform(0, 0.5))
            await asyncio.sleep(delay)
