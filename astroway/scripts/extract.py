#!/usr/bin/env python3
"""
Autonomous Extractor for AstroWay REST Engine (v2.0)
Extracts Western Natal, Harmonics, Draconic, Heliocentric, 16 Vedic Vargas (D1 to D60),
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
from typing import Any, Dict, List, Optional
import httpx

BASE_URL = os.getenv("ASTROWAY_URL", "https://api.astroway.info")
DEFAULT_TIMEOUT = 16.0


async def extract_astroway(
    client_data: Dict[str, Any],
    api_key: Optional[str] = None,
    client: Optional[httpx.AsyncClient] = None,
    include_pdf: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Executes full high-precision Swiss Ephemeris AstroWay extraction across all domains.
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

    # Hellenistic ZR Payload
    zr_payload = {
        **base_payload,
        "years": 80
    }

    # ACG Best Places Payload
    acg_best_payload = {
        **base_payload,
        "category": "career"
    }

    # Harmonics Payloads
    h5_payload = {"harmonic": 5, **base_payload}
    h7_payload = {"harmonic": 7, **base_payload}
    h9_payload = {"harmonic": 9, **base_payload}

    # Esoteric & Numerology Payloads
    destiny_payload = {"date": date_str}
    gematria_payload = {"text": name}
    numerology_payload = {"name": name, "date": date_str}

    # Taxative list of 124 pure calculation endpoints (0 PDFs)
    endpoints: List[tuple] = [
        # 1. Western Natal, Special Charts & Harmonics
        ("western_chart", "/chart", base_payload),
        ("western_chart_fagan_campanus", "/chart", fc_payload),
        ("western_harmonics_h5", "/harmonics", h5_payload),
        ("western_harmonics_h7", "/harmonics", h7_payload),
        ("western_harmonics_h9", "/harmonics", h9_payload),
        ("western_draconic", "/draconic", base_payload),
        ("western_heliocentric", "/heliocentric", base_payload),
        ("western_relocation", "/relocation", base_payload),
        ("western_geodetic", "/geodetic", base_payload),
        ("almuten_figuris", "/almuten", base_payload),
        ("arabic_parts", "/arabic-parts", base_payload),
        ("essential_dignities", "/essential-dignities", base_payload),
        ("receptions", "/receptions", base_payload),
        ("fixed_stars", "/fixed-stars", base_payload),
        ("hyleg", "/hyleg", base_payload),
        ("firdaria", "/firdaria", base_payload),
        ("antiscia", "/antiscia", base_payload),
        ("profections", "/profections", base_payload),
        ("disposition_chains", "/disposition-chains", base_payload),

        # 2. Vedic Shodashavargas (16 Vargas)
        ("vedic_varga_d1", "/vedic/varga/D1", base_payload),
        ("vedic_varga_d2", "/vedic/varga/D2", base_payload),
        ("vedic_varga_d3", "/vedic/varga/D3", base_payload),
        ("vedic_varga_d4", "/vedic/varga/D4", base_payload),
        ("vedic_varga_d7", "/vedic/varga/D7", base_payload),
        ("vedic_varga_d9", "/vedic/varga/D9", base_payload),
        ("vedic_varga_d10", "/vedic/varga/D10", base_payload),
        ("vedic_varga_d12", "/vedic/varga/D12", base_payload),
        ("vedic_varga_d16", "/vedic/varga/D16", base_payload),
        ("vedic_varga_d20", "/vedic/varga/D20", base_payload),
        ("vedic_varga_d24", "/vedic/varga/D24", base_payload),
        ("vedic_varga_d27", "/vedic/varga/D27", base_payload),
        ("vedic_varga_d30", "/vedic/varga/D30", base_payload),
        ("vedic_varga_d40", "/vedic/varga/D40", base_payload),
        ("vedic_varga_d45", "/vedic/varga/D45", base_payload),
        ("vedic_varga_d60", "/vedic/varga/D60", base_payload),

        # 3. Vedic Dashas, Shadbala, Ashtakavarga & Panchang
        ("vedic_dashas_vimshottari_maha", "/vedic/dashas/vimshottari/maha", base_payload),
        ("vedic_dashas_vimshottari_antar", "/vedic/dashas/vimshottari/antar", base_payload),
        ("vedic_dashas_yogini_maha", "/vedic/dashas/yogini/maha", base_payload),
        ("vedic_dashas_chara_maha", "/vedic/dashas/chara/maha", base_payload),
        ("vedic_shadbala_full", "/vedic/shadbala/full", base_payload),
        ("vedic_bhavabala", "/vedic/bhavabala", base_payload),
        ("vedic_ashtakavarga", "/ashtakavarga", base_payload),
        ("vedic_panchang_full", "/vedic/panchang/full", base_payload),

        # 4. Vedic Jaimini & Yogas
        ("jaimini_karakas", "/vedic/jaimini/karakas", base_payload),
        ("jaimini_chara_karakas", "/vedic/jaimini/chara-karakas", base_payload),
        ("jaimini_padas", "/vedic/jaimini/padas", base_payload),
        ("jaimini_upapada", "/vedic/jaimini/upapada", base_payload),
        ("jaimini_atmakaraka_navamsa", "/vedic/jaimini/atmakaraka-navamsa", base_payload),
        ("jaimini_argala_analysis", "/vedic/jaimini/argala-analysis", base_payload),
        ("jaimini_yogas", "/vedic/jaimini/yogas", base_payload),
        ("vedic_yogas_parashara_full", "/vedic/yogas/parashara/full", base_payload),
        ("vedic_yogas_jaimini_full", "/vedic/yogas/jaimini/full", base_payload),

        # 5. Lal Kitab
        ("lal_kitab_teva", "/vedic/lal-kitab/teva", base_payload),
        ("lal_kitab_debts", "/vedic/lal-kitab/debts", base_payload),
        ("lal_kitab_remedies", "/vedic/lal-kitab/remedies", base_payload),
        ("lal_kitab_varshphal", "/vedic/lal-kitab/varshphal", base_payload),

        # 6. Human Design
        ("human_design", "/human-design", base_payload),
        ("hd_circuitry", "/hd/circuitry", base_payload),
        ("hd_incarnation_cross", "/hd/incarnation-cross", base_payload),
        ("hd_sensitivity", "/hd/sensitivity", base_payload),
        ("hd_dream_rave", "/hd/dream-rave", base_payload),
        ("hd_hologenetic", "/hd/hologenetic", base_payload),

        # 7. Chinese BaZi & Zi Wei Dou Shu
        ("bazi_four_pillars", "/bazi/four-pillars", bazi_base_payload),
        ("bazi_ten_gods", "/bazi/ten-gods", bazi_base_payload),
        ("bazi_day_master", "/bazi/day-master", bazi_base_payload),
        ("bazi_luck_pillars", "/bazi/luck-pillars", bazi_luck_payload),
        ("bazi_element_balance", "/bazi/element-balance", bazi_base_payload),
        ("bazi_interactions", "/bazi/interactions", bazi_base_payload),
        ("bazi_symbolic_stars", "/bazi/symbolic-stars", bazi_base_payload),
        ("bazi_strength", "/bazi/strength", bazi_base_payload),
        ("ziwei_chart", "/ziwei/chart", ziwei_payload),
        ("ziwei_four_transformations", "/ziwei/four-transformations", ziwei_sihua_payload),
        ("ziwei_twelve_palaces", "/ziwei/twelve-palaces", ziwei_payload),

        # 8. Business, Finance & Career
        ("business_founder_personality", "/business/founder-personality", base_payload),
        ("business_leadership_style", "/business/leadership-style", base_payload),
        ("business_ideal_industry", "/business/ideal-industry", base_payload),
        ("business_customer_archetype", "/business/customer-archetype", base_payload),
        ("business_marketing_style", "/business/marketing-style", base_payload),
        ("business_founding_chart", "/business/founding-chart", base_payload),
        ("financial_investor_archetype", "/financial/investor-archetype", base_payload),
        ("financial_wealth_house", "/financial/wealth-house", base_payload),
        ("financial_wealth_cycle", "/financial/wealth-cycle", base_payload),
        ("financial_market_timing", "/financial/market-timing", base_payload),
        ("financial_spending_style", "/financial/spending-style", base_payload),
        ("financial_risk_tolerance", "/financial/risk-tolerance", base_payload),

        # 9. Hellenistic Astrology
        ("hellenistic_lots_15", "/hellenistic/brennan/lots-15", base_payload),
        ("hellenistic_zr_spirit", "/hellenistic/brennan/zodiacal-releasing-spirit", zr_payload),
        ("hellenistic_zr_fortune", "/hellenistic/brennan/zodiacal-releasing-fortune", zr_payload),
        ("hellenistic_zr_peaks", "/hellenistic/brennan/zr-peak-periods", zr_payload),
        ("hellenistic_zr_loosing", "/hellenistic/brennan/zr-loosing-of-bond", zr_payload),
        ("hellenistic_profections_detail", "/hellenistic/brennan/profections-detail", base_payload),
        ("hellenistic_time_lord_stack", "/hellenistic/brennan/time-lord-stack", base_payload),
        ("hellenistic_joys_of_planets", "/hellenistic/brennan/joys-of-planets", base_payload),
        ("hellenistic_triplicity_rulers", "/hellenistic/brennan/triplicity-rulers", base_payload),
        ("hellenistic_bonifications_maltreatments", "/hellenistic/brennan/bonifications-maltreatments", base_payload),
        ("hellenistic_antiscia", "/hellenistic/greenbaum/antiscia-hellenistic", base_payload),
        ("hellenistic_dodekatemoria", "/hellenistic/greenbaum/dodekatemoria", base_payload),
        ("hellenistic_daimon_tyche_axis", "/hellenistic/greenbaum/daimon-tyche-axis", base_payload),
        ("hellenistic_bounds", "/hellenistic/hand/bounds", base_payload),
        ("hellenistic_decennials", "/hellenistic/hand/decennials", base_payload),
        ("hellenistic_sect_strength", "/hellenistic/hand/sect-strength", base_payload),

        # 10. Cosmobiology & Hamburg School
        ("cosmobiology_dial90", "/cosmobiology/dial-90", dial90_payload),
        ("cosmobiology_midpoints", "/midpoint-trees", base_payload),
        ("cosmobiology_uranian_tnps", "/cosmobiology/uranian-tnps", base_payload),
        ("cosmobiology_witte_formulas", "/cosmobiology/witte-formulas", dial90_payload),
        ("cosmobiology_midpoint_pictures", "/cosmobiology/midpoint-pictures", dial90_payload),

        # 11. Astromapping & Relocation
        ("geo_acg", "/acg", base_payload),
        ("geo_acg_best_places", "/acg/best-places", acg_best_payload),
        ("geo_local_space", "/local-space", base_payload),
        ("geo_parans", "/parans", base_payload),

        # 12. Evolutionary & Modern Psychological
        ("evolutionary_skipped_steps", "/evolutionary/skipped-steps", base_payload),
        ("evolutionary_nodal_axis", "/evolutionary/nodal-axis-detail", base_payload),
        ("evolutionary_pluto_natal_condition", "/evolutionary/pluto-natal-condition", base_payload),
        ("psychological_greene_archetypes", "/modern/greene/archetypal-figures", base_payload),
        ("psychological_greene_shadow", "/modern/greene/saturn-shadow", base_payload),
        ("psychological_greene_parental_imagos", "/modern/greene/parental-imagos", base_payload),
        ("psychological_greene_lunar_myth", "/modern/greene/lunar-myth", base_payload),
        ("psychological_greene_individuation", "/modern/greene/individuation-path", base_payload),
        ("psychological_arroyo_elements", "/modern/arroyo/element-integration", base_payload),
        ("psychological_arroyo_water_trauma", "/modern/arroyo/water-houses-trauma", base_payload),
        ("psychological_rudhyar_lunation", "/modern/rudhyar/lunation-phase", base_payload),
        ("psychological_rudhyar_sabian", "/modern/rudhyar/symbolic-degrees", base_payload),
        ("psychological_rudhyar_keynote", "/modern/rudhyar/personality-keynote", base_payload),

        # 13. Esoteric & Numerology
        ("destiny_matrix_ladini", "/destiny-matrix/ladini", destiny_payload),
        ("kabbalah_gematria", "/kabbalah/gematria", gematria_payload),
        ("numerology_pythagorean_life_path", "/numerology/pythagorean/life-path", numerology_payload),
        ("numerology_pythagorean_expression", "/numerology/pythagorean/expression", numerology_payload),
        ("numerology_chaldean_life_path", "/numerology/chaldean/life-path", numerology_payload)
    ]

    # Optional PDF report activation (only if explicitly requested via include_pdf)
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
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "SUCCESS",
        "plan": "Indie PRO ($5/mo, 50k credits/mo)",
        "credits_audit": {
            "remaining": None,
            "used_last_call": None,
            "total_spent_this_run": 0,
            "limit": 50000
        },
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
        for key_name, path, body in endpoints:
            url = f"{BASE_URL}/v1{path}"
            t_start = time.perf_counter()
            try:
                # Rate limit pacing: 0.4s between requests to respect Indie PRO limits
                await asyncio.sleep(0.4)
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
                            results["endpoint_audits"].append({
                                "endpoint": key_name,
                                "url": path,
                                "status": "SUCCESS",
                                "http_status": 200,
                                "latency_ms": round(latency_ms, 2),
                                "credits_used": credits_used_call,
                                "error": None
                            })
                    else:
                        results["data"][key_name] = data
                        results["endpoint_audits"].append({
                            "endpoint": key_name,
                            "url": path,
                            "status": "SUCCESS",
                            "http_status": 200,
                            "latency_ms": round(latency_ms, 2),
                            "credits_used": credits_used_call,
                            "error": None
                        })
                else:
                    err_msg = f"HTTP {resp.status_code}: {resp.text[:150]}"
                    results["failures"].append({"endpoint": key_name, "error": err_msg})
                    results["data"][key_name] = {"error": err_msg}
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
    parser = argparse.ArgumentParser(description="AstroWay Extractor v2.0")
    parser.add_argument("--client-file", type=str, help="Path to client JSON file")
    parser.add_argument("--output", type=str, help="Path to write output JSON")
    parser.add_argument("--include-pdf", type=str, help="Comma-separated PDF reports to include (default: none)")
    args = parser.parse_args()

    client_data = {
        "year": 1986, "month": 1, "day": 18,
        "hour": 3, "minute": 0,
        "lat": 6.2340437, "lng": -75.5731248,
        "tz_offset": -5.0,
        "name": "Catalina",
        "gender": "female"
    }

    if args.client_file and Path(args.client_file).exists():
        p = Path(args.client_file)
        if p.suffix.lower() == ".json":
            client_data = json.loads(p.read_text(encoding="utf-8"))

    include_pdf = [x.strip() for x in args.include_pdf.split(",")] if args.include_pdf else None

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(extract_astroway(client_data, include_pdf=include_pdf))

    if args.output:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Extraction saved to {args.output}")
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
