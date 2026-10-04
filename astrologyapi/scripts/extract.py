#!/usr/bin/env python3
"""
Autonomous Extractor for Astrology-API.io (V3 API v2.0)
Supports Dual-Mode Execution:
1. --free-tier (Default): 24 high-value exclusive endpoints (Kabbalah, Tikkun, Birth Angels,
   Tree of Life, Almuten Figuris, Fixed Stars, and Traditional Analysis), safely preserving
   the user's 50 free monthly requests.
2. --all: Complete 240+ endpoint universal catalog from OpenAPI 3.1 for paid/pro tiers.
Enforces flat birth_data schema for Kabbalah endpoints and nested subject.birth_data for others.
"""

import argparse
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Optional, Tuple
import httpx

BASE_URL = os.getenv("ASTROLOGY_API_URL", "https://api.astrology-api.io/api/v3")
DEFAULT_TIMEOUT = 15.0


def resolve_astrologyapi_payload(
    path: str,
    full_name: str,
    birth_data_obj: Dict[str, Any],
    today_str: str
) -> Dict[str, Any]:
    """
    Builds the exact request body based on Astrology-API.io OpenAPI 3.1 requirements.
    Kabbalah endpoints strictly require flat 'birth_data' at root.
    Other endpoints expect nested 'subject.birth_data'.
    """
    clean_p = path.lower()

    # 1. Flat birth_data payloads for Kabbalah endpoints
    if "/kabbalah" in clean_p:
        return {
            "birth_data": birth_data_obj
        }

    # 2. Timing timeline requires target_date
    if "/timing/timeline" in clean_p:
        return {
            "subject": {
                "name": full_name,
                "birth_data": birth_data_obj
            },
            "target_date": today_str
        }

    # 3. Numerology options
    if "/numerology" in clean_p:
        return {
            "subject": {
                "name": full_name,
                "birth_data": birth_data_obj
            },
            "options": {
                "language": "es",
                "detail_level": "standard"
            }
        }

    # 4. Fixed stars options
    if "/fixed-stars" in clean_p:
        return {
            "subject": {
                "name": full_name,
                "birth_data": birth_data_obj
            },
            "options": {
                "max_orb": 1.0
            }
        }

    # 5. Standard nested subject payload
    return {
        "subject": {
            "name": full_name,
            "birth_data": birth_data_obj
        }
    }


def get_free_tier_endpoints() -> List[Tuple[str, str]]:
    """
    Curated suite of 5 exclusive jewels that do not duplicate other APIs
    and preserve the user's 50 free monthly credits (allowing 10 charts/month).
    """
    return [
        ("kabbalah_birth_angels", "/kabbalah/birth-angels"),
        ("kabbalah_tikkun", "/kabbalah/tikkun"),
        ("kabbalah_tree_of_life", "/kabbalah/tree-of-life-chart"),
        ("traditional_almuten", "/traditional/almuten"),
        ("timing_timeline", "/timing/timeline"),
    ]


def load_all_endpoints() -> List[Tuple[str, str]]:
    """
    Loads universal single-chart natal endpoints catalog from skill assets,
    falling back to free tier if catalog is missing.
    """
    catalog_path = Path(__file__).parent.parent / "assets" / "natal_endpoints_catalog.json"
    if catalog_path.exists():
        try:
            raw = json.loads(catalog_path.read_text(encoding="utf-8"))
            endpoints = []
            for item in raw:
                path = item[0]
                # Strip prefix /api/v3
                clean_path = path.replace("/api/v3", "") if path.startswith("/api/v3") else path
                key_name = clean_path.strip("/").replace("/", "_").replace("-", "_")
                endpoints.append((key_name, clean_path))
            if endpoints:
                return endpoints
        except Exception:
            pass

    return get_free_tier_endpoints()


