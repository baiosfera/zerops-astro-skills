#!/usr/bin/env python3
"""
Hermetic Unit Tests for Oráculo Pipeline SOTA v4.0 (Zero Network, Zero PII).
Validates configuration loading, canonical header resolution, rate limiting, and pure sharding.
"""

import sys
sys.dont_write_bytecode = True
from pathlib import Path
import tempfile
import shutil
import json

# Ensure skill root is in sys.path
SKILL_ROOT = Path(__file__).resolve().parent.parent
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from pipeline.config import config
from pipeline.clients.rest_client import UnifiedRestClient
from pipeline.rate_limiter import MultiProviderRateLimiter
from pipeline.resilience import CircuitBreaker
from pipeline.sharder import SharderEngine
from pipeline.data_lake import VirtualDataLake


def test_config_and_rate_limiter():
    assert config is not None
    # Verify rate limiter initializes all providers
    limiter = MultiProviderRateLimiter()
    for p in ["freeastro", "astroway", "astrologyapi", "vedastro", "hebcal", "nasa"]:
        assert p in limiter.limiters
    print("✓ test_config_and_rate_limiter passed")


def test_rest_client_headers():
    class DummyCache:
        def get(self, *args, **kwargs): return None
        def set(self, *args, **kwargs): pass

    client = UnifiedRestClient(cache_manager=DummyCache())
    # AstroWay requires X-Api-Key
    h_aw = client._resolve_canonical_headers("astroway", {"Authorization": "Bearer invalid"})
    assert "Authorization" not in h_aw
    assert "X-Api-Key" in h_aw or config.astroway_api_key is None

    # Astrology-API.io requires Authorization: Bearer
    h_aa = client._resolve_canonical_headers("astrologyapi", {"x-api-key": "invalid"})
    assert "x-api-key" not in h_aa
    assert "Authorization" in h_aa or config.astrology_api_key is None

    # FreeAstroAPI requires x-api-key
    h_fa = client._resolve_canonical_headers("freeastro", {})
    assert "Content-Type" in h_fa
    print("✓ test_rest_client_headers passed")


def test_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
    assert cb.allow_request() is True
    cb.record_failure()
    assert cb.allow_request() is True
    cb.record_failure()
    assert cb.allow_request() is False
    print("✓ test_circuit_breaker passed")


