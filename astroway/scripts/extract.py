#!/usr/bin/env python3
"""
Autonomous Extractor for AstroWay REST Engine (v2.2)
Extracts Western, Vedic, BaZi, Human Design, Astrocartography, Modern Psychology, and Dashas.
Captures real-time credit audit headers (X-Credits-Remaining, X-Credits-Used, X-Credits-Limit).
"""

import argparse
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional
import httpx

BASE_URL = os.getenv("ASTROWAY_URL", "https://api.astroway.info")
DEFAULT_TIMEOUT = 12.0


async def extract_astroway(
    client_data: Dict[str, Any],
    api_key: Optional[str] = None,
    client: Optional[httpx.AsyncClient] = None
) -> Dict[str, Any]:
    """
    Executes full high-precision Swiss Ephemeris AstroWay extraction across all domains.
    """
    key = api_key or os.getenv("ASTROWAY_API_KEY") or os.getenv("astroway_apiKey")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if key:
        headers["X-Api-Key"] = key

    year = int(client_data.get("year", 1990))
    month = int(client_data.get("month", 1))
    day = int(client_data.get("day", 1))
    hour = int(client_data.get("hour", 12))
    minute = int(client_data.get("minute", 0))
    lat = float(client_data.get("lat", 0.0))
    lng = float(client_data.get("lng", 0.0))
    tz_offset = float(client_data.get("tz_offset", -5.0))

    date_str = f"{year:04d}-{month:02d}-{day:02d}"
    time_str = f"{hour:02d}:{minute:02d}:00"

    base_payload = {
        "date": date_str,
        "time": time_str,
        "timezoneOffset": tz_offset,
        "latitude": lat,
        "longitude": lng,
        "houseSystem": "P",
        "zodiacType": "tropical"
    }

    fc_payload = {
        "date": date_str,
        "time": time_str,
        "timezoneOffset": tz_offset,
        "latitude": lat,
        "longitude": lng,
        "houseSystem": "C",
        "zodiacType": "sidereal",
        "ayanamsa": "fagan-bradley"
    }

    endpoints = [
        # Western Natal
        ("western_chart", f"{BASE_URL}/v1/chart", base_payload),
        ("western_chart_fagan_campanus", f"{BASE_URL}/v1/chart", fc_payload),
        # Vedic & Jaimini
        ("jaimini_chara_karakas", f"{BASE_URL}/v1/vedic/jaimini/chara-karakas", base_payload),
        ("vedic_varga_d9", f"{BASE_URL}/v1/vedic/varga/d9", base_payload),
        ("vedic_varga_d10", f"{BASE_URL}/v1/vedic/varga/d10", base_payload),
        ("vedic_shadbala_full", f"{BASE_URL}/v1/vedic/shadbala/full", base_payload),
        ("vedic_dashas_maha", f"{BASE_URL}/v1/vedic/dashas/vimshottari/maha", base_payload),
        # Evolutionary & Nodal
        ("evolutionary_skipped_steps", f"{BASE_URL}/v1/evolutionary/skipped-steps", base_payload),
        ("evolutionary_nodal_axis", f"{BASE_URL}/v1/evolutionary/nodal-axis-detail", base_payload),
        # Human Design & Cosmobiology
        ("human_design", f"{BASE_URL}/v1/human-design", base_payload),
        ("hd_circuitry", f"{BASE_URL}/v1/hd/circuitry", base_payload),
        ("hd_incarnation_cross", f"{BASE_URL}/v1/hd/incarnation-cross", base_payload),
        ("hd_sensitivity", f"{BASE_URL}/v1/hd/sensitivity", base_payload),
        ("cosmobiology_dial90", f"{BASE_URL}/v1/cosmobiology/dial-90", base_payload),
        # Astrocartography & Relocation
        ("geo_acg", f"{BASE_URL}/v1/acg", base_payload),
        ("geo_acg_best_places", f"{BASE_URL}/v1/acg/best-places", {**base_payload, "category": "career"}),
        ("geo_local_space", f"{BASE_URL}/v1/local-space", base_payload),
        # Modern Psychological Astrology (Arroyo, Greene, Rudhyar)
        ("psychological_arroyo_elements", f"{BASE_URL}/v1/modern/arroyo/element-integration", base_payload),
        ("psychological_greene_archetypes", f"{BASE_URL}/v1/modern/greene/archetypal-figures", base_payload),
        ("psychological_greene_shadow", f"{BASE_URL}/v1/modern/greene/saturn-shadow", base_payload),
        ("psychological_rudhyar_lunation", f"{BASE_URL}/v1/modern/rudhyar/lunation-phase", base_payload),
    ]

    results: Dict[str, Any] = {
        "provider": "astroway",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "SUCCESS",
        "plan": "Indie PRO ($5/mo, 50k credits/mo)",
        "credits_audit": {
            "remaining": None,
            "used_last_call": None,
            "limit": 50000
        },
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
        for key_name, url, body in endpoints:
            try:
                await asyncio.sleep(0.35)
                resp = await client.post(url, headers=headers, json=body)
                results["calls_made"] += 1

                if resp.status_code == 429:
                    wait_sec = 6.0
                    try:
                        err_data = resp.json()
                        m_wait = re.search(r"(\d+)\s*s", str(err_data))
                        if m_wait:
                            wait_sec = float(m_wait.group(1)) + 0.5
                    except Exception:
                        pass
                    await asyncio.sleep(wait_sec)
                    resp = await client.post(url, headers=headers, json=body)
                    results["calls_made"] += 1

                # Capture real-time credit audit headers
                rem = resp.headers.get("X-Credits-Remaining")
                used = resp.headers.get("X-Credits-Used")
                lim = resp.headers.get("X-Credits-Limit")
                if rem is not None:
                    try: results["credits_audit"]["remaining"] = int(rem)
                    except ValueError: results["credits_audit"]["remaining"] = rem
                if used is not None:
                    try: results["credits_audit"]["used_last_call"] = int(used)
                    except ValueError: results["credits_audit"]["used_last_call"] = used
                if lim is not None:
                    try: results["credits_audit"]["limit"] = int(lim)
                    except ValueError: results["credits_audit"]["limit"] = lim

                if resp.status_code == 200:
                    data = resp.json()
                    results["raw_responses"][key_name] = data
                    
                    if isinstance(data, dict):
                        if data.get("ok") is False or "error" in data:
                            err_msg = data.get("error", "API returned ok=False")
                            results["failures"].append({"endpoint": key_name, "error": err_msg})
                            results["data"][key_name] = {"error": err_msg}
                        else:
                            results["data"][key_name] = data
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
            results["status"] = "FAILED" if len(results["failures"]) == len(endpoints) else "PARTIAL"
        else:
            results["status"] = "SUCCESS"

    finally:
        if close_client:
            await client.aclose()

    return results


def main():
    parser = argparse.ArgumentParser(description="AstroWay Extractor")
    parser.add_argument("--client-file", type=str, help="Path to client JSON file")
    parser.add_argument("--output", type=str, help="Path to write output JSON")
    args = parser.parse_args()

    client_data = {
        "year": 1986, "month": 1, "day": 18,
        "hour": 3, "minute": 0,
        "lat": 6.2340437, "lng": -75.5731248,
        "tz_offset": -5.0
    }

    if args.client_file and Path(args.client_file).exists():
        p = Path(args.client_file)
        if p.suffix.lower() == ".json":
            client_data = json.loads(p.read_text(encoding="utf-8"))

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(extract_astroway(client_data))

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Extraction saved to {args.output}")
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
