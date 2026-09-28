#!/usr/bin/env python3
"""
Autonomous Extractor for Astrology-API.io (V3 API)
Extracts Hellenistic timing timeline, core numerology, and natal/vedic charts.
Enforces nested subject.birth_data schema and rate limit pacing (anti-429).
"""

import argparse
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, Optional
import httpx

BASE_URL = os.getenv("ASTROLOGY_API_URL", "https://api.astrology-api.io/api/v3")
DEFAULT_TIMEOUT = 12.0


async def extract_astrologyapi(
    client_data: Dict[str, Any],
    api_key: Optional[str] = None,
    client: Optional[httpx.AsyncClient] = None
) -> Dict[str, Any]:
    """
    Extracts Hellenistic timing timeline and core numerology with rate pacing.
    """
    key = api_key or os.getenv("ASTROLOGY_API_IO") or os.getenv("ASTROLOGY_API_KEY") or os.getenv("astrology_apiKey")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if key:
        headers["Authorization"] = f"Bearer {key}"

    full_name = client_data.get("name", "Consultant")
    pref_name = client_data.get("preferred_name", full_name)
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

    payload_timeline = {
        "subject": {
            "name": full_name,
            "birth_data": birth_data_obj
        },
        "target_date": today_str
    }

    payload_numerology = {
        "subject": {
            "name": full_name,
            "preferred_name": pref_name,
            "birth_data": birth_data_obj
        }
    }

    endpoints = [
        ("timing_timeline", f"{BASE_URL}/timing/timeline", payload_timeline),
        ("core_numerology", f"{BASE_URL}/numerology/core-numbers", payload_numerology),
    ]

    results: Dict[str, Any] = {
        "provider": "astrologyapi",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "SUCCESS",
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
        for idx, (key_name, url, body) in enumerate(endpoints):
            if idx > 0:
                # Polite pacing to respect free-tier rate limits and prevent 429
                await asyncio.sleep(1.2)

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
    parser = argparse.ArgumentParser(description="Astrology-API.io Extractor")
    parser.add_argument("--client-file", type=str, help="Path to client JSON file")
    parser.add_argument("--output", type=str, help="Path to write output JSON")
    args = parser.parse_args()

    client_data = {
        "name": "Laura Catalina Tamayo Perez",
        "preferred_name": "Catalina",
        "year": 1986, "month": 1, "day": 18,
        "hour": 3, "minute": 0,
        "lat": 6.2340437, "lng": -75.5731248,
        "tz_str": "America/Bogota"
    }

    if args.client_file and Path(args.client_file).exists():
        p = Path(args.client_file)
        if p.suffix.lower() == ".json":
            client_data = json.loads(p.read_text(encoding="utf-8"))

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(extract_astrologyapi(client_data))

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Extraction saved to {args.output}")
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
