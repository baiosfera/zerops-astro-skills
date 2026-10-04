#!/usr/bin/env python3
"""
Autonomous Universal Extractor for AstroWay REST Engine (v2.1)
Extracts the complete universe of Swiss Ephemeris AstroWay calculations (540+ endpoints)
across Western Natal, Harmonics, Draconic, Heliocentric, 16 Vedic Vargas (D1 to D60),
Dashas, Shadbala, Jaimini, Lal Kitab, Human Design, Chinese BaZi, Zi Wei Dou Shu,
Business & Financial Archetypes, Hellenistic Astrology, Cosmobiology, Astromapping,
and Modern Psychological & Numerology profiles.
Captures real-time credit audit headers (X-Credits-Remaining, X-Credits-Used, X-Credits-Limit).
PDF Reports are 100% discarded by default; optional activation via --include-pdf.
"""

import argparse
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple
import httpx

BASE_URL = os.getenv("ASTROWAY_URL", "https://api.astroway.info")
DEFAULT_TIMEOUT = 16.0


def resolve_astroway_payload(
    path: str,
    ref: str,
    base_payload: Dict[str, Any],
    fc_payload: Dict[str, Any],
    bazi_base_payload: Dict[str, Any],
    bazi_luck_payload: Dict[str, Any],
    ziwei_payload: Dict[str, Any],
    ziwei_sihua_payload: Dict[str, Any],
    dial90_payload: Dict[str, Any],
    date_str: str,
    time_str: str,
    name: str,
    gender: str,
    today_str: str,
    target_age: int,
    lat: float,
    lng: float,
    current_year: int
) -> Dict[str, Any]:
    """
    Constructs the exact schema-compliant payload for any AstroWay endpoint,
    fixing composite relocation, targetDate, targetAge, and specialized inputs.
    """
    # 1. Composite Relocation Chart
    if path in ("/relocation", "/v1/relocation"):
        return {
            "natal": base_payload,
            "target": {**base_payload, "latitude": lat, "longitude": lng}
        }

    # 2. Hellenistic Profections & Time Lords
    if "profections" in path:
        return {
            **base_payload,
            "targetDate": today_str,
            "targetAge": target_age
        }
    if "time-lord-stack" in path:
        return {
            **base_payload,
            "targetAge": target_age
        }

    # 3. Zodiacal Releasing
    if "zodiacal-releasing" in path or "zr-" in path:
        return {
            **base_payload,
            "years": 80
        }

    # 4. Chinese BaZi
    if "/bazi" in path or "bazi" in path:
        if "luck" in path or ref == "BaziLuckInput":
            return bazi_luck_payload
        return bazi_base_payload

    # 5. Chinese Zi Wei Dou Shu
    if "/ziwei" in path or "ziwei" in path:
        if "transformations" in path or "sihua" in path:
            return ziwei_sihua_payload
        return ziwei_payload

    # 6. Cosmobiology & Hamburg School
    if "cosmobiology" in path or "midpoint" in path or "dial-90" in path or ref == "ChartWithTnp":
        return dial90_payload

    # 7. Astromapping & Local Space
    if "acg/best-places" in path:
        return {
            **base_payload,
            "category": "career"
        }

    # 8. Harmonics
    if "harmonics" in path or ref == "HarmonicInput":
        return {"harmonic": 9, **base_payload}

    # 9. Esoteric & Mayan
    if "destiny-matrix" in path or "mayan" in path:
        return {"date": date_str}

    # 10. Numerology
    if "numerology" in path:
        return {
            "name": name,
            "date": date_str,
            "targetYear": current_year
        }

    # 11. Kabbalah Gematria
    if "gematria" in path:
        return {"text": name}

    # 12. Dasha Inputs
    if ref == "DashaInput" or "/dashas/" in path:
        return {
            **base_payload,
            "level": 3,
            "dashaSystem": "vimshottari"
        }

    # Default: Standard Tropical Placidus ChartInput
    return base_payload


