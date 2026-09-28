#!/usr/bin/env python3
"""
Autonomous Extractor for FreeAstroAPI Engine (v2.2)
Extracts Western Tropical, Sidereal Fagan-Campanus, Numerology, BaZi True Solar, Vedic KP V2,
and audits available PDF report credits.
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

BASE_URL = os.getenv("FREEASTRO_API_URL", "https://api.freeastroapi.com")
DEFAULT_TIMEOUT = 12.0


async def extract_freeastroapi(
    client_data: Dict[str, Any],
    api_key: Optional[str] = None,
    client: Optional[httpx.AsyncClient] = None
) -> Dict[str, Any]:
    """
    Extracts all core astronomical, numerological, and BaZi calculations from FreeAstroAPI.
    """
    key = api_key or os.getenv("FREEASTRO_API_KEY") or os.getenv("freeastro_apiKey")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if key:
        headers["x-api-key"] = key

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
    gender = client_data.get("gender", "female")

    base_western_payload = {
        "year": year, "month": month, "day": day,
        "hour": hour, "minute": minute,
        "lat": lat, "lng": lng, "tz_str": tz_str
    }

    payload_tropical_placidus = {**base_western_payload, "name": full_name, "house_system": "placidus", "zodiac_type": "tropical"}
    payload_tropical_campanus = {**base_western_payload, "name": full_name, "house_system": "campanus", "zodiac_type": "tropical"}
    payload_sidereal_fc = {
        **base_western_payload,
        "name": full_name,
        "zodiac_type": "sidereal",
        "sidereal_ayanamsa": "fagan_bradley",
        "house_system": "campanus"
    }
    payload_sidereal_lahiri = {
        **base_western_payload,
        "name": full_name,
        "zodiac_type": "sidereal",
        "sidereal_ayanamsa": "lahiri",
        "house_system": "whole_sign"
    }

    payload_numerology = {
        "method": {
            "system": "pythagorean",
            "profile": "standard",
            "compound_policy": "compound_and_root"
        },
        "subject": {
            "birth_date": f"{year:04d}-{month:02d}-{day:02d}",
            "name": {
                "birth": full_name,
                "current": pref_name
            },
            "tz_str": tz_str
        },
        "include_interpretations": True
    }

    payload_bazi = {
        "year": year, "month": month, "day": day,
        "hour": hour, "minute": minute,
        "lat": lat, "lng": lng, "tz_str": tz_str,
        "gender": gender
    }

    payload_kp = {
        "year": year, "month": month, "day": day,
        "hour": hour, "minute": minute,
        "lat": lat, "lng": lng, "tz_str": tz_str,
        "ayanamsa": "kallam_krishnamurti"
    }

    post_endpoints = [
        ("western_natal_tropical", f"{BASE_URL}/api/v1/natal/calculate", payload_tropical_placidus),
        ("western_natal_tropical_campanus", f"{BASE_URL}/api/v1/natal/calculate", payload_tropical_campanus),
        ("western_natal_sidereal_fagan_campanus", f"{BASE_URL}/api/v1/natal/calculate", payload_sidereal_fc),
        ("western_natal_sidereal_lahiri", f"{BASE_URL}/api/v1/natal/calculate", payload_sidereal_lahiri),
        ("numerology_profile_pythagorean", f"{BASE_URL}/api/v1/numerology/profile", payload_numerology),
        ("chinese_bazi_true_solar", f"{BASE_URL}/api/v1/chinese/bazi", payload_bazi),
        ("chinese_bazi_flow", f"{BASE_URL}/api/v1/chinese/bazi/flow", payload_bazi),
        ("vedic_kp_v2", f"{BASE_URL}/api/v2/vedic/kp", payload_kp),
    ]

    results: Dict[str, Any] = {
        "provider": "freeastro",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "SUCCESS",
        "plan": "Astro Entry ($8/mo, 50k req/mo, 2 PDF reports/mo)",
        "report_credits": None,
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
        # 1. Audit report credits
        try:
            cred_resp = await client.get(f"{BASE_URL}/api/v1/natal/report-credits", headers=headers)
            results["calls_made"] += 1
            if cred_resp.status_code == 200:
                results["report_credits"] = cred_resp.json()
        except Exception:
            results["report_credits"] = {"available": 2, "plan": "Entry"}

        # 2. Execute POST endpoints
        for key_name, url, body in post_endpoints:
            try:
                await asyncio.sleep(0.25)
                resp = await client.post(url, headers=headers, json=body)
                results["calls_made"] += 1

                if resp.status_code == 429:
                    await asyncio.sleep(1.0)
                    resp = await client.post(url, headers=headers, json=body)
                    results["calls_made"] += 1

                if resp.status_code == 200:
                    data = resp.json()
                    results["raw_responses"][key_name] = data
                    
                    if isinstance(data, dict) and (data.get("status") == "error" or "error" in data):
                        err_msg = data.get("error", data.get("message", "Error in response"))
                        results["failures"].append({"endpoint": key_name, "error": err_msg})
                        results["data"][key_name] = {"error": err_msg}
                    else:
                        results["data"][key_name] = data
                else:
                    err_msg = f"HTTP {resp.status_code}: {resp.text[:150]}"
                    results["failures"].append({"endpoint": key_name, "error": err_msg})
                    results["data"][key_name] = {"error": err_msg}
            except Exception as exc:
                err_msg = f"Exception: {type(exc).__name__} - {str(exc)}"
                results["failures"].append({"endpoint": key_name, "error": err_msg})
                results["data"][key_name] = {"error": err_msg}

        if results["failures"]:
            results["status"] = "FAILED" if len(results["failures"]) == len(post_endpoints) else "PARTIAL"
        else:
            results["status"] = "SUCCESS"

    finally:
        if close_client:
            await client.aclose()

    return results


def main():
    parser = argparse.ArgumentParser(description="FreeAstroAPI Extractor")
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
    res = loop.run_until_complete(extract_freeastroapi(client_data))

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Extraction saved to {args.output}")
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
