#!/usr/bin/env python3
"""
sharder.py — Clean-Room Gold Tier Compilation Orchestrator for Oráculo (v6.3).
Decoupled Architecture | Universal Cache Crawler | 12 Bronze Shards | 15 Silver Shards | 9 Gold Feeds.

Pure mathematical sharding and multi-provider feed synthesis.
Eradicates the legacy monolithic spaghetti sharder.py and eliminates duplicate files.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional

from pipeline.cache_crawler import CacheCrawler
from pipeline.domains.acg_domain import ACGDomain
from pipeline.domains.bazi_domain import BaZiDomain
from pipeline.domains.hd_cosmobiology_domain import HDCosmobiologyDomain
from pipeline.domains.kabbalah_domain import KabbalahDomain
from pipeline.domains.numerology_domain import NumerologyDomain
from pipeline.domains.sidereal_domain import SiderealDomain
from pipeline.domains.timing_domain import TimingDomain
from pipeline.domains.vedic_domain import VedicDomain
from pipeline.domains.western_domain import WesternDomain

logger = logging.getLogger("oraculo.sharder")


class ExtractionFatalError(Exception):
    """Raised when extraction output or cache is fatally corrupted."""
    pass


class SharderEngine:
    """
    Gold Tier Compilation Engine.
    Discovers all cached JSON files dynamically via CacheCrawler, coordinates the 9 domain engines,
    and produces 12 Bronze shards, 15 Silver relational shards, and 9 Encyclopedic Gold Feeds.
    """

    def __init__(self, output_root: Path | str):
        self.output_root = Path(output_root).resolve()
        self.raw_dir = self.output_root / "raw"
        self.cache_dir = self.raw_dir / "json" / "cache"
        self.dumps_dir = self.raw_dir / "json" / "dumps"
        self.feeds_dir = self.raw_dir / "feeds"
        self.llm_dir = self.raw_dir / "llm"

        # Ensure directory structure
        self.dumps_dir.mkdir(parents=True, exist_ok=True)
        self.feeds_dir.mkdir(parents=True, exist_ok=True)
        self.llm_dir.mkdir(parents=True, exist_ok=True)

    def verify_and_shard(self, extraction_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinates full Gold Tier compilation:
        1. Dynamic cache crawling and payload deduplication.
        2. Domain synthesis across 9 specialized engines.
        3. Sharding 12 physical JSON shards in dumps/.
        4. Compiling 15 relational shards in client_dumps_15_shards.json + manifest.json.
        5. Generating 9 Encyclopedic Gold Feeds in feeds/.
        6. Purging deprecated duplicate files.
        """
        client_payload = self._discover_client_profile(extraction_output)

        logger.info(f"Starting SharderEngine for client in {self.output_root}")

        # 1. Dynamic crawl of raw/json/cache/
        crawler = CacheCrawler(self.cache_dir).crawl()
        stats = crawler.get_stats()
        logger.info(f"Cache discovery stats: {stats}")

        # 2. Instantiate and synthesize Domain Engines
        num_engine = NumerologyDomain(crawler.get_domain_files("numerology"), client_payload)
        west_engine = WesternDomain(crawler.get_domain_files("western"), client_payload)
        west_data = west_engine.synthesize()

        sid_files = crawler.get_domain_files("sidereal") or crawler.get_domain_files("vedic")
        sid_engine = SiderealDomain(
            sid_files,
            client_payload,
            tropical_planets=west_data.get("planets"),
            tropical_houses=west_data.get("houses")
        )
        sid_data = sid_engine.synthesize()

        ved_engine = VedicDomain(crawler.get_domain_files("vedic"), client_payload)
        bazi_engine = BaZiDomain(crawler.get_domain_files("bazi"), client_payload)
        kab_engine = KabbalahDomain(crawler.get_domain_files("kabbalah"), client_payload)
        hd_engine = HDCosmobiologyDomain(crawler.get_domain_files("hd_cosmobiology"), client_payload)
        acg_engine = ACGDomain(crawler.get_domain_files("acg"), client_payload)
        tim_engine = TimingDomain(crawler.get_domain_files("timing"), client_payload)

        # 3. Synthesize remaining domain models
        num_data = num_engine.synthesize()
        ved_data = ved_engine.synthesize()
        bazi_data = bazi_engine.synthesize()
        kab_data = kab_engine.synthesize()
        hd_data = hd_engine.synthesize()
        acg_data = acg_engine.synthesize()
        tim_data = tim_engine.synthesize()

        # 4. Generate 12 Bronze Physical Shards
        shards_12 = {
            "shard_01.json": {"name": "Western Tropical Placidus", "data": west_data},
            "shard_02.json": {"name": "Western Sidereal Fagan-Bradley", "data": sid_data},
            "shard_03.json": {"name": "Vedic Jyotish KP & Shadbala", "data": ved_data},
            "shard_04.json": {"name": "Chinese BaZi Four Pillars", "data": bazi_data},
            "shard_05.json": {"name": "Human Design BodyGraph", "data": hd_data.get("human_design", {})},
            "shard_06.json": {"name": "Kabbalah Zmanim & Tikkun", "data": kab_data},
            "shard_07.json": {"name": "Vocational D-10 & Artha Wealth", "data": {"vedic_vargas": ved_data.get("vargas"), "houses_wealth": west_data.get("tripod_of_iron")}},
            "shard_08.json": {"name": "Astrocartography ACG Lines", "data": acg_data},
            "shard_09.json": {"name": "Multi-System Numerology & Brands", "data": num_data},
            "shard_10.json": {"name": "Predictive Timing & Dashas", "data": tim_data},
            "shard_11.json": {"name": "Cosmobiology Dial 90 & Midpoints", "data": hd_data.get("cosmobiology_dial_90", {})},
            "shard_12.json": {"name": "TCM Five Elements Health Balance", "data": bazi_data.get("tcm_health", {})},
        }

        for fname, s_content in shards_12.items():
            shard_path = self.dumps_dir / fname
            with open(shard_path, "w", encoding="utf-8") as f:
                json.dump(s_content, f, indent=2, ensure_ascii=False)

        # 5. Compile 15 Silver Relational Shards & Manifest
        silver_shards = {f"shard_{i:02d}": shards_12.get(f"shard_{i:02d}.json", {}) for i in range(1, 13)}
        silver_shards["shard_13"] = {"name": "Client Profile & Master Geometry", "data": client_payload}
        silver_shards["shard_14"] = {"name": "Cross-System Synthesis & Epistemic Bridges", "data": {"dominant_element": west_data.get("arroyo_elements", {}).get("dominant_element"), "yong_shen": bazi_data.get("yong_shen", {}).get("element")}}
        silver_shards["shard_15"] = {"name": "Multi-Brand Vibrational Index", "data": num_data.get("brands", [])}

        with open(self.dumps_dir / "client_dumps_15_shards.json", "w", encoding="utf-8") as f:
            json.dump(silver_shards, f, indent=2, ensure_ascii=False)

        manifest = {
            "version": "6.3",
            "schema": "urn:oraculo:canon-12-15-9-4",
            "client": client_payload.get("name", "Consultant"),
            "consultant": client_payload.get("name", "Consultant"),
            "total_shards": 15,
            "physical_shards_dir": str(self.dumps_dir),
            "shards": {f"shard_{i:02d}": f"shard_{i:02d}.json" for i in range(1, 13)},
            "manifest_pointers": {k: f"/raw/json/dumps/client_dumps_15_shards.json#/{k}" for k in silver_shards.keys()}
        }
        with open(self.dumps_dir / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        # 6. Generate 9 Gold Encyclopedic Feeds
        feeds_map = {
            "feed_numerologia_enciclopedica.md": num_engine.render_markdown_feed(),
            "feed_occidental_tropical.md": west_engine.render_markdown_feed(),
            "feed_occidental_sideral_fagan.md": sid_engine.render_markdown_feed(),
            "feed_vedica_jyotish_kp.md": ved_engine.render_markdown_feed(),
            "feed_bazi_cuatro_pilares.md": bazi_engine.render_markdown_feed(),
            "feed_kabbalah_zmanim_tikkun.md": kab_engine.render_markdown_feed(),
            "feed_human_design_cosmobiologia.md": hd_engine.render_markdown_feed(),
            "feed_astrocartografia_acg.md": acg_engine.render_markdown_feed(),
            "feed_timing_dashas_ciclos.md": tim_engine.render_markdown_feed(),
        }

        for feed_name, feed_content in feeds_map.items():
            feed_path = self.feeds_dir / feed_name
            feed_path.write_text(feed_content, encoding="utf-8")

        # 7. Purge deprecated duplicate and junk files
        self._purge_deprecated_files()

        return {
            "shards_count": len(shards_12),
            "feeds_count": len(feeds_map),
            "silver_shards_count": len(silver_shards),
            "total_cached_files_scanned": stats["total_files"],
        }

    def _purge_deprecated_files(self) -> None:
        """Purges obsolete duplicate copies of brandbook and feeds from legacy runs."""
        # 1. Purge root brandbook.json and brandbook_*.json if present
        for f in self.output_root.glob("brandbook*.json"):
            try:
                f.unlink()
                logger.info(f"Purged deprecated root file: {f}")
            except Exception:
                pass

        # 2. Purge brandbook*.json and feed_astrobranding*.md from raw/feeds/
        for pattern in ["brandbook*.json", "feed_astrobranding*.md", "feed_fase0_author_dossier.md"]:
            for f in self.feeds_dir.glob(pattern):
                try:
                    f.unlink()
                    logger.info(f"Purged deprecated feeds file: {f}")
                except Exception:
                    pass

    def _discover_client_profile(self, extraction_output: Dict[str, Any]) -> Dict[str, Any]:
        """Discovers and parses client profile from extraction output, client_profile.json, or root markdown files."""
        client_payload = extraction_output.get("client_payload") or extraction_output.get("client_data", {})
        if client_payload:
            return client_payload

        # Check raw/client_profile.json
        prof_json = self.raw_dir / "client_profile.json"
        if prof_json.exists():
            try:
                with open(prof_json, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data and isinstance(data, dict):
                    return data
            except Exception:
                pass

        # Discover client markdown/text files in output_root (e.g. Damarén.md, Catalina.md)
        MONTHS_ES = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
            "julio": 7, "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10,
            "noviembre": 11, "diciembre": 12
        }
        CITY_GEO = {
            "bogota": (4.5882, -74.0854, "America/Bogota", "Bogota"),
            "bogotá": (4.5882, -74.0854, "America/Bogota", "Bogota"),
            "medellin": (6.2340, -75.5731, "America/Bogota", "Medellin"),
            "medellín": (6.2340, -75.5731, "America/Bogota", "Medellin"),
        }

        md_candidates = [
            f for f in self.output_root.glob("*.md")
            if not f.name.startswith(("feed_", "LAKEHOUSE", "extraction", "coach", "fase0", "astrobranding", "system"))
        ]
        if not md_candidates:
            md_candidates = list(self.output_root.glob("*.txt"))

        if md_candidates:
            target_md = md_candidates[0]
            try:
                lines = target_md.read_text(encoding="utf-8").splitlines()
                raw: Dict[str, str] = {}
                brands: List[str] = []
                in_brands = False
                for line in lines:
                    line_s = line.strip()
                    if not line_s:
                        continue
                    if re.match(r"^(marcas?|brands?)\s*:", line_s, re.I):
                        in_brands = True
                        v = line_s.split(":", 1)[1].strip()
                        if v:
                            brands.extend([b.strip() for b in v.split(",") if b.strip()])
                        continue
                    if in_brands:
                        m_b = re.match(r"^[-*•]\s*(.*)$", line_s)
                        if m_b:
                            brands.append(m_b.group(1).strip())
                            continue
                        elif ":" not in line_s:
                            brands.append(line_s)
                            continue
                        else:
                            in_brands = False
                    if ":" in line_s:
                        k, v = line_s.split(":", 1)
                        raw[k.strip().lower()] = v.strip()

                birth_name = raw.get("nombre de nacimiento") or raw.get("nombre") or "Consultant"
                current_name = raw.get("nombre actual (cambio)") or raw.get("nombre actual") or birth_name

                dob_raw = raw.get("fecha de nacimiento") or raw.get("fecha") or ""
                m_d = re.search(r"(\d{1,2})\s+(?:de\s+)?([a-zA-ZáéíóúÁÉÍÓÚñÑ]+)(?:\s+de)?\s+(\d{4})", dob_raw, re.I)
                y, m, d = 1990, 1, 1
                if m_d and m_d.group(2).lower() in MONTHS_ES:
                    y = int(m_d.group(3))
                    m = MONTHS_ES[m_d.group(2).lower()]
                    d = int(m_d.group(1))
                else:
                    m_iso = re.search(r"(\d{4})[-/. ](\d{1,2})[-/. ](\d{1,2})", dob_raw)
                    if m_iso:
                        y, m, d = int(m_iso.group(1)), int(m_iso.group(2)), int(m_iso.group(3))

                tob_raw = raw.get("hora") or raw.get("hora de nacimiento") or ""
                m_t = re.search(r"(\d{1,2}):(\d{2})\s*(am|pm)?", tob_raw, re.I)
                h, mn = 12, 0
                if m_t:
                    h = int(m_t.group(1))
                    mn = int(m_t.group(2))
                    ampm = m_t.group(3)
                    if ampm:
                        if ampm.lower() == "pm" and h < 12: h += 12
                        elif ampm.lower() == "am" and h == 12: h = 0

                ciudad_raw = raw.get("ciudad") or ""
                lat, lon, tz, city = 6.2442, -75.5812, "America/Bogota", "Medellin"
                for ck, cv in CITY_GEO.items():
                    if ck in ciudad_raw.lower():
                        lat, lon, tz, city = cv
                        break

                parsed_payload = {
                    "birth_name": birth_name,
                    "current_name": current_name,
                    "name": birth_name,
                    "preferred_name": current_name,
                    "year": y, "month": m, "day": d,
                    "hour": h, "minute": mn,
                    "lat": lat, "lng": lon,
                    "tz_str": tz, "tz_offset": -5.0,
                    "city": city,
                    "brand_names": brands if brands else [self.output_root.name]
                }
                # Persist client_profile.json
                with open(self.raw_dir / "client_profile.json", "w", encoding="utf-8") as f:
                    json.dump(parsed_payload, f, indent=2, ensure_ascii=False)
                return parsed_payload
            except Exception as e:
                logger.warning(f"Failed to parse client markdown {target_md}: {e}")

        return {}