def load_natal_catalog(use_curated: bool = True) -> List[Tuple[str, str, str]]:
    """
    Loads curated high-value natal endpoints catalog by default (118 endpoints for oraculo-diag-*),
    falling back to full catalog if use_curated is False.
    """
    assets_dir = Path(__file__).parent.parent / "assets"
    if use_curated:
        curated_path = assets_dir / "curated_natal_catalog.json"
        if curated_path.exists():
            try:
                raw = json.loads(curated_path.read_text(encoding="utf-8"))
                if isinstance(raw, list) and raw:
                    return [(item[0], item[1], item[2] if len(item) > 2 else "") for item in raw]
            except Exception:
                pass

    catalog_path = assets_dir / "natal_endpoints_catalog.json"
    if catalog_path.exists():
        try:
            raw = json.loads(catalog_path.read_text(encoding="utf-8"))
            if isinstance(raw, list) and raw:
                return [(item[0], item[1], item[2] if len(item) > 2 else "") for item in raw]
        except Exception:
            pass

    # Built-in robust 128-endpoint catalog fallback
    standard_paths = [
        ("/chart", "ChartInput", "Western Natal Tropical"),
        ("/draconic", "ChartInput", "Draconic Chart"),
        ("/heliocentric", "ChartInput", "Heliocentric Chart"),
        ("/harmonics", "HarmonicInput", "Harmonics H9"),
        ("/relocation", "RelocationInput", "Relocated Chart"),
        ("/almuten", "ChartInput", "Almuten Figuris"),
        ("/arabic-parts", "ChartInput", "Arabic Parts"),
        ("/essential-dignities", "ChartInput", "Essential Dignities"),
        ("/fixed-stars", "ChartInput", "Fixed Stars"),
        ("/profections", "ChartInput", "Profections"),
        ("/vedic/varga/D1", "ChartInput", "Rasi D1"),
        ("/vedic/varga/D9", "ChartInput", "Navamsa D9"),
        ("/vedic/varga/D10", "ChartInput", "Dasamsa D10"),
        ("/vedic/shadbala/full", "ChartInput", "Shadbala Full"),
        ("/vedic/dashas/vimshottari/maha", "ChartInput", "Vimshottari Maha"),
        ("/bazi/four-pillars", "BaziChartInput", "BaZi Four Pillars"),
        ("/ziwei/twelve-palaces", "ZiweiDateInput", "Zi Wei Twelve Palaces"),
        ("/human-design", "ChartInput", "Human Design BodyGraph"),
        ("/acg", "ChartInput", "Astrocartography"),
        ("/cosmobiology/dial-90", "ChartWithTnp", "90 Degree Dial")
    ]
    return standard_paths


