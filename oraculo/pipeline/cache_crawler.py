#!/usr/bin/env python3
"""
cache_crawler.py — Universal Dynamic Cache Crawler & Semantic Ingester for Oráculo.
Zero Hardcoded Endpoints | 100% Dynamic Discovery | Payload Signature Deduplication.

Traverses raw/json/cache/ across all provider folders (astroway, freeastroapi, vedastro,
astrology_api_io, bazi_mcp, zmanim_mcp, kundali_mcp, hebcal, nasa, and future engines),
deduplicates identical payload signatures, and categorizes files into normalized domain buckets.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Set, Tuple

logger = logging.getLogger("oraculo.cache_crawler")

PROVIDER_CANONICAL_MAP = {
    "astroway": "astroway",
    "freeastroapi": "freeastroapi",
    "freeastro": "freeastroapi",
    "vedastro": "vedastro",
    "astrology_api_io": "astrologyapi",
    "astrologyapi": "astrologyapi",
    "bazi_mcp": "bazi_mcp",
    "bazi": "bazi_mcp",
    "zmanim_mcp": "zmanim_mcp",
    "zmanim": "zmanim_mcp",
    "kundali_mcp": "kundali_mcp",
    "kundali": "kundali_mcp",
    "hebcal": "hebcal",
    "nasa": "nasa",
}

ALIAS_CANONICAL_MAP = {
    # FreeAstroAPI semantic alias normalization
    "western_natal_tropical": "natal_calculate",
    "freeastro_western_natal_tropical": "freeastro_natal_calculate",
    "chinese_bazi_true_solar": "chinese_bazi",
    "freeastro_chinese_bazi_true_solar": "freeastro_chinese_bazi",
    "western_astrocartography_lines": "astrocartography_lines",
    "freeastro_western_astrocartography_lines": "freeastro_astrocartography_lines",
    "vedic_kp_v2": "vedic_kp",
    "freeastro_vedic_kp_v2": "freeastro_vedic_kp",
    "western_numerology_profile": "numerology_profile",
    "freeastro_western_numerology_profile": "freeastro_numerology_profile",
}


def unwrap_payload(content: Any) -> Any:
    """Recursively unwraps response envelopes (_provider, data, ok, xml_parsed) without losing data."""
    if isinstance(content, dict):
        if "_provider" in content and "data" in content and isinstance(content["data"], (dict, list)):
            return unwrap_payload(content["data"])
        if "ok" in content and "data" in content and isinstance(content["data"], (dict, list)):
            return unwrap_payload(content["data"])
        if "xml_parsed" in content and isinstance(content["xml_parsed"], (dict, list)):
            return unwrap_payload(content["xml_parsed"])
        if len(content) == 1 and "data" in content and isinstance(content["data"], (dict, list)):
            return unwrap_payload(content["data"])
    return content


def compute_payload_hash(data: Any) -> str:
    """Computes a deterministic hash of JSON payload structure for deduplication."""
    try:
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    except Exception:
        return ""


class CacheCrawler:
    """
    Dynamically crawls and indexes all cached JSON files in a client's raw/json/cache directory.
    Provides semantic lookup, deduplication, and domain aggregation across all providers.
    """

    def __init__(self, cache_root: Path | str):
        self.cache_root = Path(cache_root).resolve()
        self.indexed_files: List[Dict[str, Any]] = []
        self.payload_signatures: Set[str] = set()
        self.domain_buckets: Dict[str, List[Dict[str, Any]]] = {
            "numerology": [],
            "western": [],
            "sidereal": [],
            "vedic": [],
            "bazi": [],
            "kabbalah": [],
            "hd_cosmobiology": [],
            "acg": [],
            "timing": [],
            "misc": [],
        }
        self._crawled = False

    def crawl(self) -> CacheCrawler:
        """Walks the entire cache directory recursively, indexing all valid JSON files."""
        if not self.cache_root.exists() or not self.cache_root.is_dir():
            logger.warning(f"Cache root does not exist or is not a directory: {self.cache_root}")
            return self

        total_scanned = 0
        duplicates_skipped = 0

        for root_dir, _, files in os.walk(self.cache_root):
            for file_name in files:
                if not file_name.endswith(".json"):
                    continue

                total_scanned += 1
                file_path = Path(root_dir) / file_name

                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = json.load(f)
                except Exception as e:
                    logger.debug(f"Failed to read/parse {file_path}: {e}")
                    continue

                # Deduplication by payload signature (e.g. duplicate full extracts)
                p_hash = compute_payload_hash(content)
                is_duplicate = False
                if p_hash:
                    if p_hash in self.payload_signatures:
                        # Allow individual files if they provide distinct naming context,
                        # but flag for downstream priority
                        is_duplicate = True
                        duplicates_skipped += 1
                    else:
                        self.payload_signatures.add(p_hash)

                provider_raw = file_path.parent.name
                provider = PROVIDER_CANONICAL_MAP.get(provider_raw.lower(), provider_raw.lower())

                file_stem = file_path.stem.lower()
                canonical_alias = ALIAS_CANONICAL_MAP.get(file_stem, file_stem)

                entry = {
                    "path": str(file_path),
                    "file_name": file_name,
                    "file_stem": file_stem,
                    "canonical_alias": canonical_alias,
                    "provider": provider,
                    "content": unwrap_payload(content),
                    "raw_content": content,
                    "payload_hash": p_hash,
                    "is_duplicate_payload": is_duplicate,
                    "rel_path": str(file_path.relative_to(self.cache_root)),
                }

                self.indexed_files.append(entry)
                self._classify_entry(entry)

        self._crawled = True
        logger.info(
            f"Crawler indexed {len(self.indexed_files)} JSON files ({duplicates_skipped} duplicate payloads flagged) across {len(self.domain_buckets)} domains"
        )
        return self

    def _classify_entry(self, entry: Dict[str, Any]) -> None:
        """Classifies a cache entry into one or more domain buckets based on path, name, and keys."""
        fname = entry["file_name"].lower()
        rel_path = entry["rel_path"].lower()
        provider = entry["provider"]
        content = entry["content"]

        # Check content keys if content is a dict
        content_keys = set()
        if isinstance(content, dict):
            content_keys = {str(k).lower() for k in content.keys()}

        matched_domains = set()

        # 1. Numerology
        if any(k in fname or k in rel_path for k in ["numerolog", "pythagor", "chaldean", "kabalistic_numerology", "name_number", "life_path", "expression_number"]):
            matched_domains.add("numerology")
        if "numerology" in content_keys or "life_path_number" in content_keys or "expression_number" in content_keys:
            matched_domains.add("numerology")

        # 2. Western (Tropical & Psychological)
        if any(k in fname or k in rel_path for k in ["tropical", "placidus", "western", "psychological", "arroyo", "elements", "houses_placidus", "aspects_major", "ephemeris"]):
            matched_domains.add("western")
        if provider in ["astroway", "freeastroapi", "astrologyapi"] and any(k in content_keys for k in ["planets", "houses", "aspects", "elements_distribution"]):
            matched_domains.add("western")

        # 3. Sidereal (Fagan-Bradley, Campanus, Mundoscope)
        if any(k in fname or k in rel_path for k in ["sidereal", "fagan", "bradley", "campanus", "mundoscope", "malta", "ayanamsa"]):
            matched_domains.add("sidereal")

        # 4. Vedic (Jyotish, KP, Kundali, VedAstro, Shadbala, D1-D60)
        if provider in ["vedastro", "kundali_mcp"] or any(k in fname or k in rel_path for k in ["vedic", "jyotish", "kp_", "shadbala", "nakshatra", "vargas", "dasamsa", "d10", "kundali", "jaimini", "karakas", "yogas"]):
            matched_domains.add("vedic")
        if any(k in content_keys for k in ["shadbala", "sub_lord", "star_lord", "vargas", "planet_data"]):
            matched_domains.add("vedic")

        # 5. BaZi (Four Pillars, 10 Gods, Yong Shen, TCM)
        if provider == "bazi_mcp" or any(k in fname or k in rel_path for k in ["bazi", "four_pillars", "ten_gods", "shi_shen", "yong_shen", "huangli", "lunar_calendar", "tcm_health"]):
            matched_domains.add("bazi")
        if any(k in content_keys for k in ["four_pillars", "day_master", "ten_gods", "lucky_element"]):
            matched_domains.add("bazi")

        # 6. Kabbalah & Zmanim (HebCal, Tikkun, Gematria, Halachic times)
        if provider in ["zmanim_mcp", "hebcal"] or any(k in fname or k in rel_path for k in ["kabbalah", "tikkun", "gematria", "zmanim", "shabbat", "hebrew_date", "72_names", "sephirot"]):
            matched_domains.add("kabbalah")

        # 7. Human Design & Cosmobiology
        if any(k in fname or k in rel_path for k in ["human_design", "bodygraph", "gates", "channels", "centers", "cosmobiology", "dial_90", "uranian", "midpoints", "tnps"]):
            matched_domains.add("hd_cosmobiology")

        # 8. Astrocartography (ACG, Best Places, Local Space, GeoJSON)
        if any(k in fname or k in rel_path for k in ["acg", "astrocarto", "relocation", "best_places", "local_space", "planetary_lines", "world_lines", "cities"]):
            matched_domains.add("acg")

        # 9. Timing (Dashas, Firdaria, Profections, Transits, Timeline)
        if any(k in fname or k in rel_path for k in ["timing", "timeline", "dasha", "vimshottari", "firdaria", "profection", "zodiacal_releasing", "transits"]):
            matched_domains.add("timing")

        if not matched_domains:
            matched_domains.add("misc")

        for d in matched_domains:
            self.domain_buckets[d].append(entry)

    def get_domain_files(self, domain: str) -> List[Dict[str, Any]]:
        """Returns all indexed files belonging to a specific domain."""
        if not self._crawled:
            self.crawl()
        return self.domain_buckets.get(domain, [])

    def get_all_entries(self) -> List[Dict[str, Any]]:
        """Returns all indexed cache entries."""
        if not self._crawled:
            self.crawl()
        return self.indexed_files

    def get_stats(self) -> Dict[str, Any]:
        """Returns diagnostic crawl statistics."""
        if not self._crawled:
            self.crawl()
        return {
            "total_files": len(self.indexed_files),
            "unique_payloads": len(self.payload_signatures),
            "by_domain": {k: len(v) for k, v in self.domain_buckets.items()},
        }