def test_sharder_engine_hermetic():
    temp_dir = tempfile.mkdtemp()
    try:
        mock_tropical = {
            "angles": {"asc": 250.9, "mc": 160.35},
            "planets": [
                {"name": "Sun", "sign": "Cap", "pos": 27.93, "house": 2, "retrograde": False},
                {"name": "Moon", "sign": "Tau", "pos": 2.36, "house": 5, "retrograde": False}
            ],
            "houses": [{"house": 1, "sign": "Sag"}, {"house": 2, "sign": "Cap"}]
        }
        extraction_output = {
            "client_data": {
                "name": "Hermetic Test Consultant",
                "preferred_name": "Test",
                "year": 1986, "month": 1, "day": 18,
                "hour": 3, "minute": 0,
                "lat": 6.234, "lng": -75.573,
                "tz_str": "America/Bogota",
                "brand_names": ["Test Brand"]
            },
            "rest": {
                "freeastro": {
                    "western_natal_tropical": mock_tropical,
                    "western_natal_sidereal": {"planets": [{"name": "Sun", "sign": "Cap", "pos": 4.12, "house": 2}]},
                    "numerology_profile_pythagorean": {"core_numbers": {"life_path": {"value": 7}}}
                },
                "astroway": {
                    "western_chart": {"ok": True},
                    "jaimini_chara_karakas": {"ok": True, "data": {"ranking": [{"role": "Atmakaraka", "grahaName": "Jupiter", "signName": "Capricorn", "longitudeInSign": 28.44}]}},
                    "evolutionary_skipped_steps": {"ok": True, "data": {"skippedSteps": []}},
                    "evolutionary_nodal_axis": {"ok": True, "data": {"northNode": {"sign": "Taurus", "longitude": 35.35}, "southNode": {"sign": "Scorpio", "longitude": 215.35}}}
                }
            },
            "mcp": {
                "lunar_mcp_calculate_bazi": {
                    "four_pillars": {
                        "year": {"stem": "Wood", "branch": "Ox", "animal": "Ox"},
                        "month": {"stem": "Earth", "branch": "Ox", "animal": "Ox"},
                        "day": {"stem": "Water", "branch": "Snake", "animal": "Snake"},
                        "hour": {"stem": "Metal", "branch": "Tiger", "animal": "Tiger"}
                    },
                    "day_master": {"element": "Water", "strength": "Balanced"}
                }
            },
            "credit_stats": {"calls_made": {"freeastro": 1}, "cache_hits": {}},
            "extraction_results": []
        }
        sharder = SharderEngine(output_root=temp_dir)
        res = sharder.verify_and_shard(extraction_output)
        assert res["shards_count"] == 12
        assert res["feeds_count"] == 10
        assert res["manifest_generated"] is True
        
        # Verify physical files
        dumps_dir = Path(temp_dir) / "raw" / "json" / "dumps"
        assert (dumps_dir / "shard_01_astro_western_tropical.json").exists()
        assert (dumps_dir / "shard_05_kabbalah_tikkun.json").exists()
        assert (dumps_dir / "manifest.json").exists()
        
        feeds_dir = Path(temp_dir) / "raw" / "feeds"
        assert (feeds_dir / "feed_fase0_author_dossier.md").exists()
        f2 = feeds_dir / "feed_fase2_occ.md"
        assert f2.exists()
        content = f2.read_text(encoding="utf-8")
        assert 'degree="27.93"' in content
        assert "0.0°" not in content
        print("✓ test_sharder_engine_hermetic passed")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_virtual_data_lake_hermetic():
    temp_dir = tempfile.mkdtemp()
    try:
        raw_dir = Path(temp_dir) / "raw"
        dumps_dir = raw_dir / "json" / "dumps"
        dumps_dir.mkdir(parents=True, exist_ok=True)
        
        # Write dummy shard
        s1 = {
            "metadata": {"name": "Lake Test"},
            "system": "western_tropical",
            "freeastro_tropical_placidus": {
                "angles": {"asc": 123.45},
                "planets": [{"name": "Sun", "pos": 28.5}]
            }
        }
        (dumps_dir / "shard_01_astro_western_tropical.json").write_text(json.dumps(s1), encoding="utf-8")
        
        manifest = {
            "contract": "gentle-ai.datalake.virtual/v1",
            "consultant": "Test Consultant",
            "shards": {
                "western_tropical": "shard_01_astro_western_tropical.json"
            },
            "pointers": {
                "tropical/ascendant": "western_tropical#/freeastro_tropical_placidus/angles/asc"
            }
        }
        (dumps_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        
        dl = VirtualDataLake(raw_dir=raw_dir)
        val = dl.get("tropical/ascendant")
        assert val == 123.45
        
        direct_val = dl.resolve_pointer("western_tropical#/freeastro_tropical_placidus/planets/0/name")
        assert direct_val == "Sun"
        
        # Test export
        export_path = raw_dir / "omni_dump_mega.json"
        res_path = dl.export_master_dump(out_path=export_path)
        assert res_path.exists()
        exported = json.loads(res_path.read_text(encoding="utf-8"))
        assert "shards" in exported
        assert "western_tropical" in exported["shards"]
        assert exported["shards"]["western_tropical"]["freeastro_tropical_placidus"]["angles"]["asc"] == 123.45
        print("✓ test_virtual_data_lake_hermetic passed")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    test_config_and_rate_limiter()
    test_rest_client_headers()
    test_circuit_breaker()
    test_sharder_engine_hermetic()
    test_virtual_data_lake_hermetic()
    print("All hermetic tests passed successfully (exit code 0).")

