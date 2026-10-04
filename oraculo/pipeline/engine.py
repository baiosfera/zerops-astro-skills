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
        self.audit_dir = Path(cache_dir).parent / "audit"
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def _save_micro_audit(
        self,
        provider: str,
        status: str,
        results_list: List[ExtractionResult],
        credit_stats: dict,
        client_data: dict,
        latency_ms: float = 0.0,
        is_cached: bool = False
    ) -> None:
        try:
            self.audit_dir.mkdir(parents=True, exist_ok=True)
            audit_file = self.audit_dir / f"audit_{provider}.json"
            audit_md_file = self.audit_dir / f"audit_{provider}.md"

            prov_results = [
                r for r in results_list
                if r.provider == provider
                or (provider == "freeastro" and r.provider in ("freeastro", "freeastroapi"))
                or (provider == "mcp" and "mcp" in r.provider)
                or (provider == "lunar" and r.provider in ("lunar", "lunar_mcp"))
                or (provider == "zmanim" and r.provider in ("zmanim", "zmanim_mcp"))
                or (provider == "kundali" and r.provider in ("kundali", "kundali_mcp"))
            ]

            effective_cached = is_cached or (bool(prov_results) and all(r.status == "CACHED" for r in prov_results))

            # Read historical credit data if present to preserve balances on cached re-runs
            prev_credits = {}
            if audit_file.exists():
                try:
                    with open(audit_file, "r", encoding="utf-8") as f:
                        prev_rec = json.load(f)
                    if isinstance(prev_rec, dict):
                        prev_credits = prev_rec.get("credits_audit", {})
                except Exception:
                    pass

            consultant_name = client_data.get("preferred_name") or client_data.get("name") or "Unknown"

            rem_aw = credit_stats.get("astroway_credits_remaining")
            if rem_aw is None:
                rem_aw = prev_credits.get("astroway_credits_remaining")

            used_aw = credit_stats.get("astroway_credits_used")
            if used_aw is None:
                used_aw = prev_credits.get("astroway_credits_used")

            rep_fa = credit_stats.get("freeastro_report_credits")
            if rep_fa is None:
                rep_fa = prev_credits.get("freeastro_report_credits")

            calls_val = credit_stats.get("calls_made", {}).get(provider)
            if calls_val is None:
                if effective_cached:
                    calls_val = 0
                else:
                    calls_val = prev_credits.get("calls_made", len(prov_results))

            audit_record = {
                "provider": provider,
                "consultant": consultant_name,
                "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "status": status,
                "is_cached": effective_cached,
                "total_endpoints": len(prov_results),
                "success_count": len([r for r in prov_results if r.status in ("SUCCESS", "CACHED")]),
                "failure_count": len([r for r in prov_results if r.status == "FAILED"]),
                "latency_ms": round(latency_ms, 2),
                "credits_audit": {
                    "astroway_credits_remaining": rem_aw,
                    "astroway_credits_used": used_aw,
                    "freeastro_report_credits": rep_fa,
                    "calls_made": calls_val
                },
                "endpoints": [
                    {
                        "endpoint": r.endpoint_key,
                        "status": r.status,
                        "http_status": r.http_status,
                        "latency_ms": round(r.latency_ms, 2),
                        "error": r.error
                    }
                    for r in prov_results
                ]
            }
            with open(audit_file, "w", encoding="utf-8") as f:
                json.dump(audit_record, f, indent=2, ensure_ascii=False)

            # Generate individual Markdown audit
            md_content = self._render_provider_markdown(audit_record)
            with open(audit_md_file, "w", encoding="utf-8") as f:
                f.write(md_content)

            # Update cumulative Lakehouse audit
            self._render_lakehouse_markdown()
        except Exception as exc:
            logger.warning(f"Could not write micro audit for {provider}: {exc}")

    def _render_provider_markdown(self, audit_record: dict) -> str:
        provider = audit_record.get("provider", "unknown").upper()
        consultant = audit_record.get("consultant", "Unknown")
        ts = audit_record.get("timestamp_utc", "")
        status = audit_record.get("status", "UNKNOWN")
        is_cached = audit_record.get("is_cached", False)
        total = audit_record.get("total_endpoints", 0)
        success = audit_record.get("success_count", 0)
        failures = audit_record.get("failure_count", 0)
        latency = audit_record.get("latency_ms", 0.0)
        credits_audit = audit_record.get("credits_audit", {})
        endpoints = audit_record.get("endpoints", [])

        status_badge = "🟢 **SUCCESS**" if status == "SUCCESS" else ("🔵 **CACHED**" if status == "CACHED" else ("🟡 **PARTIAL**" if status == "PARTIAL" else f"🔴 **{status}**"))
        origin = "⚡ **Caché Inmutable en Disco** (0ms, 0 créditos consumidos)" if is_cached else "🌐 **Llamada en Vivo a la API**"

        md = [
            f"# 📊 Auditoría de Extracción: {provider}",
            "",
            f"> **Consultante:** `{consultant}` | **Timestamp:** `{ts}`  ",
            f"> **Estado Operativo:** {status_badge} | **Origen:** {origin}",
            "",
            "---",
            "",
            "## 1. Resumen Ejecutivo de Métricas",
            "",
            "| Métrica | Valor | Detalle / Observación |",
            "|---|---|---|",
            f"| **Estado Global** | `{status}` | {'Todos los endpoints respondieron correctamente' if failures == 0 else f'{failures} fallos detectados'} |",
            f"| **Total Endpoints Evaluados** | `{total}` | Universo taxativo invocado |",
            f"| **Respuestas Exitosas (200 OK)** | `{success}` | Tasa de éxito: {round(success / max(1, total) * 100, 1)}% |",
            f"| **Fallas / Errores** | `{failures}` | {'Cero errores' if failures == 0 else 'Revisar tabla de detalle'} |",
            f"| **Latencia Total Incurrida** | `{latency:.2f} ms` | {'0 ms por hit en caché' if is_cached else 'Tiempo total de red'} |",
        ]

        prov_low = provider.lower()
        calls = credits_audit.get("calls_made", total)
        calls_detail = "0 llamadas HTTP (100% Blindaje por Caché)" if (is_cached or calls == 0) else "Peticiones HTTP enviadas"

        if prov_low in ("astroway", "astroway_api"):
            rem = credits_audit.get("astroway_credits_remaining")
            used = credits_audit.get("astroway_credits_used")
            lim = credits_audit.get("astroway_credits_limit", 50000)
            md.extend([
                f"| **Llamadas Efectuadas** | `{calls}` | {calls_detail} |",
                f"| **Créditos Gastados (Última llamada)** | `{used if used is not None else 'N/A'}` | Registrado en cabecera X-Credits-Used |",
                f"| **Créditos Restantes (Saldo)** | `{rem if rem is not None else 'N/A'}` / `{lim}` | Plan Indie PRO (50.000 créditos/mes) |"
            ])
        elif prov_low in ("freeastro", "freeastroapi"):
            rep_cred = credits_audit.get("freeastro_report_credits", "N/A")
            md.extend([
                f"| **Llamadas Efectuadas** | `{calls}` | {calls_detail} |",
                f"| **Créditos Reportados** | `{rep_cred}` | Estado de cuenta FreeAstro |",
                "| **Nivel de Servicio** | `Free Tier Dedicado` | Sin costo financiero |"
            ])
        elif prov_low in ("kundali", "kundali_mcp"):
            md.extend([
                f"| **Llamadas Efectuadas** | `{calls}` | {calls_detail} |",
                "| **Motor Jyotish** | `Kundali Remote MCP` | Precision Shodashavarga & Dashas |",
                "| **Autenticación** | `Bearer Token` | Akriti Engine 17.5.4 |"
            ])
        elif prov_low in ("lunar", "lunar_mcp"):
            md.extend([
                f"| **Llamadas Efectuadas** | `{calls}` | {calls_detail} |",
                "| **Motor Calendárico** | `Lunar Local MCP` | BaZi Cuatro Pilares & Huangli |",
                "| **Protocolo** | `stdio RPC` | Cálculo Solar Verdadero |"
            ])
        elif prov_low in ("zmanim", "zmanim_mcp"):
            md.extend([
                f"| **Llamadas Efectuadas** | `{calls}` | {calls_detail} |",
                "| **Motor Halájico** | `Zmanim Local MCP` | Tiempos de Oración & Shabat |",
                "| **Protocolo** | `stdio RPC` | Gr\"a / MGA |"
            ])
        else:
            md.append(f"| **Llamadas Efectuadas** | `{calls}` | {calls_detail} |")

        md.extend([
            "",
            "---",
            "",
            "## 2. Detalle Exhaustivo de Endpoints",
            "",
            "| # | Endpoint / Clave | Estado | Código HTTP | Latencia (ms) | Observaciones / Error |",
            "|---|---|---|---|---|---|"
        ])

        for idx, ep in enumerate(endpoints, 1):
            ep_name = ep.get("endpoint", "")
            ep_st = ep.get("status", "")
            ep_code = ep.get("http_status", "-")
            ep_lat = ep.get("latency_ms", 0.0)
            ep_err = ep.get("error") or "✅ OK"
            badge = "🟢 OK" if ep_st in ("SUCCESS", "CACHED") else ("🟡 THROTTLED" if ep_st == "THROTTLED" else f"🔴 {ep_st}")
            md.append(f"| {idx} | `{ep_name}` | {badge} | `{ep_code}` | `{ep_lat:.1f}` | {ep_err} |")

        md.append("")
        return "\n".join(md)

    def _render_lakehouse_markdown(self) -> None:
        """Reads all audit_*.json in self.audit_dir and produces the cumulative LAKEHOUSE_AUDIT.md."""
        lakehouse_file = self.audit_dir / "LAKEHOUSE_AUDIT.md"
        audit_files = sorted(self.audit_dir.glob("audit_*.json"))
        if not audit_files:
            return

        records = []
        for af in audit_files:
            try:
                with open(af, "r", encoding="utf-8") as f:
                    records.append(json.load(f))
            except Exception:
                pass

        if not records:
            return

        # Aggregate metrics
        consultant = records[0].get("consultant", "Unknown")
        latest_ts = max((r.get("timestamp_utc", "") for r in records), default="")
        total_endpoints = sum(r.get("total_endpoints", 0) for r in records)
        total_success = sum(r.get("success_count", 0) for r in records)
        total_failures = sum(r.get("failure_count", 0) for r in records)
        health_pct = round(total_success / max(1, total_endpoints) * 100, 1)

        md = [
            "# 🏛️ Data Lakehouse de Oráculo: Auditoría Consolidada y Acumulativa",
            "",
            "> **Registro Acumulativo Soberano de Ingesta Cruda (Bronze Layer - Multi-Proveedor)**  ",
            f"> **Consultante:** `{consultant}` | **Última Actualización:** `{latest_ts}`  ",
            f"> **Salud Global del Lakehouse:** `{health_pct}%` ({total_success}/{total_endpoints} endpoints exitosos)",
            "",
            "---",
            "",
            "## 1. Resumen Consolidado de Proveedores",
            "",
            "| Proveedor | Estado | Origen | Endpoints OK / Total | Latencia Total | Créditos Usados | Saldo Restante | Auditoría Individual |",
            "|---|---|---|---|---|---|---|---|"
        ]

        all_failures = []
        for r in records:
            prov = r.get("provider", "unknown").upper()
            prov_file = f"audit_{r.get('provider', '').lower()}.md"
            st = r.get("status", "UNKNOWN")
            is_c = r.get("is_cached", False)
            tot = r.get("total_endpoints", 0)
            succ = r.get("success_count", 0)
            lat = r.get("latency_ms", 0.0)
            cr = r.get("credits_audit", {})

            st_badge = "🟢 SUCCESS" if st == "SUCCESS" else ("🔵 CACHED" if st == "CACHED" else ("🟡 PARTIAL" if st == "PARTIAL" else f"🔴 {st}"))
            origin_str = "⚡ Caché" if is_c else "🌐 En Vivo"

            cr_used = "0 (Free)"
            cr_rem = "Ilimitado"
            if prov.lower() == "astroway":
                used_v = cr.get("astroway_credits_used")
                rem_v = cr.get("astroway_credits_remaining")
                cr_used = f"{used_v} créditos" if used_v is not None else "N/A"
                cr_rem = f"{rem_v} / {cr.get('astroway_credits_limit', 50000)}" if rem_v is not None else "50000"
            elif prov.lower() == "freeastro":
                cr_used = "0 (Free Tier)"
                cr_rem = str(cr.get("freeastro_report_credits", "Activo"))
            elif prov.lower() == "vedastro":
                cr_used = "0 (PRO Unlimited)"
                cr_rem = "Ilimitado"

            md.append(f"| **{prov}** | {st_badge} | {origin_str} | `{succ}/{tot}` | `{lat:.1f} ms` | `{cr_used}` | `{cr_rem}` | [`{prov_file}`]({prov_file}) |")

            for ep in r.get("endpoints", []):
                if ep.get("status") == "FAILED":
                    all_failures.append({
                        "provider": prov,
                        "endpoint": ep.get("endpoint"),
                        "http_status": ep.get("http_status"),
                        "error": ep.get("error")
                    })

        md.extend([
            "",
            "---",
            "",
            "## 2. Diagnóstico de Salud & Anomalías",
            ""
        ])

        if not all_failures:
            md.extend([
                "✅ **Cero fallas detectadas en el Data Lakehouse.** Todos los proveedores y endpoints auditados respondieron con integridad 100% (HTTP 200 OK).",
                "",
                "> **Garantía Inmutable de Pago Único:** Todos los datos ingestados residen en `raw/json/cache/` indexados por hash del consultante. Las ejecuciones futuras hidratarán desde disco a costo computacional y financiero cero."
            ])
        else:
            md.extend([
                f"⚠️ **Se detectaron {len(all_failures)} fallas en el Lakehouse:**",
                "",
                "| Proveedor | Endpoint | Código HTTP | Mensaje de Error |",
                "|---|---|---|---|",
            ])
            for f_item in all_failures:
                md.append(f"| **{f_item['provider']}** | `{f_item['endpoint']}` | `{f_item['http_status']}` | `{f_item['error']}` |")

        md.append("")
        with open(lakehouse_file, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

    def hydrate_accumulated_data(
        self,
        client_data: dict,
        rest_results: Dict[str, Any],
        mcp_results: Dict[str, Any],
        results_list: List[ExtractionResult]
    ) -> None:
        """
        Additive Lakehouse Upsert:
        Inspects disk cache for all providers for this client and populates
        rest_results and mcp_results for any missing or empty entries.
        Ensures incremental runs (--apis) accumulate without destroying previous data.
        """
        client_hash = self.cache.generate_client_hash(client_data)
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

        # 1. Hydrate REST providers
        rest_specs = [
            ("freeastro", "full_extract"),
            ("astroway", "full_extract"),
            ("astrologyapi", "full_extract"),
            ("vedastro", "full_extract"),
            ("hebcal", "combined"),
            ("nasa", "asteroids")
        ]

        for prov, endpoint in rest_specs:
            if not rest_results.get(prov):
                cached = self.cache.get(prov, endpoint, client_hash)
                if cached:
                    if prov in ("freeastro", "astroway", "astrologyapi", "vedastro"):
                        data_payload = cached.get("data", cached) if isinstance(cached, dict) else cached
                    else:
                        data_payload = cached
                    if data_payload and isinstance(data_payload, dict):
                        rest_results[prov] = data_payload
                        for ep_k, ep_v in data_payload.items():
                            results_list.append(ExtractionResult(
                                provider=prov, endpoint_key=ep_k, status="CACHED",
                                data=ep_v if isinstance(ep_v, dict) else {"value": ep_v},
                                http_status=200
                            ))

        # 2. Hydrate MCP tools
        lunar_bazi_args = {"birth_datetime": f"{date_str} {hour:02d}:{minute:02d}", "timezone_offset": int(tz_offset)}
        lunar_bazi_legacy_args = {"birth_datetime": f"{date_str} {hour:02d}:{minute:02d}:00", "timezone_offset": int(tz_offset)}
        if not mcp_results.get("lunar_mcp_calculate_bazi"):
            cached_bazi = (
                self.cache.get("lunar", "calculate_bazi", lunar_bazi_args)
                or self.cache.get("lunar", "calculate_bazi", lunar_bazi_legacy_args)
                or self.cache.get("mcp", "lunar_calculate_bazi", lunar_bazi_args)
                or self.cache.get("mcp", "lunar_calculate_bazi", lunar_bazi_legacy_args)
            )
            if cached_bazi:
                mcp_results["lunar_mcp_calculate_bazi"] = cached_bazi
                results_list.append(ExtractionResult(provider="lunar_mcp", endpoint_key="calculate_bazi", status="CACHED", data=cached_bazi, http_status=200))

        lunar_stl_args = {"solar_date": date_str, "culture": "chinese"}
        if not mcp_results.get("lunar_mcp_solar_to_lunar"):
            cached_stl = self.cache.get("lunar", "solar_to_lunar", lunar_stl_args) or self.cache.get("mcp", "lunar_solar_to_lunar", lunar_stl_args)
            if cached_stl:
                mcp_results["lunar_mcp_solar_to_lunar"] = cached_stl
                results_list.append(ExtractionResult(provider="lunar_mcp", endpoint_key="solar_to_lunar", status="CACHED", data=cached_stl, http_status=200))

        lunar_lh_args = {"date": date_str, "culture": "chinese"}
        if not mcp_results.get("lunar_mcp_get_lucky_hours"):
            cached_lh = self.cache.get("lunar", "get_lucky_hours", lunar_lh_args) or self.cache.get("mcp", "lunar_get_lucky_hours", lunar_lh_args)
            if cached_lh:
                mcp_results["lunar_mcp_get_lucky_hours"] = cached_lh
                results_list.append(ExtractionResult(provider="lunar_mcp", endpoint_key="get_lucky_hours", status="CACHED", data=cached_lh, http_status=200))

        zm_args = {
            "location": city or "Unknown",
            "latitude": lat,
            "longitude": lng,
            "date": date_str,
            "time_zone": tz_str,
            "response_format": "json"
        }
        if not mcp_results.get("zmanim_mcp_daily_times"):
            cached_zm = self.cache.get("zmanim", "zmanim_get_daily_times", zm_args) or self.cache.get("mcp", "zmanim_zmanim_get_daily_times", zm_args)
            if cached_zm:
                mcp_results["zmanim_mcp_daily_times"] = cached_zm
                results_list.append(ExtractionResult(provider="zmanim_mcp", endpoint_key="daily_times", status="CACHED", data=cached_zm, http_status=200))

        kd_args = {
            "birth_datetime": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00",
            "latitude": float(lat),
            "longitude": float(lng),
            "school": "parashari",
            "locale": "en"
        }
        kd_legacy_args = {
            "birth_datetime": f"{date_str}T{hour:02d}:{minute:02d}:00",
            "latitude": float(lat),
            "longitude": float(lng),
            "timezone": tz_str,
            "ayanamsha": "lahiri",
            "calculation_type": "all"
        }
        if not mcp_results.get("kundali_mcp_kundali_calc"):
            cached_kd = (
                self.cache.get("kundali", "kundali", kd_args)
                or self.cache.get("kundali", "kundali", kd_legacy_args)
                or self.cache.get("mcp", "kundali_kundali", kd_args)
                or self.cache.get("mcp", "kundali_kundali", kd_legacy_args)
            )
            if cached_kd:
                mcp_results["kundali_mcp_kundali_calc"] = cached_kd
                results_list.append(ExtractionResult(provider="kundali_mcp", endpoint_key="kundali", status="CACHED", data=cached_kd, http_status=200))

        partner = client_data.get("partner")
        if partner and isinstance(partner, dict) and not mcp_results.get("kundali_mcp_kundali_milan"):
            p_dt = f"{partner.get('year', year):04d}-{partner.get('month', month):02d}-{partner.get('day', day):02d}T{partner.get('hour', hour):02d}:{partner.get('minute', minute):02d}:00"
            km_args = {
                "groom": {"birth_datetime": f"{date_str}T{hour:02d}:{minute:02d}:00", "latitude": lat, "longitude": lng},
                "bride": {"birth_datetime": p_dt, "latitude": float(partner.get("lat", lat)), "longitude": float(partner.get("lng", lng))},
                "school": "parashari",
                "locale": "en"
            }
            cached_km = self.cache.get("kundali", "kundali_milan", km_args) or self.cache.get("mcp", "kundali_kundali_milan", km_args)
            if cached_km:
                mcp_results["kundali_mcp_kundali_milan"] = cached_km
                results_list.append(ExtractionResult(provider="kundali_mcp", endpoint_key="kundali_milan", status="CACHED", data=cached_km, http_status=200))

    def get_coverage_status(self, client_data: dict) -> Dict[str, Any]:
        """Returns the presence of all required multi-tradition providers in cache."""
        client_hash = self.cache.generate_client_hash(client_data)
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

        fe_data = self.cache.get("freeastro", "full_extract", client_hash)
        fe_ok = bool(fe_data and isinstance(fe_data, dict) and len(fe_data.get("data", {})) >= 50)

        aw_data = self.cache.get("astroway", "full_extract", client_hash)
        aw_ok = bool(aw_data and isinstance(aw_data, dict) and len(aw_data.get("data", {})) >= 80)

        aa_data = self.cache.get("astrologyapi", "full_extract", client_hash)
        aa_ok = bool(aa_data and isinstance(aa_data, dict) and len(aa_data.get("data", {})) >= 5)

        va_data = self.cache.get("vedastro", "full_extract", client_hash)
        va_ok = bool(va_data and isinstance(va_data, dict) and len(va_data.get("data", {})) >= 6)

        zm_args = {
            "location": city or "Unknown",
            "latitude": lat,
            "longitude": lng,
            "date": date_str,
            "time_zone": tz_str,
            "response_format": "json"
        }
        kd_args = {
            "birth_datetime": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00",
            "latitude": float(lat),
            "longitude": float(lng),
            "school": "parashari",
            "locale": "en"
        }
        kd_legacy_args = {
            "birth_datetime": f"{date_str}T{hour:02d}:{minute:02d}:00",
            "latitude": float(lat),
            "longitude": float(lng),
            "timezone": tz_str,
            "ayanamsha": "lahiri",
            "calculation_type": "all"
        }

        lunar_ok = bool(
            self.cache.get("lunar", "calculate_bazi", {"birth_datetime": f"{date_str} {hour:02d}:{minute:02d}", "timezone_offset": int(tz_offset)})
            or self.cache.get("lunar", "calculate_bazi", {"birth_datetime": f"{date_str} {hour:02d}:{minute:02d}:00", "timezone_offset": int(tz_offset)})
            or self.cache.get("mcp", "lunar_calculate_bazi", {"birth_datetime": f"{date_str} {hour:02d}:{minute:02d}:00", "timezone_offset": int(tz_offset)})
        )
        zmanim_ok = bool(
            self.cache.get("zmanim", "zmanim_get_daily_times", zm_args)
            or self.cache.get("mcp", "zmanim_zmanim_get_daily_times", zm_args)
        )
        kundali_ok = bool(
            self.cache.get("kundali", "kundali", kd_args)
            or self.cache.get("kundali", "kundali", kd_legacy_args)
            or self.cache.get("mcp", "kundali_kundali", kd_args)
            or self.cache.get("mcp", "kundali_kundali", kd_legacy_args)
        )

        required = {
            "freeastro": fe_ok,
            "astroway": aw_ok,
            "astrologyapi": aa_ok,
            "vedastro": va_ok,
            "hebcal": bool(self.cache.get("hebcal", "combined", client_hash)),
            "nasa": bool(self.cache.get("nasa", "asteroids", client_hash)),
            "lunar_bazi": lunar_ok,
            "zmanim": zmanim_ok,
            "kundali": kundali_ok
        }
        missing = [k for k, v in required.items() if not v]
        return {
            "client_hash": client_hash,
            "status": "COMPLETE" if not missing else "PARTIAL",
            "coverage": required,
            "missing": missing,
            "pct": round((len(required) - len(missing)) / len(required) * 100, 1)
        }

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

        def should_run(*prov_aliases: str) -> bool:
            if not norm_apis and not norm_exclude:
                return True
            for prov in prov_aliases:
                if prov.lower() in norm_exclude:
                    return False
            if not norm_apis:
                return True
            return any(prov.lower() in norm_apis for prov in prov_aliases)

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
        bazi_datetime_str = f"{date_str} {hour:02d}:{minute:02d}"

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
            "astrologyapi_plan": "Free Tier Dedicated (5 curated jewels)"
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
                if fn_freeastro and should_run("freeastro", "freeastroapi"):
                    # Check cache first (reject poisoned entries and require complete catalog)
                    explicit_run = bool(norm_apis and any(p in norm_apis for p in ["freeastro", "freeastroapi"]))
                    cached = self.cache.get("freeastro", "full_extract", client_cache_key) if not self.refresh_pro else None
                    if cached and isinstance(cached, dict) and "data" in cached and not explicit_run:
                        cached_has_err = bool(cached.get("failures")) or any(
                            isinstance(v, dict) and ("error" in v or v.get("status") == "FAIL")
                            for v in cached.get("data", {}).values()
                        )
                        if not cached_has_err and len(cached.get("data", {})) >= 50:
                            rest_results["freeastro"] = cached.get("data", {})
                            credit_stats["freeastro_report_credits"] = cached.get("report_credits")
                            credit_stats["calls_made"]["freeastro"] = 0
                            credit_stats["cache_hits"]["freeastro"] = 1
                            for ep_k, ep_data in cached.get("data", {}).items():
                                results_list.append(ExtractionResult(
                                    provider="freeastro", endpoint_key=ep_k,
                                    status="CACHED", data=ep_data, http_status=200, latency_ms=0.0
                                ))
                            self._save_micro_audit("freeastro", "CACHED", results_list, credit_stats, client_data, latency_ms=0.0, is_cached=True)
                            return

                    t0 = asyncio.get_event_loop().time()
                    elapsed = 0.0
                    has_err = False
                    try:
                        res = await fn_freeastro(
                            client_data,
                            client=http_client,
                            cache_manager=self.cache,
                            client_hash=client_cache_key
                        )
                        elapsed = (asyncio.get_event_loop().time() - t0) * 1000.0

                        # Cumulative Additive Merge:
                        accumulated = self.cache.get_all_provider_endpoints("freeastro", client_cache_key)
                        for ep_k, ep_v in res.get("data", {}).items():
                            if isinstance(ep_v, dict) and (ep_v.get("status") == "FAIL" or "error" in ep_v):
                                continue
                            accumulated[ep_k] = ep_v

                        rest_results["freeastro"] = accumulated
                        res["data"] = accumulated

                        credit_stats["freeastro_report_credits"] = res.get("report_credits")
                        credit_stats["calls_made"]["freeastro"] = res.get("calls_made", 0)

                        has_err = bool(res.get("failures")) or res.get("status") == "FAILED"

                        # Persist cumulative cache if we have gathered valid endpoints (>= 5)
                        if len(accumulated) >= 5:
                            self.cache.set("freeastro", "full_extract", client_cache_key, res, http_status=200)

                        if res.get("endpoint_audits"):
                            for ep_audit in res["endpoint_audits"]:
                                results_list.append(ExtractionResult(
                                    provider="freeastro",
                                    endpoint_key=ep_audit["endpoint"],
                                    status=ep_audit["status"],
                                    data=res.get("data", {}).get(ep_audit["endpoint"], {}),
                                    http_status=ep_audit.get("http_status", 200),
                                    latency_ms=ep_audit.get("latency_ms", 0.0),
                                    error=ep_audit.get("error")
                                ))
                        else:
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
                        has_err = True
                        results_list.append(ExtractionResult(
                            provider="freeastro", endpoint_key="all", status="FAILED",
                            data={}, http_status=500, error=str(exc)
                        ))
                    self._save_micro_audit("freeastro", "FAILED" if has_err else "SUCCESS", results_list, credit_stats, client_data, latency_ms=elapsed, is_cached=False)

            # 2. Dispatch AstroWay
            async def _run_astroway():
                if fn_astroway and should_run("astroway"):
                    # Check cache first (reject poisoned entries and require complete catalog)
                    explicit_run = bool(norm_apis and any(p in norm_apis for p in ["astroway"]))
                    cached = self.cache.get("astroway", "full_extract", client_cache_key) if not self.refresh_pro else None
                    if cached and isinstance(cached, dict) and "data" in cached and not explicit_run:
                        cached_has_err = bool(cached.get("failures")) or any(
                            isinstance(v, dict) and ("error" in v or v.get("ok") is False)
                            for v in cached.get("data", {}).values()
                        )
                        if not cached_has_err and len(cached.get("data", {})) >= 80:
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
                            self._save_micro_audit("astroway", "CACHED", results_list, credit_stats, client_data, latency_ms=0.0, is_cached=True)
                            return

                    t0 = asyncio.get_event_loop().time()
                    elapsed = 0.0
                    has_err = False
                    try:
                        res = await fn_astroway(
                            client_data,
                            client=http_client,
                            cache_manager=self.cache,
                            client_hash=client_cache_key,
                            use_curated=True
                        )
                        elapsed = (asyncio.get_event_loop().time() - t0) * 1000.0

                        # Cumulative Additive Merge:
                        # Reconstruct or merge all atomic endpoints on disk for astroway & client
                        accumulated = self.cache.get_all_provider_endpoints("astroway", client_cache_key)
                        for ep_k, ep_v in res.get("data", {}).items():
                            if isinstance(ep_v, dict) and (ep_v.get("ok") is False or "error" in ep_v):
                                continue
                            accumulated[ep_k] = ep_v

                        rest_results["astroway"] = accumulated
                        res["data"] = accumulated

                        audit = res.get("credits_audit", {})
                        credit_stats["astroway_credits_remaining"] = audit.get("remaining")
                        credit_stats["astroway_credits_used"] = audit.get("used_last_call")
                        credit_stats["astroway_credits_limit"] = audit.get("limit", 50000)
                        credit_stats["calls_made"]["astroway"] = res.get("calls_made", 0)

                        has_err = bool(res.get("failures")) or res.get("status") == "FAILED"

                        # Persist cumulative cache if we have gathered valid endpoints
                        if len(accumulated) >= 20:
                            self.cache.set("astroway", "full_extract", client_cache_key, res, http_status=200)

                        if res.get("endpoint_audits"):
                            for ep_audit in res["endpoint_audits"]:
                                results_list.append(ExtractionResult(
                                    provider="astroway",
                                    endpoint_key=ep_audit["endpoint"],
                                    status=ep_audit["status"],
                                    data=res.get("data", {}).get(ep_audit["endpoint"], {}),
                                    http_status=ep_audit.get("http_status", 200),
                                    latency_ms=ep_audit.get("latency_ms", 0.0),
                                    error=ep_audit.get("error")
                                ))
                        else:
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
                        has_err = True
                        results_list.append(ExtractionResult(
                            provider="astroway", endpoint_key="all", status="FAILED",
                            data={}, http_status=500, error=str(exc)
                        ))
                    self._save_micro_audit("astroway", "FAILED" if has_err else "SUCCESS", results_list, credit_stats, client_data, latency_ms=elapsed, is_cached=False)

            # 3. Dispatch AstrologyAPI
            async def _run_astrology():
                if fn_astrology and should_run("astrologyapi", "astrology_api_io"):
                    # Check cache first (reject poisoned entries and require complete catalog)
                    explicit_run = bool(norm_apis and any(p in norm_apis for p in ["astrologyapi", "astrology_api_io"]))
                    cached = self.cache.get("astrologyapi", "full_extract", client_cache_key) if not self.refresh_pro else None
                    if cached and isinstance(cached, dict) and "data" in cached and not explicit_run:
                        cached_has_err = bool(cached.get("failures")) or any(
                            isinstance(v, dict) and "error" in v
                            for v in cached.get("data", {}).values()
                        )
                        if not cached_has_err and len(cached.get("data", {})) >= 5:
                            rest_results["astrologyapi"] = cached.get("data", {})
                            credit_stats["calls_made"]["astrologyapi"] = 0
                            credit_stats["cache_hits"]["astrologyapi"] = 1
                            for ep_k, ep_data in cached.get("data", {}).items():
                                results_list.append(ExtractionResult(
                                    provider="astrologyapi", endpoint_key=ep_k,
                                    status="CACHED", data=ep_data, http_status=200, latency_ms=0.0
                                ))
                            self._save_micro_audit("astrologyapi", "CACHED", results_list, credit_stats, client_data, latency_ms=0.0, is_cached=True)
                            return

                    t0 = asyncio.get_event_loop().time()
                    elapsed = 0.0
                    has_err = False
                    try:
                        res = await fn_astrology(
                            client_data,
                            client=http_client,
                            cache_manager=self.cache,
                            client_hash=client_cache_key
                        )
                        elapsed = (asyncio.get_event_loop().time() - t0) * 1000.0

                        # Cumulative Additive Merge:
                        accumulated = self.cache.get_all_provider_endpoints("astrologyapi", client_cache_key)
                        for ep_k, ep_v in res.get("data", {}).items():
                            if isinstance(ep_v, dict) and ("error" in ep_v or ep_v.get("status") == "FAIL"):
                                continue
                            accumulated[ep_k] = ep_v

                        rest_results["astrologyapi"] = accumulated
                        res["data"] = accumulated
                        credit_stats["calls_made"]["astrologyapi"] = res.get("calls_made", 0)

                        has_err = bool(res.get("failures")) or res.get("status") == "FAILED"

                        if len(accumulated) >= 3:
                            self.cache.set("astrologyapi", "full_extract", client_cache_key, res, http_status=200)

                        if res.get("endpoint_audits"):
                            for ep_audit in res["endpoint_audits"]:
                                results_list.append(ExtractionResult(
                                    provider="astrologyapi",
                                    endpoint_key=ep_audit["endpoint"],
                                    status=ep_audit["status"],
                                    data=res.get("data", {}).get(ep_audit["endpoint"], {}),
                                    http_status=ep_audit.get("http_status", 200),
                                    latency_ms=ep_audit.get("latency_ms", 0.0),
                                    error=ep_audit.get("error")
                                ))
                        else:
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
                        has_err = True
                        results_list.append(ExtractionResult(
                            provider="astrologyapi", endpoint_key="all", status="FAILED",
                            data={}, http_status=500, error=str(exc)
                        ))
                    self._save_micro_audit("astrologyapi", "FAILED" if has_err else "SUCCESS", results_list, credit_stats, client_data, latency_ms=elapsed, is_cached=False)

            # 4. Dispatch VedAstro
            async def _run_vedastro():
                if fn_vedastro and should_run("vedastro"):
                    # Check cache first (reject poisoned entries and require complete catalog)
                    explicit_run = bool(norm_apis and any(p in norm_apis for p in ["vedastro"]))
                    cached = self.cache.get("vedastro", "full_extract", client_cache_key) if not self.refresh_pro else None
                    if cached and isinstance(cached, dict) and "data" in cached and not explicit_run:
                        cached_has_err = bool(cached.get("failures")) or any(
                            isinstance(v, dict) and ("error" in v or v.get("status") == "FAIL")
                            for v in cached.get("data", {}).values()
                        )
                        if not cached_has_err and len(cached.get("data", {})) >= 6:
                            rest_results["vedastro"] = cached.get("data", {})
                            credit_stats["calls_made"]["vedastro"] = 0
                            credit_stats["cache_hits"]["vedastro"] = 1
                            for ep_k, ep_data in cached.get("data", {}).items():
                                results_list.append(ExtractionResult(
                                    provider="vedastro", endpoint_key=ep_k,
                                    status="CACHED", data=ep_data, http_status=200, latency_ms=0.0
                                ))
                            self._save_micro_audit("vedastro", "CACHED", results_list, credit_stats, client_data, latency_ms=0.0, is_cached=True)
                            return

                    t0 = asyncio.get_event_loop().time()
                    elapsed = 0.0
                    has_err = False
                    try:
                        res = await fn_vedastro(
                            client_data,
                            client=http_client,
                            cache_manager=self.cache,
                            client_hash=client_cache_key
                        )
                        elapsed = (asyncio.get_event_loop().time() - t0) * 1000.0

                        # Cumulative Additive Merge:
                        accumulated = self.cache.get_all_provider_endpoints("vedastro", client_cache_key)
                        for ep_k, ep_v in res.get("data", {}).items():
                            if isinstance(ep_v, dict) and ("error" in ep_v or ep_v.get("status") == "FAIL"):
                                continue
                            accumulated[ep_k] = ep_v

                        rest_results["vedastro"] = accumulated
                        res["data"] = accumulated
                        credit_stats["calls_made"]["vedastro"] = res.get("calls_made", 0)

                        has_err = bool(res.get("failures")) or res.get("status") == "FAILED"

                        if len(accumulated) >= 4:
                            self.cache.set("vedastro", "full_extract", client_cache_key, res, http_status=200)

                        if res.get("endpoint_audits"):
                            for ep_audit in res["endpoint_audits"]:
                                results_list.append(ExtractionResult(
                                    provider="vedastro",
                                    endpoint_key=ep_audit["endpoint"],
                                    status=ep_audit["status"],
                                    data=res.get("data", {}).get(ep_audit["endpoint"], {}),
                                    http_status=ep_audit.get("http_status", 200),
                                    latency_ms=ep_audit.get("latency_ms", 0.0),
                                    error=ep_audit.get("error")
                                ))
                        else:
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
                        has_err = True
                        results_list.append(ExtractionResult(
                            provider="vedastro", endpoint_key="all", status="FAILED",
                            data={}, http_status=500, error=str(exc)
                        ))
                    self._save_micro_audit("vedastro", "FAILED" if has_err else "SUCCESS", results_list, credit_stats, client_data, latency_ms=elapsed, is_cached=False)

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
                            z_url = f"https://www.hebcal.com/zmanim?cfg=json&latitude={lat}&longitude={lng}&date={date_str}&tzid={tz_str}"
                            resp = await http_client.get(z_url, headers={"User-Agent": "GentleAI-Hebcal/1.0"})
                            d = resp.json()
                            rest_results["hebcal"]["zmanim"] = d
                            results_list.append(ExtractionResult(provider="hebcal", endpoint_key="zmanim", status="SUCCESS", data=d, http_status=200))
                        except Exception as e:
                            results_list.append(ExtractionResult(provider="hebcal", endpoint_key="zmanim", status="FAILED", data={}, error=str(e)))
                        
                        if rest_results["hebcal"].get("converter") and rest_results["hebcal"].get("zmanim"):
                            self.cache.set("hebcal", "combined", client_cache_key, rest_results["hebcal"], http_status=200)
                    self._save_micro_audit("hebcal", "SUCCESS", results_list, credit_stats, client_data, latency_ms=0.0, is_cached=bool(cached_heb))

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
                                    raw_text = h_json.get("result", "")
                                    ephem_table = ""
                                    if "$$SOE" in raw_text and "$$EOE" in raw_text:
                                        ephem_table = raw_text.split("$$SOE")[1].split("$$EOE")[0].strip()
                                    d_ast = {
                                        "name": ast_name.capitalize(),
                                        "horizons_result": raw_text[:500],
                                        "ephemeris_table": ephem_table or raw_text
                                    }
                                    rest_results["nasa"][f"asteroid_{ast_name}"] = d_ast
                                    results_list.append(ExtractionResult(provider="nasa", endpoint_key=f"asteroid_{ast_name}", status="SUCCESS", data=d_ast, http_status=200))
                                else:
                                    results_list.append(ExtractionResult(provider="nasa", endpoint_key=f"asteroid_{ast_name}", status="FAILED", data={}, http_status=h_res.status_code, error=f"HTTP {h_res.status_code}"))
                            except Exception as e:
                                results_list.append(ExtractionResult(provider="nasa", endpoint_key=f"asteroid_{ast_name}", status="FAILED", data={}, error=str(e)))
                        if rest_results["nasa"]:
                            self.cache.set("nasa", "asteroids", client_cache_key, rest_results["nasa"], http_status=200)
                    self._save_micro_audit("nasa", "SUCCESS", results_list, credit_stats, client_data, latency_ms=0.0, is_cached=bool(cached_nasa))

            # 6. Dispatch MCPs
            async def _run_mcps():
                run_lunar = should_run("lunar", "mcp")
                run_zmanim = should_run("zmanim", "mcp")
                run_kundali = should_run("kundali", "mcp")

                if not (run_lunar or run_zmanim or run_kundali):
                    return

                if run_lunar:
                    lunar_bazi_args = {"birth_datetime": bazi_datetime_str, "timezone_offset": int(tz_offset)}
                    lunar_bazi_legacy_args = {"birth_datetime": f"{bazi_datetime_str}:00", "timezone_offset": int(tz_offset)}
                    cached_bazi = self.cache.get("lunar", "calculate_bazi", lunar_bazi_args) or self.cache.get("lunar", "calculate_bazi", lunar_bazi_legacy_args) or self.cache.get("mcp", "lunar_calculate_bazi", lunar_bazi_args) or self.cache.get("mcp", "lunar_calculate_bazi", lunar_bazi_legacy_args)

                    lunar_stl_args = {"solar_date": date_str, "culture": "chinese"}
                    cached_stl = self.cache.get("lunar", "solar_to_lunar", lunar_stl_args) or self.cache.get("mcp", "lunar_solar_to_lunar", lunar_stl_args)

                    lunar_lh_args = {"date": date_str, "culture": "chinese"}
                    cached_lh = self.cache.get("lunar", "get_lucky_hours", lunar_lh_args) or self.cache.get("mcp", "lunar_get_lucky_hours", lunar_lh_args)

                    lunar_all_cached = bool(cached_bazi and cached_stl and cached_lh) and not self.refresh_pro

                    try:
                        bazi_res = cached_bazi if lunar_all_cached else await mcp_client.call_tool("lunar", "calculate_bazi", lunar_bazi_args)
                        mcp_results["lunar_mcp_calculate_bazi"] = bazi_res
                        results_list.append(ExtractionResult(provider="lunar", endpoint_key="calculate_bazi", status="CACHED" if lunar_all_cached else "SUCCESS", data=bazi_res, http_status=200))
                    except Exception as e:
                        results_list.append(ExtractionResult(provider="lunar", endpoint_key="calculate_bazi", status="FAILED", data={}, error=str(e)))

                    try:
                        stl_res = cached_stl if lunar_all_cached else await mcp_client.call_tool("lunar", "solar_to_lunar", lunar_stl_args)
                        mcp_results["lunar_mcp_solar_to_lunar"] = stl_res
                        results_list.append(ExtractionResult(provider="lunar", endpoint_key="solar_to_lunar", status="CACHED" if lunar_all_cached else "SUCCESS", data=stl_res, http_status=200))
                    except Exception as e:
                        results_list.append(ExtractionResult(provider="lunar", endpoint_key="solar_to_lunar", status="FAILED", data={}, error=str(e)))

                    try:
                        lh_res = cached_lh if lunar_all_cached else await mcp_client.call_tool("lunar", "get_lucky_hours", lunar_lh_args)
                        mcp_results["lunar_mcp_get_lucky_hours"] = lh_res
                        results_list.append(ExtractionResult(provider="lunar", endpoint_key="get_lucky_hours", status="CACHED" if lunar_all_cached else "SUCCESS", data=lh_res, http_status=200))
                    except Exception as e:
                        results_list.append(ExtractionResult(provider="lunar", endpoint_key="get_lucky_hours", status="FAILED", data={}, error=str(e)))

                    self._save_micro_audit("lunar", "SUCCESS", results_list, credit_stats, client_data, latency_ms=0.0, is_cached=lunar_all_cached)

                if run_zmanim:
                    zm_args = {
                        "location": city or "Unknown",
                        "latitude": lat,
                        "longitude": lng,
                        "date": date_str,
                        "time_zone": tz_str,
                        "response_format": "json"
                    }
                    cached_zm = self.cache.get("zmanim", "zmanim_get_daily_times", zm_args) or self.cache.get("mcp", "zmanim_zmanim_get_daily_times", zm_args)
                    zmanim_cached = bool(cached_zm) and not self.refresh_pro

                    try:
                        zm_res = cached_zm if zmanim_cached else await mcp_client.call_tool("zmanim", "zmanim_get_daily_times", zm_args)
                        mcp_results["zmanim_mcp_daily_times"] = zm_res
                        results_list.append(ExtractionResult(provider="zmanim", endpoint_key="daily_times", status="CACHED" if zmanim_cached else "SUCCESS", data=zm_res, http_status=200))
                    except Exception as e:
                        results_list.append(ExtractionResult(provider="zmanim", endpoint_key="daily_times", status="FAILED", data={}, error=str(e)))

                    self._save_micro_audit("zmanim", "SUCCESS", results_list, credit_stats, client_data, latency_ms=0.0, is_cached=zmanim_cached)

                if run_kundali:
                    kd_args = {
                        "birth_datetime": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00",
                        "latitude": float(lat),
                        "longitude": float(lng),
                        "school": "parashari",
                        "locale": "en"
                    }
                    cached_kd = self.cache.get("kundali", "kundali", kd_args) or self.cache.get("mcp", "kundali_kundali", kd_args)
                    partner = client_data.get("partner")
                    cached_km = None
                    km_args = None
                    if partner and isinstance(partner, dict):
                        p_dt = f"{partner.get('year', year):04d}-{partner.get('month', month):02d}-{partner.get('day', day):02d}T{partner.get('hour', hour):02d}:{partner.get('minute', minute):02d}:00"
                        km_args = {
                            "groom": {"birth_datetime": iso_local_str, "latitude": lat, "longitude": lng},
                            "bride": {"birth_datetime": p_dt, "latitude": float(partner.get("lat", lat)), "longitude": float(partner.get("lng", lng))},
                            "school": "parashari",
                            "locale": "en"
                        }
                        cached_km = self.cache.get("kundali", "kundali_milan", km_args) or self.cache.get("mcp", "kundali_kundali_milan", km_args)

                    kundali_cached = bool(cached_kd) and (cached_km is not None or not partner) and not self.refresh_pro

                    try:
                        kd_res = cached_kd if kundali_cached else await mcp_client.call_tool("kundali", "kundali", kd_args)
                        mcp_results["kundali_mcp_kundali_calc"] = kd_res
                        results_list.append(ExtractionResult(provider="kundali", endpoint_key="kundali_calc", status="CACHED" if kundali_cached else "SUCCESS", data=kd_res, http_status=200))
                    except Exception as e:
                        results_list.append(ExtractionResult(provider="kundali", endpoint_key="kundali_calc", status="FAILED", data={}, error=str(e)))

                    if partner and isinstance(partner, dict):
                        try:
                            km_res = cached_km if kundali_cached else await mcp_client.call_tool("kundali", "kundali_milan", km_args)
                            mcp_results["kundali_mcp_kundali_milan"] = km_res
                            results_list.append(ExtractionResult(provider="kundali", endpoint_key="kundali_milan", status="CACHED" if kundali_cached else "SUCCESS", data=km_res, http_status=200))
                        except Exception as e:
                            results_list.append(ExtractionResult(provider="kundali", endpoint_key="kundali_milan", status="FAILED", data={}, error=str(e)))

                    self._save_micro_audit("kundali", "SUCCESS", results_list, credit_stats, client_data, latency_ms=0.0, is_cached=kundali_cached)

            # Execute all tasks concurrently in TaskGroup
            async with asyncio.TaskGroup() as tg:
                tg.create_task(_run_freeastro())
                tg.create_task(_run_astroway())
                tg.create_task(_run_astrology())
                tg.create_task(_run_vedastro())
                tg.create_task(_run_hebcal_nasa())
                tg.create_task(_run_mcps())

        # Hidratación acumulativa: fusionar respuestas previas desde el caché de disco
        self.hydrate_accumulated_data(client_data, rest_results, mcp_results, results_list)

        # Actualización de auditoría acumulativa consolidada en Markdown
        try:
            self._render_lakehouse_markdown()
        except Exception as exc:
            logger.warning(f"Could not render cumulative lakehouse markdown: {exc}")

        return {
            "client_data": client_data,
            "rest": rest_results,
            "mcp": mcp_results,
            "credit_stats": credit_stats,
            "extraction_results": results_list
        }
