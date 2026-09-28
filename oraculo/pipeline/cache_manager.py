"""
Universal Idempotent Disk Cache Manager for Oráculo Pipeline.
Shields quotas for all external APIs and local MCP executions.
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Optional


class CacheManager:
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _compute_hash(self, key_data: Any) -> str:
        if isinstance(key_data, (dict, list)):
            normalized = json.dumps(key_data, sort_keys=True, ensure_ascii=False)
        else:
            normalized = str(key_data)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]

    def _get_path(self, provider: str, endpoint: str, key_data: Any) -> Path:
        safe_endpoint = endpoint.strip("/").replace("/", "_").replace("-", "_")
        h = self._compute_hash(key_data)
        filename = f"{provider}_{safe_endpoint}_{h}.json"
        return self.cache_dir / filename

    def get(self, provider: str, endpoint: str, key_data: Any) -> Optional[dict]:
        p = self._get_path(provider, endpoint, key_data)
        if not p.exists():
            return None
        try:
            with open(p, "r", encoding="utf-8") as f:
                payload = json.load(f)
                # Verify that it was a successful response
                if payload.get("_http_status", 200) == 200 or "data" in payload or "result" in payload:
                    return payload.get("data", payload)
        except Exception:
            return None
        return None

    def set(self, provider: str, endpoint: str, key_data: Any, data: Any, http_status: int = 200) -> None:
        p = self._get_path(provider, endpoint, key_data)
        record = {
            "_provider": provider,
            "_endpoint": endpoint,
            "_http_status": http_status,
            "data": data
        }
        try:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Cache write warning ({p}): {e}")

    def has_valid(self, provider: str, endpoint: str, key_data: Any) -> bool:
        return self.get(provider, endpoint, key_data) is not None
