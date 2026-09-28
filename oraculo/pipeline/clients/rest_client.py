"""
Unified Asynchronous HTTP/2 REST Client for Oráculo (v4.0).
Consolidates FreeAstroAPI, Astrology-API.io, AstroWay REST, VedAstro, HebCal, and NASA.
Auto-injects canonical authentication headers per provider to prevent cross-inversion bugs.
Captures credit headers and strictly shields with CacheManager.
"""

import asyncio
from typing import Any, Dict, Optional

try:
    import httpx
except ImportError:
    httpx = None

from pipeline.config import config
from pipeline.cache_manager import CacheManager
from pipeline.rate_limiter import MultiProviderRateLimiter
from pipeline.resilience import CircuitBreaker, retry_with_backoff


class UnifiedRestClient:
    def __init__(self, cache_manager: CacheManager, refresh_pro: bool = False):
        self.cache = cache_manager
        self.refresh_pro = refresh_pro
        self.rate_limiter = MultiProviderRateLimiter()
        self.breakers: Dict[str, CircuitBreaker] = {
            "freeastro": CircuitBreaker(),
            "astrologyapi": CircuitBreaker(),
            "astroway": CircuitBreaker(),
            "vedastro": CircuitBreaker(),
            "hebcal": CircuitBreaker(),
            "nasa": CircuitBreaker(),
        }
        self.client: Optional[Any] = None
        self.credit_stats: Dict[str, Any] = {
            "astroway_credits_remaining": None,
            "astroway_credits_used": None,
            "calls_made": {"freeastro": 0, "astrologyapi": 0, "astroway": 0, "vedastro": 0, "hebcal": 0, "nasa": 0},
            "cache_hits": {"freeastro": 0, "astrologyapi": 0, "astroway": 0, "vedastro": 0, "hebcal": 0, "nasa": 0},
        }

    async def __aenter__(self):
        if httpx is None:
            raise RuntimeError("httpx is required for live network requests. Install with: sudo apt-get install -y python3-httpx or pip install httpx")
        try:
            self.client = httpx.AsyncClient(
                http2=True,
                timeout=httpx.Timeout(15.0, connect=5.0),
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=30)
            )
        except Exception:
            self.client = httpx.AsyncClient(
                http2=False,
                timeout=httpx.Timeout(15.0, connect=5.0),
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=30)
            )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    def _resolve_canonical_headers(self, provider_key: str, headers: Optional[dict]) -> dict:
        """Injects canonical auth headers per provider, overriding any erroneous input."""
        h = dict(headers or {})
        h["Content-Type"] = "application/json"

        if provider_key == "astroway":
            # AstroWay STRICTLY requires X-Api-Key
            if config.astroway_api_key:
                h["X-Api-Key"] = config.astroway_api_key
            h.pop("Authorization", None)

        elif provider_key == "astrologyapi":
            # Astrology-API.io Developer V3 STRICTLY requires Authorization: Bearer
            if config.astrology_api_key:
                h["Authorization"] = f"Bearer {config.astrology_api_key}"
            h.pop("x-api-key", None)

        elif provider_key == "freeastro":
            # FreeAstroAPI requires x-api-key
            if config.freeastro_api_key:
                h["x-api-key"] = config.freeastro_api_key

        elif provider_key == "vedastro":
            # VedAstro PRO requires x-api-key
            if config.vedastro_api_key:
                h["x-api-key"] = config.vedastro_api_key

        return h

    async def request(
        self,
        provider: str,
        method: str,
        url: str,
        endpoint_key: str,
        headers: Optional[dict] = None,
        json_data: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> dict:
        provider_key = provider.lower()
        key_data = json_data if json_data is not None else (params or {})

        # 1. Check Cache
        allow_cache_bypass = self.refresh_pro and provider_key in ["astroway", "vedastro"]
        if not allow_cache_bypass:
            cached = self.cache.get(provider_key, endpoint_key, key_data)
            if cached is not None:
                self.credit_stats["cache_hits"][provider_key] = self.credit_stats["cache_hits"].get(provider_key, 0) + 1
                return cached

        # 2. Circuit Breaker Check
        breaker = self.breakers.get(provider_key)
        if breaker and not breaker.allow_request():
            return {"error": f"Circuit breaker OPEN for {provider_key} (too many recent failures)"}

        # 3. Rate Limiter
        await self.rate_limiter.acquire(provider_key)

        # 4. Resolve Canonical Headers
        final_headers = self._resolve_canonical_headers(provider_key, headers)

        # 5. Perform Request
        async def _do_req():
            if not self.client:
                raise RuntimeError("Client not initialized. Use 'async with UnifiedRestClient(...)'.")
            
            resp = await self.client.request(
                method=method,
                url=url,
                headers=final_headers,
                json=json_data,
                params=params,
            )
            
            # Capture AstroWay credit headers
            if provider_key == "astroway":
                rem = resp.headers.get("X-Credits-Remaining")
                used = resp.headers.get("X-Credits-Used")
                if rem is not None:
                    self.credit_stats["astroway_credits_remaining"] = rem
                if used is not None:
                    self.credit_stats["astroway_credits_used"] = used

            if resp.status_code in [401, 403]:
                if breaker:
                    breaker.record_failure(is_fatal=True)
                return {"error": f"Authentication failure ({resp.status_code}): {resp.text[:120]}", "status_code": resp.status_code}

            if resp.status_code >= 500:
                resp.raise_for_status()

            if resp.status_code == 429:
                raise RuntimeError(f"Rate limit exceeded (429) for {provider_key}")

            try:
                data = resp.json()
            except Exception:
                data = {"raw_text": resp.text}

            # Cache successful response
            if resp.status_code == 200:
                if breaker:
                    breaker.record_success()
                self.cache.set(provider_key, endpoint_key, key_data, data, http_status=200)
                self.credit_stats["calls_made"][provider_key] = self.credit_stats["calls_made"].get(provider_key, 0) + 1

            return data

        try:
            return await retry_with_backoff(_do_req, max_retries=2, base_delay=1.5)
        except Exception as e:
            if breaker:
                breaker.record_failure()
            return {"error": str(e)}