async def extract_astroway(
    client_data: Dict[str, Any],
    api_key: Optional[str] = None,
    client: Optional[httpx.AsyncClient] = None,
    include_pdf: Optional[List[str]] = None,
    max_endpoints: int = 0,
    cache_manager: Optional[Any] = None,
    client_hash: Optional[str] = None,
    use_curated: bool = True
) -> Dict[str, Any]:
    """
    Executes universal high-precision Swiss Ephemeris AstroWay extraction across all domains.
    Discards PDF reports by default; allows optional download only if requested.
    """
    key = api_key or os.getenv("ASTROWAY_API_KEY") or os.getenv("astroway_apiKey")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    if key:
        headers["X-Api-Key"] = key

    name = client_data.get("preferred_name") or client_data.get("name") or "Consultant"
    gender = client_data.get("gender", "female")
    year = int(client_data.get("year", 1990))
    month = int(client_data.get("month", 1))
    day = int(client_data.get("day", 1))
    hour = int(client_data.get("hour", 12))
    minute = int(client_data.get("minute", 0))
    lat = float(client_data.get("lat", 0.0))
    lng = float(client_data.get("lng", 0.0))
    tz_offset = float(client_data.get("tz_offset", -5.0))
    city = client_data.get("city", "Unknown")

    date_str = f"{year:04d}-{month:02d}-{day:02d}"
    time_str = f"{hour:02d}:{minute:02d}:00"
    now_utc = datetime.now(timezone.utc)
    today_str = now_utc.strftime("%Y-%m-%d")
    current_year = now_utc.year
    target_age = max(1, current_year - year)

    # Base Payload (Standard Tropical Placidus)
    base_payload = {
        "date": date_str,
        "time": time_str,
        "timezoneOffset": tz_offset,
        "latitude": lat,
        "longitude": lng,
        "houseSystem": "P",
        "zodiacType": "tropical"
    }

    # Sidereal Fagan-Bradley Campanus Payload
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

    # BaZi Payloads
    bazi_base_payload = {
        "date": date_str,
        "time": time_str,
        "timezoneOffset": tz_offset,
        "language": "en"
    }
    bazi_luck_payload = {
        "date": date_str,
        "time": time_str,
        "timezoneOffset": tz_offset,
        "gender": gender,
        "count": 10,
        "language": "en"
    }

    # Zi Wei Dou Shu Payloads
    ziwei_payload = {
        "date": date_str,
        "time": time_str,
        "timezoneOffset": tz_offset,
        "gender": gender
    }
    ziwei_sihua_payload = {
        "date": date_str,
        "time": time_str,
        "timezoneOffset": tz_offset
    }

    # Cosmobiology Payloads
    dial90_payload = {
        **base_payload,
        "withTnp": True
    }

    # Load universal catalog (curated high-value by default)
    catalog = load_natal_catalog(use_curated=use_curated)
    if max_endpoints > 0:
        catalog = catalog[:max_endpoints]

    endpoints: List[Tuple[str, str, Dict[str, Any]]] = []
    for path, ref, summary in catalog:
        clean_path = path if path.startswith("/") else f"/{path}"
        key_name = clean_path.strip("/").replace("/", "_").replace("-", "_")
        body = resolve_astroway_payload(
            path=clean_path,
            ref=ref,
            base_payload=base_payload,
            fc_payload=fc_payload,
            bazi_base_payload=bazi_base_payload,
            bazi_luck_payload=bazi_luck_payload,
            ziwei_payload=ziwei_payload,
            ziwei_sihua_payload=ziwei_sihua_payload,
            dial90_payload=dial90_payload,
            date_str=date_str,
            time_str=time_str,
            name=name,
            gender=gender,
            today_str=today_str,
            target_age=target_age,
            lat=lat,
            lng=lng,
            current_year=current_year
        )
        endpoints.append((key_name, clean_path, body))

    # Optional PDF report activation
    if include_pdf:
        pdf_options = {
            "natal": "/reports/natal",
            "business": "/reports/business",
            "career": "/reports/career",
            "money": "/reports/money",
            "human_design": "/reports/human-design",
            "relocation": "/reports/relocation"
        }
        for slug in include_pdf:
            clean_slug = slug.strip().lower()
            if clean_slug in pdf_options:
                endpoints.append((f"pdf_report_{clean_slug}", pdf_options[clean_slug], base_payload))

    results: Dict[str, Any] = {
        "provider": "astroway",
        "timestamp": now_utc.isoformat(),
        "status": "SUCCESS",
        "plan": "Indie PRO ($5/mo, 50k credits/mo)",
        "credits_audit": {
            "remaining": None,
            "used_last_call": None,
            "total_spent_this_run": 0,
            "limit": 50000
        },
        "calls_made": 0,
        "cache_hits": 0,
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
            # 1. Delta Cache Check: Skip if already extracted with HTTP 200
            if cache_manager and client_hash:
                if cache_manager.has_endpoint("astroway", key_name, client_hash):
                    cached_val = cache_manager.get_endpoint("astroway", key_name, client_hash)
                    results["data"][key_name] = cached_val
                    results["cache_hits"] = results.get("cache_hits", 0) + 1
                    print(f"⚡ [AstroWay ({idx}/{total_eps})] {key_name} -> [CACHED / SKIP]", flush=True)
                    results["endpoint_audits"].append({
                        "endpoint": key_name,
                        "url": path,
                        "status": "CACHED",
                        "http_status": 200,
                        "latency_ms": 0.0,
                        "credits_used": 0
                    })
                    continue

            url = f"{BASE_URL}/v1{path}" if not path.startswith("/v1") else f"{BASE_URL}{path}"
            t_start = time.perf_counter()
            try:
                # Rate limit pacing: 0.35s between requests to respect Indie PRO limits
                await asyncio.sleep(0.35)
                resp = await client.post(url, headers=headers, json=body)
                results["calls_made"] += 1

                # Adaptive backoff on 429
                if resp.status_code == 429:
                    wait_sec = 6.0
                    try:
                        err_data = resp.json()
                        m_wait = re.search(r"(\d+)\s*s", str(err_data))
                        if m_wait:
                            wait_sec = float(m_wait.group(1)) + 1.0
                    except Exception:
                        pass
                    print(f"⏳ [AstroWay ({idx}/{total_eps})] 429 Rate Limit hit. Backing off {wait_sec}s...", flush=True)
                    await asyncio.sleep(wait_sec)
                    resp = await client.post(url, headers=headers, json=body)
                    results["calls_made"] += 1

                latency_ms = (time.perf_counter() - t_start) * 1000.0

                # Capture real-time credit audit headers
                rem = resp.headers.get("X-Credits-Remaining")
                used = resp.headers.get("X-Credits-Used")
                lim = resp.headers.get("X-Credits-Limit")
                credits_used_call = 0
                if rem is not None:
                    try: results["credits_audit"]["remaining"] = int(rem)
                    except ValueError: results["credits_audit"]["remaining"] = rem
                if used is not None:
                    try:
                        credits_used_call = int(used)
                        results["credits_audit"]["used_last_call"] = credits_used_call
                        results["credits_audit"]["total_spent_this_run"] += credits_used_call
                    except ValueError:
                        results["credits_audit"]["used_last_call"] = used
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
                            print(f"⚠️  [AstroWay ({idx}/{total_eps})] {key_name} -> [FAIL ok=False] ({round(latency_ms, 1)}ms): {err_msg}", flush=True)
                            results["endpoint_audits"].append({
                                "endpoint": key_name,
                                "url": path,
                                "status": "FAILED",
                                "http_status": 200,
                                "latency_ms": round(latency_ms, 2),
                                "credits_used": credits_used_call,
                                "error": err_msg
                            })
                        else:
                            results["data"][key_name] = data
                            if cache_manager and client_hash:
                                cache_manager.set_endpoint("astroway", key_name, client_hash, data, http_status=200)
                            rem_str = f" | Restan: {results['credits_audit']['remaining']}" if results['credits_audit']['remaining'] is not None else ""
                            print(f"✨ [AstroWay ({idx}/{total_eps})] {key_name} -> [200 OK] ({round(latency_ms, 1)}ms){rem_str}", flush=True)
                            results["endpoint_audits"].append({
                                "endpoint": key_name,
                                "url": path,
                                "status": "SUCCESS",
                                "http_status": 200,
                                "latency_ms": round(latency_ms, 2),
                                "credits_used": credits_used_call
                            })
                    else:
                        results["data"][key_name] = data
                        if cache_manager and client_hash:
                            cache_manager.set_endpoint("astroway", key_name, client_hash, data, http_status=200)
                        rem_str = f" | Restan: {results['credits_audit']['remaining']}" if results['credits_audit']['remaining'] is not None else ""
                        print(f"✨ [AstroWay ({idx}/{total_eps})] {key_name} -> [200 OK] ({round(latency_ms, 1)}ms){rem_str}", flush=True)
                        results["endpoint_audits"].append({
                            "endpoint": key_name,
                            "url": path,
                            "status": "SUCCESS",
                            "http_status": 200,
                            "latency_ms": round(latency_ms, 2),
                            "credits_used": credits_used_call
                        })
                else:
                    err_msg = f"HTTP {resp.status_code}: {resp.text[:200]}"
                    results["failures"].append({"endpoint": key_name, "error": err_msg})
                    results["data"][key_name] = {"error": err_msg}
                    print(f"❌ [AstroWay ({idx}/{total_eps})] {key_name} -> [HTTP {resp.status_code}] ({round(latency_ms, 1)}ms): {err_msg[:60]}", flush=True)
                    results["endpoint_audits"].append({
                        "endpoint": key_name,
                        "url": path,
                        "status": "FAILED",
                        "http_status": resp.status_code,
                        "latency_ms": round(latency_ms, 2),
                        "credits_used": credits_used_call,
                        "error": err_msg
                    })
            except Exception as exc:
                latency_ms = (time.perf_counter() - t_start) * 1000.0
                err_msg = f"Exception: {type(exc).__name__} - {str(exc)}"
                results["failures"].append({"endpoint": key_name, "error": err_msg})
                results["data"][key_name] = {"error": err_msg}
                print(f"💥 [AstroWay ({idx}/{total_eps})] {key_name} -> [EXC]: {err_msg[:60]}", flush=True)
                results["endpoint_audits"].append({
                    "endpoint": key_name,
                    "url": path,
                    "status": "FAILED",
                    "http_status": 500,
                    "latency_ms": round(latency_ms, 2),
                    "credits_used": 0,
                    "error": err_msg
                })

        if results["failures"]:
            results["status"] = "FAILED" if len(results["failures"]) == len(endpoints) else "PARTIAL"
        else:
            results["status"] = "SUCCESS"

    finally:
        if close_client:
            await client.aclose()

    return results


def main():
    parser = argparse.ArgumentParser(description="AstroWay Universal Extractor v2.1")
    parser.add_argument("--client-file", type=str, help="Path to client JSON file")
    parser.add_argument("--output", type=str, help="Path to write output JSON")
    parser.add_argument("--max-endpoints", type=int, default=0, help="Maximum endpoints to extract (0 = all)")
    parser.add_argument("--include-pdf", type=str, help="Comma-separated PDF reports to include (default: none)")
    args = parser.parse_args()

    client_data = {
        "year": 1986, "month": 1, "day": 18,
        "hour": 3, "minute": 0,
        "lat": 6.2340437, "lng": -75.5731248,
        "tz_offset": -5.0,
        "name": "Consultant",
        "gender": "female"
    }

    if args.client_file and Path(args.client_file).exists():
        p = Path(args.client_file)
        if p.suffix.lower() == ".json":
            client_data = json.loads(p.read_text(encoding="utf-8"))

    include_pdf = [x.strip() for x in args.include_pdf.split(",")] if args.include_pdf else None

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(
        extract_astroway(
            client_data,
            include_pdf=include_pdf,
            max_endpoints=args.max_endpoints
        )
    )

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Extraction saved to {args.output}")
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
