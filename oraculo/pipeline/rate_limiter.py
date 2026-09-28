"""
Asynchronous TokenBucket Rate Limiter per Provider.
Enforces upstream API boundaries (e.g. AstroWay 30 req/min, FreeAstroAPI Astro Entry 50k req/mo).
"""

import asyncio
import time
from typing import Dict


class TokenBucketLimiter:
    def __init__(self, rate: float, capacity: float):
        """
        rate: tokens per second added
        capacity: max burst tokens
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.last_update = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)

            if self.tokens < 1.0:
                wait_time = (1.0 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0.0
                self.last_update = time.monotonic()
            else:
                self.tokens -= 1.0


class MultiProviderRateLimiter:
    def __init__(self):
        self.limiters: Dict[str, TokenBucketLimiter] = {
            # AstroWay Pro Indie: 30 req/min = 0.5 req/s sustained, burst 2
            "astroway": TokenBucketLimiter(rate=0.5, capacity=2.0),
            # FreeAstroAPI: Spaced out to prevent 429 burst errors (1 req/s, capacity 1)
            "freeastro": TokenBucketLimiter(rate=1.0, capacity=1.0),
            # Astrology-API.io Developer V3: 2 req/s
            "astrologyapi": TokenBucketLimiter(rate=2.0, capacity=4.0),
            # VedAstro PRO: 2 req/s
            "vedastro": TokenBucketLimiter(rate=2.0, capacity=4.0),
            # HebCal REST: 5 req/s
            "hebcal": TokenBucketLimiter(rate=5.0, capacity=5.0),
            # NASA Horizons: 2 req/s
            "nasa": TokenBucketLimiter(rate=2.0, capacity=4.0),
        }

    async def acquire(self, provider: str):
        limiter = self.limiters.get(provider.lower())
        if limiter:
            await limiter.acquire()
