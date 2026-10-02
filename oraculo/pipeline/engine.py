#!/usr/bin/env python3
"""
Oráculo Pipeline Engine (v4.8)
Unified orchestrator for Swiss Ephemeris APIs, MCP clients, and multi-disciplinary extractors.
Includes anti-poisoning cache, dynamic agents root resolution, fail-fast verification,
and selective API execution filters (--apis, --exclude).
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Literal, Optional
import httpx

from pipeline.config import config
from pipeline.cache_manager import CacheManager
from pipeline.clients.mcp_client import UnifiedMcpClient

logger = logging.getLogger("oraculo.engine")


def get_agents_root() -> Path:
    """Dynamically resolves the skills directory for local and Zerops container portability."""
    env_root = os.getenv("AGENTS_ROOT") or os.getenv("SKILLS_ROOT")
    if env_root and Path(env_root).exists():
        return Path(env_root)
    # Search relative to this script: /var/www/.agents/skills/oraculo/pipeline/engine.py
    file_parent = Path(__file__).resolve().parent.parent.parent
    if (file_parent / "astrologyapi").exists():
        return file_parent
    standard = Path("/var/www/.agents/skills")
    if standard.exists() and (standard / "astrologyapi").exists():
        return standard
    repo_skills = Path("/var/www/zerops-astro-skills")
    if repo_skills.exists():
        return repo_skills
    return standard


@dataclass(slots=True)
class ExtractionResult:
    provider: str
    endpoint_key: str
    status: Literal["SUCCESS", "CACHED", "FAILED", "THROTTLED"]
    data: Dict[str, Any]
    http_status: Optional[int] = None
    latency_ms: float = 0.0
    error: Optional[str] = None


class ExtractionEngine:
    def __init__(self, cache_dir: str = "raw/json/cache", refresh_pro: bool = False):
        self.cache = CacheManager(cache_dir=cache_dir)
        self.refresh_pro = refresh_pro

    async def execute_extraction(
        self,
        client_data: dict,
        apis: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Entry point that delegates to extract_all."""
        return await self.extract_all(client_data, apis=apis, exclude=exclude)

    async def extract_all(
        self,
        client_data: dict,
        apis: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Executes unified concurrent extraction across external REST APIs and MCP tools.
        Applies filter filters (apis, exclude) and enforces strict unpoisoned cache mechanics.
        """
        norm_apis = [a.lower().strip() for a in apis] if apis else None
        norm_exclude = [e.lower().strip() for e in exclude] if exclude else []

        def should_run(prov: str) -> bool:
            if norm_apis and prov.lower() not in norm_apis:
                return False
            if prov.lower() in norm_exclude:
                return False
            return True

        client_cache_key = self.cache.generate_client_hash(client_data)
        
        # Prepare birth data fields
        year = int(client_data.get("year", 1990))
        month = int(client_data.get("month", 1))
        day = int(client_data.get("day", 1))
        hour = int(client_data.get("hour", 12))
        minute = int(client_data.get("minute", 0))
        lat = float(client_data.get("lat", 0.0))
        lng = float(client_data.get("lng", 0.0))
        tz_offset = float(client_data.get("tz_offset", -5.0))
        tz_str = client_data.get("tz_str", "UTC")
        city = client_data.get("city", client_data.get("preferred_name", "Unknown"))

        date_str = f"{year:04d}-{month:02d}-{day:02d}"
        iso_local_str = f"{date_str}T{hour:02d}:{minute:02d}:00"
        bazi_datetime_str = f"{date_str} {hour:02d}:{minute:02d}:00"

        rest_results: Dict[str, Dict[str, Any]] = {
            "freeastro": {},
            "astroway": {},
            "astrologyapi": {},
            "vedastro": {},
            "hebcal": {},
            "nasa": {}
        }
        mcp_results: Dict[str, Dict[str, Any]] = {}
        credit_stats: Dict[str, Any] = {
            "calls_made": {},
            "cache_hits": {},
            "astroway_credits_remaining": None,
            "astroway_credits_used": None,
            "astroway_credits_limit": 50000,
            "freeastro_report_credits": None,
            "vedastro_plan": "PRO Unlimited ($1/mo, llamadas ilimitadas)",
            "astrologyapi_plan": "Free Tier Dedicated (9 macro endpoints)"
        }
        results_list: List[ExtractionResult] = []

        # Dynamic import of sub-skills to guarantee SSoT independence
        import importlib.util
        agents_root = get_agents_root()

        def _load_extractor(skill_name: str):
            p = agents_root / skill_name / "scripts" / "extract.py"
            if p.exists():
                spec = importlib.util.spec_from_file_location(f"{skill_name}_extract", str(p))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return getattr(mod, f"extract_{skill_name}", None)
            return None

        fn_freeastro = _load_extractor("freeastroapi")
        fn_astroway = _load_extractor("astroway")
        fn_astrology = _load_extractor("astrologyapi")
        fn_vedastro = _load_extractor("vedastro")

        mcp_client = UnifiedMcpClient(self.cache)

        async with httpx.AsyncClient(timeout=18.0, follow_redirects=True) as http_client:
            # 1. Dispatch FreeAstroAPI
            async def _run_freeastro():
                if fn_freeastro and should_run("freeastro") and should_run("freeastroapi"):
                    # Check cache first (reject poisoned entries)
                    cached = self.cache.get("freeastro", "full_extract", client_cache_key) if not self.refresh_pro else None
                    if cached and isinstance(cached, dict) and "data" in cached:
                        cached_has_err = bool(cached.get("failures")) or any(
                            isinstance(v, dict) and ("error" in v or v.get("status") == "FAIL")
                            for v in cached.get("data", {}).values()
                        )
                        if not cached_has_err and len(cached.get("data", {})) > 0:
                            rest_results["freeastro"] = cached.get("data", {})
                            credit_stats["freeastro_report_credits"] = cached.get("report_credits")
                            credit_stats["calls_made"]["freeastro"] = 0
                            credit_stats["cache_hits"]["freeastro"] = 1
                            for ep_k, ep_data in cached.get("data", {}).items():
                                results_list.append(ExtractionResult(
                                    provider="freeastro", endpoint_key=ep_k,
                                    status="CACHED", data=ep_data, http_status=200, latency_ms=0.0
                                ))
                            return

                    t0 = asyncio.get_event_loop().time()
                    try:
                        res = await fn_freeastro(client_data, client=http_client)
                        elapsed = (asyncio.get_event_loop().time() - t0) * 1000.0
                        rest_results["freeastro"] = res.get("data", {})
                        credit_stats["freeastro_report_credits"] = res.get("report_credits")
                        credit_stats["calls_made"]["freeastro"] = res.get("calls_made", 0)

                        # Enforce Invariant 5: Anti-Poisoning (Only cache 100% verified clean responses)
                        has_err = bool(res.get("failures")) or res.get("status") != "SUCCESS" or any(
                            isinstance(v, dict) and ("error" in v or v.get("status") == "FAIL")
                            for v in res.get("data", {}).values()
                        )
                        if res.get("data") and not has_err:
                            self.cache.set("freeastro", "full_extract", client_cache_key, res, http_status=200)

                        for ep_k, ep_data in res.get("data", {}).items():
                            is_err = isinstance(ep_data, dict) and ("error" in ep_data or ep_data.get("status") == "FAIL")
                            results_list.append(ExtractionResult(
                                provider="freeastro", endpoint_key=ep_k,
                                status="FAILED" if is_err else "SUCCESS",
                                data=ep_data if not is_err else {},
                                http_status=200 if not is_err else 500,
                                latency_ms=elapsed / max(1, len(res.get("data", {}))),
                                error=ep_data.get("error") if is_err else None
                            ))
                    except Exception as exc:
                        results_list.append(ExtractionResult(
                            provider="freeastro", endpoint_key="all", status="FAILED",
                            data={}, http_status=500, error=str(exc)
                        ))

            # 2. Dispatch AstroWay
            async def _run_astroway():
                if fn_astroway and should_run("astroway"):
                    cached = self.cache.get("astroway", "full_extract", client_cache_key) if not self.refresh_pro else None
                    if cached and isinstance(cached, dict) and "data" in cached:
                        cached_has_err = bool(cached.get("failures")) or any(
                            isinstance(v, dict) and ("error" in v or v.get("ok") is False)
                            for v in cached.get("data", {}).values()
                        )
                        if not cached_has_err and len(cached.get("data", {})) > 0:
                            rest_results["astroway"] = cached.get("data", {})
                            audit = cached.get("credits_audit", {})
                            credit_stats["astroway_credits_remaining"] = audit.get("remaining")
                            credit_stats["astroway_credits_used"] = audit.get("used_last_call")
                            credit_stats["astroway_credits_limit"] = audit.get("limit", 50000)
                            credit_stats["calls_made"]["astroway"] = 0
                            credit_stats["cache_hits"]["astroway"] = 1
                            for ep_k, ep_data in cached.get("data", {}).items():
                                results_list.append(ExtractionResult(
                                    provider="astroway", endpoint_key=ep_k,
                                    status="CACHED", data=ep_data, http_status=200, latency_ms=0.0
                                ))
                            return

                    t0 = asyncio.get_event_loop().time()
                    try:
                        res = await fn_astroway(client_data, client=http_client)
                        elapsed = (asyncio.get_event_loop().time() - t0) * 1000.0
                        rest_results["astroway"] = res.get("data", {})
                        audit = res.get("credits_audit", {})
                        credit_stats["astroway_credits_remaining"] = audit.get("remaining")
                        credit_stats["astroway_credits_used"] = audit.get("used_last_call")
                        credit_stats["astroway_credits_limit"] = audit.get("limit", 50000)
                        credit_stats["calls_made"]["astroway"] = res.get("calls_made", 0)

                        has_err = bool(res.get("failures")) or res.get("status") != "SUCCESS" or any(
                            isinstance(v, dict) and ("error" in v or v.get("ok") is False)
                            for v in res.get("data", {}).values()
                        )
                        if res.get("data") and not has_err:
                            self.cache.set("astroway", "full_extract", client_cache_key, res, http_status=200)

                        for ep_k, ep_data in res.get("data", {}).items():
                            is_err = isinstance(ep_data, dict) and ("error" in ep_data or ep_data.get("ok") is False)
                            results_list.append(ExtractionResult(
                                provider="astroway", endpoint_key=ep_k,
                                status="FAILED" if is_err else "SUCCESS",
                                data=ep_data if not is_err else {},
                                http_status=200 if not is_err else 500,
                                latency_ms=elapsed / max(1, len(res.get("data", {}))),
                                error=ep_data.get("error") if is_err else None
                            ))
                    except Exception as exc:
                        results_list.append(ExtractionResult(
                            provider="astroway", endpoint_key="all", status="FAILED",
                            data={}, http_status=500, error=str(exc)
                        ))

            # 3. Dispatch AstrologyAPI
            async def _run_astrology():
                if fn_astrology and should_run("astrologyapi") and should_run("astrology_api_io"):
                    cached = self.cache.get("astrologyapi", "full_extract", client_cache_key) if not self.refresh_pro else None
                    if cached and isinstance(cached, dict) and "data" in cached:
                        cached_has_err = bool(cached.get("failures")) or any(
                            isinstance(v, dict) and "error" in v
                            for v in cached.get("data", {}).values()
                        )
                        if not cached_has_err and len(cached.get("data", {})) > 0:
                            rest_results["astrologyapi"] = cached.get("data", {})
                            credit_stats["calls_made"]["astrologyapi"] = 0
                            credit_stats["cache_hits"]["astrologyapi"] = 1
                            for ep_k, ep_data in cached.get("data", {}).items():
                                results_list.append(ExtractionResult(
                                    provider="astrologyapi", endpoint_key=ep_k,
                                    status="CACHED", data=ep_data, http_status=200, latency_ms=0.0
                                ))
                            return

                    t0 = asyncio.get_event_loop().time()
                    try:
                        res = await fn_astrology(client_data, client=http_client)
                        elapsed = (asyncio.get_event_loop().time() - t0) * 1000.0
                        rest_results["astrologyapi"] = res.get("data", {})
                        credit_stats["calls_made"]["astrologyapi"] = res.get("calls_made", 0)

                        has_err = bool(res.get("failures")) or res.get("status") != "SUCCESS" or any(
                            isinstance(v, dict) and "error" in v
                            for v in res.get("data", {}).values()
                        )
                        if res.get("data") and not has_err:
                            self.cache.set("astrologyapi", "full_extract", client_cache_key, res, http_status=200)

                        for ep_k, ep_data in res.get("data", {}).items():
                            is_err = isinstance(ep_data, dict) and "error" in ep_data
                            results_list.append(ExtractionResult(
                                provider="astrologyapi", endpoint_key=ep_k,
                                status="FAILED" if is_err else "SUCCESS",
                                data=ep_data if not is_err else {},
                                http_status=200 if not is_err else 500,
                                latency_ms=elapsed / max(1, len(res.get("data", {}))),
                                error=ep_data.get("error") if is_err else None
                            ))
                    except Exception as exc:
                        results_list.append(ExtractionResult(
                            provider="astrologyapi", endpoint_key="all", status="FAILED",
                            data={}, http_status=500, error=str(exc)
                        ))

            # 4. Dispatch VedAstro
            async def _run_vedastro():
                if fn_vedastro and should_run("vedastro"):
                    cached = self.cache.get("vedastro", "full_extract", client_cache_key) if not self.refresh_pro else None
                    if cached and isinstance(cached, dict) and "data" in cached:
                        cached_has_err = bool(cached.get("failures")) or any(
                            isinstance(v, dict) and ("error" in v or v.get("status") == "FAIL")
                            for v in cached.get("data", {}).values()
                        )
                        if not cached_has_err and len(cached.get("data", {})) > 0:
                            rest_results["vedastro"] = cached.get("data", {})
                            credit_stats["calls_made"]["vedastro"] = 0
                            credit_stats["cache_hits"]["vedastro"] = 1
                            for ep_k, ep_data in cached.get("data", {}).items():
                                results_list.append(ExtractionResult(
                                    provider="vedastro", endpoint_key=ep_k,
                                    status="CACHED", data=ep_data, http_status=200, latency_ms=0.0
                                ))
                            return

                    t0 = asyncio.get_event_loop().time()
                    try:
                        res = await fn_vedastro(client_data, client=http_client)
                        elapsed = (asyncio.get_event_loop().time() - t0) * 1000.0
                        rest_results["vedastro"] = res.get("data", {})
                        credit_stats["calls_made"]["vedastro"] = res.get("calls_made", 0)

                        has_err = bool(res.get("failures")) or res.get("status") != "SUCCESS" or any(
                            isinstance(v, dict) and ("error" in v or v.get("status") == "FAIL")
                            for v in res.get("data", {}).values()
                        )
                        if res.get("data") and not has_err:
                            self.cache.set("vedastro", "full_extract", client_cache_key, res, http_status=200)

                        for ep_k, ep_data in res.get("data", {}).items():
                            is_err = isinstance(ep_data, dict) and ("error" in ep_data or ep_data.get("status") == "FAIL")
                            results_list.append(ExtractionResult(
                                provider="vedastro", endpoint_key=ep_k,
                                status="FAILED" if is_err else "SUCCESS",
                                data=ep_data if not is_err else {},
                                http_status=200 if not is_err else 500,
                                latency_ms=elapsed / max(1, len(res.get("data", {}))),
                                error=ep_data.get("error") if is_err else None
                            ))
                    except Exception as exc:
                        results_list.append(ExtractionResult(
                            provider="vedastro", endpoint_key="all", status="FAILED",
                            data={}, http_status=500, error=str(exc)
                        ))

            # 5. Dispatch HebCal & NASA
            async def _run_hebcal_nasa():
                run_heb = should_run("hebcal")
                run_nasa = should_run("nasa")

                if run_heb:
                    cached_heb = self.cache.get("hebcal", "combined", client_cache_key) if not self.refresh_pro else None
                    if cached_heb and isinstance(cached_heb, dict) and "converter" in cached_heb:
                        rest_results["hebcal"] = cached_heb
                        credit_stats["cache_hits"]["hebcal"] = 1
                        results_list.append(ExtractionResult(provider="hebcal", endpoint_key="converter", status="CACHED", data=cached_heb.get("converter", {}), http_status=200))
                        results_list.append(ExtractionResult(provider="hebcal", endpoint_key="zmanim", status="CACHED", data=cached_heb.get("zmanim", {}), http_status=200))
                    else:
                        # HebCal converter
                        try:
                            h_url = f"https://www.hebcal.com/converter?cfg=json&gy={year}&gm={month}&gd={day}&g2h=1"
                            resp = await http_client.get(h_url)
                            d = resp.json()
                            rest_results["hebcal"]["converter"] = d
                            results_list.append(ExtractionResult(provider="hebcal", endpoint_key="converter", status="SUCCESS", data=d, http_status=200))
                        except Exception as e:
                            results_list.append(ExtractionResult(provider="hebcal", endpoint_key="converter", status="FAILED", data={}, error=str(e)))

                        # HebCal zmanim
                        try:
                            z_url = f"https://www.hebcal.com/zmanim?cfg=json&latitude={lat}&longitude={lng}&date={date_str}"
                            resp = await http_client.get(z_url)
                            d = resp.json()
                            rest_results["hebcal"]["zmanim"] = d
                            results_list.append(ExtractionResult(provider="hebcal", endpoint_key="zmanim", status="SUCCESS", data=d, http_status=200))
                        except Exception as e:
                            results_list.append(ExtractionResult(provider="hebcal", endpoint_key="zmanim", status="FAILED", data={}, error=str(e)))
                        
                        if rest_results["hebcal"].get("converter") and rest_results["hebcal"].get("zmanim"):
                            self.cache.set("hebcal", "combined", client_cache_key, rest_results["hebcal"], http_status=200)

                if run_nasa:
                    cached_nasa = self.cache.get("nasa", "asteroids", client_cache_key) if not self.refresh_pro else None
                    if cached_nasa and isinstance(cached_nasa, dict) and cached_nasa:
                        rest_results["nasa"] = cached_nasa
                        credit_stats["cache_hits"]["nasa"] = 1
                        for ast_k, ast_v in cached_nasa.items():
                            results_list.append(ExtractionResult(provider="nasa", endpoint_key=ast_k, status="CACHED", data=ast_v, http_status=200))
                    else:
                        asteroid_ids = {
                            "ceres": "1;",
                            "pallas": "2;",
                            "juno": "3;",
                            "vesta": "4;",
                            "chiron": "2060;",
                            "eris": "136199;"
                        }
                        for ast_name, ast_cmd in asteroid_ids.items():
                            try:
                                h_params = {
                                    "format": "json",
                                    "COMMAND": f"'{ast_cmd}'",
                                    "EPHEM_TYPE": "'OBSERVER'",
                                    "CENTER": "'500@399'",
                                    "START_TIME": f"'{date_str}'",
                                    "STOP_TIME": f"'{date_str} 23:59'",
                                    "STEP_SIZE": "'1d'",
                                    "QUANTITIES": "'31'"
                                }
                                h_res = await http_client.get("https://ssd.jpl.nasa.gov/api/horizons.api", params=h_params, timeout=6.0)
                                if h_res.status_code == 200:
                                    h_json = h_res.json()
                                    d_ast = {"name": ast_name.capitalize(), "horizons_result": h_json.get("result", "")[:500]}
                                    rest_results["nasa"][f"asteroid_{ast_name}"] = d_ast
                                    results_list.append(ExtractionResult(provider="nasa", endpoint_key=f"asteroid_{ast_name}", status="SUCCESS", data=d_ast, http_status=200))
                                else:
                                    results_list.append(ExtractionResult(provider="nasa", endpoint_key=f"asteroid_{ast_name}", status="FAILED", data={}, http_status=h_res.status_code, error=f"HTTP {h_res.status_code}"))
                            except Exception as e:
                                results_list.append(ExtractionResult(provider="nasa", endpoint_key=f"asteroid_{ast_name}", status="FAILED", data={}, error=str(e)))
                        if rest_results["nasa"]:
                            self.cache.set("nasa", "asteroids", client_cache_key, rest_results["nasa"], http_status=200)

            # 6. Dispatch MCPs
            async def _run_mcps():
                if not should_run("mcp"):
                    return
                # Lunar MCP calculate_bazi
                try:
                    bazi_res = await mcp_client.call_tool(
                        "lunar", "calculate_bazi",
                        {"birth_datetime": bazi_datetime_str, "timezone_offset": int(tz_offset)}
                    )
                    mcp_results["lunar_mcp_calculate_bazi"] = bazi_res
                    results_list.append(ExtractionResult(provider="lunar_mcp", endpoint_key="calculate_bazi", status="SUCCESS", data=bazi_res, http_status=200))
                except Exception as e:
                    results_list.append(ExtractionResult(provider="lunar_mcp", endpoint_key="calculate_bazi", status="FAILED", data={}, error=str(e)))

                # Lunar MCP solar_to_lunar
                try:
                    stl_res = await mcp_client.call_tool(
                        "lunar", "solar_to_lunar",
                        {"solar_date": date_str, "culture": "chinese"}
                    )
                    mcp_results["lunar_mcp_solar_to_lunar"] = stl_res
                    results_list.append(ExtractionResult(provider="lunar_mcp", endpoint_key="solar_to_lunar", status="SUCCESS", data=stl_res, http_status=200))
                except Exception as e:
                    results_list.append(ExtractionResult(provider="lunar_mcp", endpoint_key="solar_to_lunar", status="FAILED", data={}, error=str(e)))

                # Lunar MCP get_lucky_hours
                try:
                    lh_res = await mcp_client.call_tool(
                        "lunar", "get_lucky_hours",
                        {"date": date_str, "culture": "chinese"}
                    )
                    mcp_results["lunar_mcp_get_lucky_hours"] = lh_res
                    results_list.append(ExtractionResult(provider="lunar_mcp", endpoint_key="get_lucky_hours", status="SUCCESS", data=lh_res, http_status=200))
                except Exception as e:
                    results_list.append(ExtractionResult(provider="lunar_mcp", endpoint_key="get_lucky_hours", status="FAILED", data={}, error=str(e)))

                # Zmanim MCP daily_times
                try:
                    zm_res = await mcp_client.call_tool(
                        "zmanim", "zmanim_get_daily_times",
                        {"location": city or "Unknown", "latitude": lat, "longitude": lng, "date": date_str, "time_zone": tz_str, "response_format": "json"}
                    )
                    mcp_results["zmanim_mcp_daily_times"] = zm_res
                    results_list.append(ExtractionResult(provider="zmanim_mcp", endpoint_key="daily_times", status="SUCCESS", data=zm_res, http_status=200))
                except Exception as e:
                    results_list.append(ExtractionResult(provider="zmanim_mcp", endpoint_key="daily_times", status="FAILED", data={}, error=str(e)))

                # Kundali MCP
                try:
                    kd_res = await mcp_client.call_tool(
                        "kundali", "kundali",
                        {
                            "birth_datetime": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00",
                            "latitude": float(lat),
                            "longitude": float(lng),
                            "school": "parashari",
                            "locale": "en"
                        }
                    )
                    mcp_results["kundali_mcp_kundali_calc"] = kd_res
                    results_list.append(ExtractionResult(provider="kundali_mcp", endpoint_key="kundali_calc", status="SUCCESS", data=kd_res, http_status=200))
                except Exception as e:
                    results_list.append(ExtractionResult(provider="kundali_mcp", endpoint_key="kundali_calc", status="FAILED", data={}, error=str(e)))

                # Kundali MCP kundali_milan (if partner data exists)
                partner = client_data.get("partner")
                if partner and isinstance(partner, dict):
                    try:
                        p_dt = f"{partner.get('year', year):04d}-{partner.get('month', month):02d}-{partner.get('day', day):02d}T{partner.get('hour', hour):02d}:{partner.get('minute', minute):02d}:00"
                        km_res = await mcp_client.call_tool(
                            "kundali", "kundali_milan",
                            {
                                "groom": {"birth_datetime": iso_local_str, "latitude": lat, "longitude": lng},
                                "bride": {"birth_datetime": p_dt, "latitude": float(partner.get("lat", lat)), "longitude": float(partner.get("lng", lng))},
                                "school": "parashari",
                                "locale": "en"
                            }
                        )
                        mcp_results["kundali_mcp_kundali_milan"] = km_res
                        results_list.append(ExtractionResult(provider="kundali_mcp", endpoint_key="kundali_milan", status="SUCCESS", data=km_res, http_status=200))
                    except Exception as e:
                        results_list.append(ExtractionResult(provider="kundali_mcp", endpoint_key="kundali_milan", status="FAILED", data={}, error=str(e)))

            # Execute all tasks concurrently in TaskGroup
            async with asyncio.TaskGroup() as tg:
                tg.create_task(_run_freeastro())
                tg.create_task(_run_astroway())
                tg.create_task(_run_astrology())
                tg.create_task(_run_vedastro())
                tg.create_task(_run_hebcal_nasa())
                tg.create_task(_run_mcps())

        return {
            "client_data": client_data,
            "rest": rest_results,
            "mcp": mcp_results,
            "credit_stats": credit_stats,
            "extraction_results": results_list
        }