async def extract_astrologyapi(
    client_data: Dict[str, Any],
    api_key: Optional[str] = None,
    client: Optional[httpx.AsyncClient] = None,
    mode: str = "free-tier",
    cache_manager: Optional[Any] = None,
    client_hash: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extracts calculations from Astrology-API.io.
    mode='free-tier' restricts to 6 curated jewel endpoints to protect the 50 free credits limit.
    mode='all' executes the full 240+ endpoint catalog.
    Supports atomic delta-cache skipping and recording.
    """
    key = api_key or os.getenv("ASTROLOGY_API_IO") or os.getenv("ASTROLOGY_API_KEY") or os.getenv("astrology_apiKey")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if key:
        headers["Authorization"] = f"Bearer {key}"

    full_name = client_data.get("name", "Consultant")
    year = int(client_data.get("year", 1990))
    month = int(client_data.get("month", 1))
    day = int(client_data.get("day", 1))
    hour = int(client_data.get("hour", 12))
    minute = int(client_data.get("minute", 0))
    lat = float(client_data.get("lat", 0.0))
    lng = float(client_data.get("lng", 0.0))
    tz_str = client_data.get("tz_str", "UTC")
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    birth_data_obj = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "latitude": lat,
        "longitude": lng,
        "timezone": tz_str
    }

    if mode == "all":
        raw_endpoints = load_all_endpoints()
    else:
        raw_endpoints = get_free_tier_endpoints()

    endpoints = [
        (key_name, path, resolve_astrologyapi_payload(path, full_name, birth_data_obj, today_str))
        for key_name, path in raw_endpoints
    ]

    results: Dict[str, Any] = {
        "provider": "astrologyapi",
        "mode": mode,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "SUCCESS",
        "quota_note": "Free Tier has 50 requests/month limit. Current run planned: {} calls".format(len(endpoints)),
        "calls_made": 0,
        "data": {},
        "raw_responses": {},
        "endpoint_audits": [],
        "failures": []
    }

    close_client = False
    if client is None:
        client = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT, follow_redirects=True)
        close_client = True

    try:
        total_eps = len(endpoints)
        for idx, (key_name, path, body) in enumerate(endpoints, 1):
            # Check delta cache
            if cache_manager and client_hash:
                cached_data = cache_manager.get_endpoint("astrologyapi", key_name, client_hash)
                if cached_data is not None:
                    print(f"⚡ [AstrologyAPI ({idx}/{total_eps})] {key_name} -> [CACHED / SKIP]", flush=True)
                    results["data"][key_name] = cached_data
                    results["raw_responses"][key_name] = cached_data
                    results["endpoint_audits"].append({
                        "endpoint": key_name,
                        "status": "CACHED",
                        "http_status": 200,
                        "latency_ms": 0.0,
                        "error": None
                    })
                    continue

            url = f"{BASE_URL}{path}" if path.startswith("/") else f"{BASE_URL}/{path}"
            if results["calls_made"] > 0:
                # Polite pacing to respect rate limits and avoid 429
                await asyncio.sleep(1.0)

            t0 = time.perf_counter()
            for attempt in range(2):
                try:
                    resp = await client.post(url, headers=headers, json=body)
                    results["calls_made"] += 1
                    lat = (time.perf_counter() - t0) * 1000.0

                    if resp.status_code == 200:
                        data = resp.json()
                        results["raw_responses"][key_name] = data

                        # Check semantic error in body
                        if isinstance(data, dict) and "detail" in data:
                            err_msg = str(data.get("detail"))
                            print(f"❌ [AstrologyAPI ({idx}/{total_eps})] {key_name} -> [DETAIL ERR] ({lat:.1f}ms): {err_msg}", flush=True)
                            results["failures"].append({"endpoint": key_name, "error": err_msg})
                            results["data"][key_name] = {"error": err_msg}
                            results["endpoint_audits"].append({
                                "endpoint": key_name,
                                "status": "FAILED",
                                "http_status": 200,
                                "latency_ms": lat,
                                "error": err_msg
                            })
                        else:
                            extracted_val = data.get("data", data)
                            results["data"][key_name] = extracted_val
                            if cache_manager and client_hash:
                                cache_manager.set_endpoint("astrologyapi", key_name, client_hash, extracted_val)
                            print(f"✨ [AstrologyAPI ({idx}/{total_eps})] {key_name} -> [200 OK] ({lat:.1f}ms)", flush=True)
                            results["endpoint_audits"].append({
                                "endpoint": key_name,
                                "status": "SUCCESS",
                                "http_status": 200,
                                "latency_ms": lat,
                                "error": None
                            })
                        break
                    elif resp.status_code == 429:
                        if attempt == 0:
                            await asyncio.sleep(3.0)
                            continue
                        err_msg = "Rate limit exceeded (429)"
                        print(f"❌ [AstrologyAPI ({idx}/{total_eps})] {key_name} -> [429]: {err_msg}", flush=True)
                        results["failures"].append({"endpoint": key_name, "error": err_msg})
                        results["data"][key_name] = {"error": err_msg}
                        results["endpoint_audits"].append({
                            "endpoint": key_name,
                            "status": "FAILED",
                            "http_status": 429,
                            "latency_ms": lat,
                            "error": err_msg
                        })
                        break
                    elif resp.status_code == 402:
                        err_msg = "Payment Required / Monthly Quota Exceeded (402)"
                        print(f"❌ [AstrologyAPI ({idx}/{total_eps})] {key_name} -> [402]: {err_msg}", flush=True)
                        results["failures"].append({"endpoint": key_name, "error": err_msg})
                        results["data"][key_name] = {"error": err_msg}
                        results["endpoint_audits"].append({
                            "endpoint": key_name,
                            "status": "FAILED",
                            "http_status": 402,
                            "latency_ms": lat,
                            "error": err_msg
                        })
                        break
                    else:
                        err_msg = f"HTTP {resp.status_code}: {resp.text[:200]}"
                        print(f"❌ [AstrologyAPI ({idx}/{total_eps})] {key_name} -> [HTTP {resp.status_code}]: {err_msg}", flush=True)
                        results["failures"].append({"endpoint": key_name, "error": err_msg})
                        results["data"][key_name] = {"error": err_msg}
                        results["endpoint_audits"].append({
                            "endpoint": key_name,
                            "status": "FAILED",
                            "http_status": resp.status_code,
                            "latency_ms": lat,
                            "error": err_msg
                        })
                        break
                except Exception as exc:
                    lat = (time.perf_counter() - t0) * 1000.0
                    err_msg = f"Exception: {type(exc).__name__} - {str(exc)}"
                    print(f"❌ [AstrologyAPI ({idx}/{total_eps})] {key_name} -> [EXC]: {err_msg}", flush=True)
                    results["failures"].append({"endpoint": key_name, "error": err_msg})
                    results["data"][key_name] = {"error": err_msg}
                    results["endpoint_audits"].append({
                        "endpoint": key_name,
                        "status": "FAILED",
                        "http_status": 500,
                        "latency_ms": lat,
                        "error": err_msg
                    })
                    break

        if results["failures"]:
            results["status"] = "FAILED" if len(results["failures"]) == len(endpoints) else "PARTIAL"
        else:
            results["status"] = "SUCCESS"

    finally:
        if close_client:
            await client.aclose()

    return results


def main():
    parser = argparse.ArgumentParser(description="Astrology-API.io Extractor v2.0")
    parser.add_argument("--client-file", type=str, help="Path to client JSON file")
    parser.add_argument("--output", type=str, help="Path to write output JSON")
    parser.add_argument("--mode", type=str, choices=["free-tier", "all"], default="free-tier",
                        help="Execution mode: 'free-tier' (24 calls, protects 50/mo limit) or 'all' (240+ calls)")
    args = parser.parse_args()

    client_data = {
        "year": 1986, "month": 1, "day": 18,
        "hour": 3, "minute": 0,
        "lat": 6.2340437, "lng": -75.5731248,
        "tz_str": "America/Bogota",
        "name": "Consultant"
    }

    if args.client_file and Path(args.client_file).exists():
        p = Path(args.client_file)
        if p.suffix.lower() == ".json":
            client_data = json.loads(p.read_text(encoding="utf-8"))

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(extract_astrologyapi(client_data, mode=args.mode))

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Extraction saved to {args.output}")
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
