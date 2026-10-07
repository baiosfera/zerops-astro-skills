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
        if isinstance(key_data, str) and len(key_data) == 16 and all(c in "0123456789abcdefABCDEF" for c in key_data):
            return key_data.lower()
        if isinstance(key_data, (dict, list)):
            normalized = json.dumps(key_data, sort_keys=True, ensure_ascii=False)
        else:
            normalized = str(key_data)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]

    def generate_client_hash(self, client_data: Any) -> str:
        """
        Generates a deterministic 16-character SHA-256 fingerprint for a client profile.
        Used as the client cache key and in cached dump filenames.
        """
        return self._compute_hash(client_data)

    def _get_path(self, provider: str, endpoint: str, key_data: Any, check_read: bool = False) -> Path:
        safe_endpoint = endpoint.strip("/").replace("/", "_").replace("-", "_")
        h = self._compute_hash(key_data)
        if safe_endpoint == "full_extract":
            filename = f"00_{provider}_full_extract_{h}.json"
        else:
            filename = f"{provider}_{safe_endpoint}_{h}.json"
        provider_dir = self.cache_dir / provider.lower()
        if not check_read:
            provider_dir.mkdir(parents=True, exist_ok=True)
        target = provider_dir / filename
        if check_read and not target.exists():
            if safe_endpoint == "full_extract":
                legacy_target = provider_dir / f"{provider}_full_extract_{h}.json"
                if legacy_target.exists():
                    return legacy_target
                candidates = list(provider_dir.glob(f"*{provider}*full_extract*.json"))
                if not candidates:
                    candidates = list(self.cache_dir.glob(f"*{provider}*full_extract*.json"))
                if candidates:
                    candidates.sort(key=lambda p: p.stat().st_size, reverse=True)
                    return candidates[0]
            legacy = self.cache_dir / filename
            if legacy.exists():
                return legacy
            if safe_endpoint == "full_extract":
                legacy_root = self.cache_dir / f"{provider}_full_extract_{h}.json"
                if legacy_root.exists():
                    return legacy_root
            alt_candidates = list(provider_dir.glob(f"{provider}_{safe_endpoint}_*.json"))
            if not alt_candidates:
                alt_candidates = list(self.cache_dir.glob(f"{provider}_{safe_endpoint}_*.json"))
            if alt_candidates:
                alt_candidates.sort(key=lambda p: p.stat().st_size, reverse=True)
                return alt_candidates[0]
        return target

    def get(self, provider: str, endpoint: str, key_data: Any) -> Optional[dict]:
        p = self._get_path(provider, endpoint, key_data, check_read=True)
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
        p = self._get_path(provider, endpoint, key_data, check_read=False)
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

    def has_endpoint(self, provider: str, endpoint: str, key_data: Any) -> bool:
        """Determines if a specific endpoint has an unpoisoned 200 OK result on disk."""
        data = self.get(provider, endpoint, key_data)
        if data is None:
            return False
        if isinstance(data, dict):
            if data.get("ok") is False or "error" in data:
                return False
        return True

    def get_endpoint(self, provider: str, endpoint: str, key_data: Any) -> Optional[Any]:
        """Retrieves raw data for a specific endpoint from disk cache."""
        return self.get(provider, endpoint, key_data)

    def set_endpoint(self, provider: str, endpoint: str, key_data: Any, data: Any, http_status: int = 200) -> None:
        """Immediately persists a successful endpoint calculation to disk."""
        self.set(provider, endpoint, key_data, data, http_status=http_status)

    def get_all_provider_endpoints(self, provider: str, key_data: Any) -> dict:
        """
        Scans cache directory and reconstructs the cumulative dictionary
        of all successfully extracted endpoints for this provider and client hash.
        Checks both provider subdirectories and legacy root cache for seamless compatibility.
        """
        h = self._compute_hash(key_data)
        prefix = f"{provider}_"
        suffix = f"_{h}.json"
        endpoints_data = {}
        if not self.cache_dir.exists():
            return endpoints_data

        try:
            dirs_to_check = [self.cache_dir / provider.lower(), self.cache_dir]
            for d in dirs_to_check:
                if not d.exists():
                    continue
                for p in d.glob(f"{prefix}*{suffix}"):
                    if p.name == f"{provider}_full_extract_{h}.json" or p.name == f"00_{provider}_full_extract_{h}.json":
                        continue
                    # Extract endpoint name from filename
                    stem = p.name[len(prefix):-len(suffix)]
                    if stem in endpoints_data:
                        continue
                    val = self.get(provider, stem, key_data)
                    if val is not None:
                        if isinstance(val, dict) and (val.get("ok") is False or "error" in val):
                            continue
                        endpoints_data[stem] = val
        except Exception as exc:
            print(f"⚠️ Error recovering accumulated endpoints for {provider}: {exc}")

        return endpoints_data

