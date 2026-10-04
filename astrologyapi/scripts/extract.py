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
    Curated suite of 24 high-value exclusive endpoints that do not duplicate
    other APIs and fit comfortably within the 50 free monthly credits.
    """
    return [
        ("kabbalah_birth_angels", "/kabbalah/birth-angels"),
        ("kabbalah_tikkun", "/kabbalah/tikkun"),
        ("kabbalah_tree_of_life", "/kabbalah/tree-of-life-chart"),
        ("kabbalah_sephirot_activation", "/kabbalah/sephirot-activation"),
        ("traditional_almuten", "/traditional/almuten"),
        ("traditional_analysis", "/traditional/analysis"),
        ("traditional_temperament", "/traditional/temperament"),
        ("traditional_hyleg", "/traditional/hyleg"),
        ("timing_timeline", "/timing/timeline"),
        ("timing_annual_profections", "/timing/annual-profections"),
        ("timing_firdaria", "/timing/firdaria"),
        ("data_positions_enhanced", "/data/positions/enhanced"),
        ("fixed_stars_conjunctions", "/fixed-stars/conjunctions"),
        ("fixed_stars_paranatellonta", "/fixed-stars/paranatellonta"),
        ("numerology_comprehensive", "/numerology/comprehensive"),
        ("numerology_life_cycles", "/numerology/life-cycles"),
        ("analysis_vocational", "/analysis/vocational"),
        ("analysis_wealth", "/analysis/wealth"),
        ("analysis_psychological", "/analysis/psychological"),
        ("insights_karmic", "/insights/karmic"),
        ("insights_shadow", "/insights/shadow"),
        ("insights_life_purpose", "/insights/life-purpose"),
        ("charts_draconic", "/charts/draconic"),
        ("charts_heliocentric", "/charts/heliocentric"),
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
    mode: str = "free-tier"
) -> Dict[str, Any]:
    """
    Extracts calculations from Astrology-API.io.
    mode='free-tier' restricts to 24 curated endpoints to protect the 50 free credits limit.
    mode='all' executes the full 240+ endpoint catalog.
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
        "failures": []
    }

    close_client = False
    if client is None:
        client = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT, follow_redirects=True)
        close_client = True

    try:
        for idx, (key_name, path, body) in enumerate(endpoints):
            url = f"{BASE_URL}{path}" if path.startswith("/") else f"{BASE_URL}/{path}"
            if idx > 0:
                # Polite pacing to respect rate limits and avoid 429
                await asyncio.sleep(1.0)

            for attempt in range(2):
                try:
                    resp = await client.post(url, headers=headers, json=body)
                    results["calls_made"] += 1

                    if resp.status_code == 200:
                        data = resp.json()
                        results["raw_responses"][key_name] = data

                        # Check semantic error in body
                        if isinstance(data, dict) and "detail" in data:
                            err_msg = str(data.get("detail"))
                            results["failures"].append({"endpoint": key_name, "error": err_msg})
                            results["data"][key_name] = {"error": err_msg}
                        else:
                            results["data"][key_name] = data.get("data", data)
                        break
                    elif resp.status_code == 429:
                        if attempt == 0:
                            await asyncio.sleep(3.0)
                            continue
                        err_msg = "Rate limit exceeded (429)"
                        results["failures"].append({"endpoint": key_name, "error": err_msg})
                        results["data"][key_name] = {"error": err_msg}
                        break
                    elif resp.status_code == 402:
                        err_msg = "Payment Required / Monthly Quota Exceeded (402)"
                        results["failures"].append({"endpoint": key_name, "error": err_msg})
                        results["data"][key_name] = {"error": err_msg}
                        break
                    else:
                        err_msg = f"HTTP {resp.status_code}: {resp.text[:200]}"
                        results["failures"].append({"endpoint": key_name, "error": err_msg})
                        results["data"][key_name] = {"error": err_msg}
                        break
                except Exception as exc:
                    err_msg = f"Exception: {type(exc).__name__} - {str(exc)}"
                    results["failures"].append({"endpoint": key_name, "error": err_msg})
                    results["data"][key_name] = {"error": err_msg}
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
        "name": "Catalina"
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
