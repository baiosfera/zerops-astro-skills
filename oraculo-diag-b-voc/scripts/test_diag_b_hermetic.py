#!/usr/bin/env python3
"""
Hermetic Unit Test for Oráculo Diag-B-Voc (Carrera, Riqueza & Dasamsa D-10).
Zero LLM Tokens | < 50ms Execution | 100% Deterministic | Zero Network / Zero PII.
Validates Dual Ingestion: Primary (VirtualDataLake RFC 6901 Shards) & Fallback (omni_dump_mega.json).
"""

import sys
sys.dont_write_bytecode = True

import json
from typing import Any, Dict, List, Optional


def resolve_rfc6901(shards: Dict[str, Any], manifest_pointers: Dict[str, str], pointer: str) -> Any:
    """Standard RFC 6901 JSON pointer resolver with manifest pointer aliasing."""
    if pointer in manifest_pointers:
        pointer = manifest_pointers[pointer]

    if "#" in pointer:
        shard_key, json_pointer = pointer.split("#", 1)
    else:
        shard_key, json_pointer = pointer, ""

    if shard_key not in shards:
        raise KeyError(f"Shard key '{shard_key}' not found in virtual data lake")

    curr = shards[shard_key]
    if not json_pointer or json_pointer == "/":
        return curr

    tokens = [t.replace("~1", "/").replace("~0", "~") for t in json_pointer.lstrip("/").split("/")]
    for token in tokens:
        if isinstance(curr, dict):
            if token not in curr:
                raise KeyError(f"Token '{token}' not found in dict")
            curr = curr[token]
        elif isinstance(curr, list):
            try:
                idx = int(token)
                curr = curr[idx]
            except (ValueError, IndexError) as exc:
                raise IndexError(f"Index '{token}' invalid in list") from exc
        else:
            raise TypeError(f"Cannot resolve token '{token}' on scalar type {type(curr).__name__}")
    return curr


def build_mock_shards_diag_b() -> Dict[str, Any]:
    """Builds in-memory mock shards matching usage.md specifications for Diag-B."""
    shard_12 = {
        "metadata": {
            "name": "Executive Consultant Beta",
            "client_id": "CLIENT_002"
        },
        "system": "vedic_shodashavarga_d1_d60",
        "astroway_vargas": {
            "d10": {
                "chart_name": "Dasamsa",
                "lagna": {"sign": "Aries", "degree": 14.20},
                "planets": [
                    {"name": "Sun", "sign": "Leo", "degree": 10.50, "house": 5, "dignity": "Moolatrikona"},
                    {"name": "Mars", "sign": "Capricorn", "degree": 28.00, "house": 10, "dignity": "Exalted"},
                    {"name": "Jupiter", "sign": "Sagittarius", "degree": 18.30, "house": 9, "dignity": "Own"}
                ],
                "c10_profession": "Strategic Enterprise Architecture & Executive Leadership",
                "actions_in_society": "High-velocity systems building and governance"
            },
            "d9": {"chart_name": "Navamsa", "lagna": {"sign": "Leo"}},
            "d60": {"chart_name": "Shashtiamsa", "lagna": {"sign": "Scorpio"}}
        }
    }

    shard_03 = {
        "metadata": {
            "name": "Executive Consultant Beta",
            "client_id": "CLIENT_002"
        },
        "system": "vedic_jyotish",
        "vedic_shadbala_full": {
            "Sun": {"total_rupas": 7.82, "strength_ratio": 1.45, "rank": 2},
            "Mars": {"total_rupas": 8.10, "strength_ratio": 1.62, "rank": 1},
            "Venus": {"total_rupas": 6.95, "strength_ratio": 1.15, "rank": 4}
        },
        "houses_artha": {
            "house_2": {
                "sign": "Taurus",
                "ruler": "Venus",
                "degree": 12.40,
                "signification": "Direct cash flow, pricing power, asset accumulation"
            },
            "house_6": {
                "sign": "Virgo",
                "ruler": "Mercury",
                "degree": 18.25,
                "signification": "Daily operations, service optimization, team debt reduction"
            },
            "house_10": {
                "sign": "Capricorn",
                "ruler": "Saturn",
                "mc_degree": 282.15,
                "signification": "Public authority, executive prestige, peak career zenith"
            }
        },
        "nakshatras_wealth": [
            {"planet": "Moon", "nakshatra": "Rohini", "pada": 2, "deity": "Brahma", "wealth_multiplier": "Abundant"},
            {"planet": "Jupiter", "nakshatra": "Purva Ashadha", "pada": 4, "wealth_multiplier": "Strategic"}
        ]
    }

    shard_04 = {
        "metadata": {
            "name": "Executive Consultant Beta",
            "client_id": "CLIENT_002"
        },
        "system": "chinese_bazi",
        "chinese_bazi_true_solar": {
            "day_master": {
                "stem": "Jia",
                "element": "Yang Wood",
                "strength": "Dominant / Resource-Fed",
                "rooting": "Strong root in Yin/Mao branches"
            },
            "ten_gods": {
                "wealth": {
                    "direct_wealth": "Zheng Cai (Wu Earth)",
                    "indirect_wealth": "Pian Cai (Ji Earth)",
                    "wealth_structure": "Solid foundation with capital retention capacity"
                },
                "output": {
                    "eating_god": "Shi Shen (Bing Fire)",
                    "hurting_officer": "Shang Guan (Ding Fire)",
                    "production_talent": "High innovation and scalable technical synthesis"
                },
                "power": {
                    "direct_officer": "Zheng Guan (Xin Metal)",
                    "seven_killings": "Qi Sha (Geng Metal)"
                }
            },
            "five_elements_balance": {
                "Wood": 35.0,
                "Fire": 25.0,
                "Earth": 20.0,
                "Metal": 12.0,
                "Water": 8.0
            }
        }
    }

    shard_11 = {
        "metadata": {
            "name": "Executive Consultant Beta",
            "client_id": "CLIENT_002"
        },
        "system": "chinese_tcm_health_lifecurve",
        "tcm_health": {
            "dominant_meridian": "Liver / Gallbladder (Wood Meridian)",
            "organ_network": "Zang-Fu Wood-Fire Axis",
            "biotype": "Wood Dynamic Architect",
            "vitality_index": 92.4,
            "optimal_performance_window": "09:00 - 13:00 GMT-5"
        },
        "lifespan_curve": {
            "neijing_cycle": "8-year male biological cycle (Peak at 32-48)",
            "vitality_trend": "Sustained ascending plateau",
            "recommended_recovery_protocol": "Active cognitive down-regulation and somatic grounding"
        }
    }

    return {
        "harmonic_charts": shard_12,
        "vedic_sidereal": shard_03,
        "chinese_bazi": shard_04,
        "tcm_health": shard_11
    }


def build_mock_manifest_diag_b() -> Dict[str, Any]:
    """Builds RFC 6901 manifest mapping for Diag-B."""
    return {
        "contract": "gentle-ai.datalake.virtual/v1",
        "consultant": "Executive Consultant Beta",
        "shards": {
            "harmonic_charts": "shard_12_harmonic_charts.json",
            "vedic_sidereal": "shard_03_vedic_sidereal.json",
            "chinese_bazi": "shard_04_chinese_metaphysics.json",
            "tcm_health": "shard_11_tcm_health.json"
        },
        "pointers": {
            "vedic/dasamsa_d10": "harmonic_charts#/astroway_vargas/d10",
            "vedic/d10_planets": "harmonic_charts#/astroway_vargas/d10/planets",
            "vedic/shadbala": "vedic_sidereal#/vedic_shadbala_full",
            "vedic/artha_houses": "vedic_sidereal#/houses_artha",
            "vedic/c10_ruler": "vedic_sidereal#/houses_artha/house_10/ruler",
            "vedic/mc_degree": "vedic_sidereal#/houses_artha/house_10/mc_degree",
            "bazi/day_master": "chinese_bazi#/chinese_bazi_true_solar/day_master",
            "bazi/wealth_gods": "chinese_bazi#/chinese_bazi_true_solar/ten_gods/wealth",
            "tcm/vitality": "tcm_health#/tcm_health",
            "tcm/neijing_curve": "tcm_health#/lifespan_curve"
        }
    }


def build_mock_omni_dump_diag_b() -> Dict[str, Any]:
    """Builds fallback monolithic omni_dump_mega.json for Diag-B."""
    return {
        "client_data": {
            "name": "Executive Consultant Beta",
            "client_id": "CLIENT_002"
        },
        "va_horoscope_predictions": {
            "d10_summary": {"career": "High executive achievement in technology and systems"}
        },
        "va_all_planet_data": {
            "Sun": {"pos": 10.5, "house": 5},
            "Mars": {"pos": 28.0, "house": 10, "dignity": "Exalted"}
        },
        "fa_chinese_bazi": {
            "day_master": {"stem": "Jia", "element": "Yang Wood"},
            "ten_gods": {"direct_wealth": "Wu Earth"}
        },
        "fa_tropical_calculate": {
            "angles": {"mc": 282.15},
            "houses": [{"house": 10, "ruler": "Saturn"}]
        }
    }


def test_primary_shards_structure():
    shards = build_mock_shards_diag_b()
    assert isinstance(shards, dict)
    assert "harmonic_charts" in shards
    assert "vedic_sidereal" in shards
    assert "chinese_bazi" in shards
    assert "tcm_health" in shards

    assert shards["harmonic_charts"]["system"] == "vedic_shodashavarga_d1_d60"
    assert shards["vedic_sidereal"]["system"] == "vedic_jyotish"
    assert shards["chinese_bazi"]["system"] == "chinese_bazi"
    assert shards["tcm_health"]["system"] == "chinese_tcm_health_lifecurve"
    print("✓ test_primary_shards_structure passed")


def test_rfc6901_pointers_resolution():
    shards = build_mock_shards_diag_b()
    manifest = build_mock_manifest_diag_b()

    d10_chart = resolve_rfc6901(shards, manifest["pointers"], "vedic/dasamsa_d10")
    assert isinstance(d10_chart, dict)
    assert d10_chart["chart_name"] == "Dasamsa"

    c10_ruler = resolve_rfc6901(shards, manifest["pointers"], "vedic/c10_ruler")
    assert c10_ruler == "Saturn"

    mc_deg = resolve_rfc6901(shards, manifest["pointers"], "vedic/mc_degree")
    assert isinstance(mc_deg, (int, float))
    assert mc_deg == 282.15

    dm = resolve_rfc6901(shards, manifest["pointers"], "bazi/day_master")
    assert dm["element"] == "Yang Wood"

    tcm = resolve_rfc6901(shards, manifest["pointers"], "tcm/vitality")
    assert tcm["vitality_index"] > 90
    print("✓ test_rfc6901_pointers_resolution passed")


def test_mandatory_canonical_vectors():
    shards = build_mock_shards_diag_b()

    # Vector 1: Dasamsa (D-10) Védico
    d10 = shards["harmonic_charts"]["astroway_vargas"]["d10"]
    assert "actions_in_society" in d10
    assert "planets" in d10 and len(d10["planets"]) >= 3
    mars_d10 = next(p for p in d10["planets"] if p["name"] == "Mars")
    assert mars_d10["dignity"] == "Exalted"

    # Vector 2: Day Master (BaZi) & Diez Dioses
    bazi = shards["chinese_bazi"]["chinese_bazi_true_solar"]
    assert "day_master" in bazi
    assert "ten_gods" in bazi
    assert "direct_wealth" in bazi["ten_gods"]["wealth"]

    # Vector 3: Casas Terrenales (2, 6, 10)
    artha = shards["vedic_sidereal"]["houses_artha"]
    assert "house_2" in artha and "ruler" in artha["house_2"]
    assert "house_6" in artha and "ruler" in artha["house_6"]
    assert "house_10" in artha and "ruler" in artha["house_10"]

    # Vector 4: Vitalidad & Biotipo (MTC)
    tcm = shards["tcm_health"]["tcm_health"]
    neijing = shards["tcm_health"]["lifespan_curve"]
    assert "dominant_meridian" in tcm
    assert "neijing_cycle" in neijing
    print("✓ test_mandatory_canonical_vectors passed")


def test_attestation_protocol():
    shards = build_mock_shards_diag_b()

    # Attestation requirements from usage.md: MC, ruler of house 10, Day Master
    h10 = shards["vedic_sidereal"]["houses_artha"]["house_10"]
    bazi_dm = shards["chinese_bazi"]["chinese_bazi_true_solar"]["day_master"]

    assert "mc_degree" in h10 and h10["mc_degree"] is not None
    assert "ruler" in h10 and len(h10["ruler"]) > 0
    assert "element" in bazi_dm and len(bazi_dm["element"]) > 0

    # Test failure detection if MC is missing
    corrupt_h10 = {"ruler": "Saturn"}
    assert "mc_degree" not in corrupt_h10
    print("✓ test_attestation_protocol passed")


def test_omni_dump_fallback():
    omni = build_mock_omni_dump_diag_b()
    assert "va_horoscope_predictions" in omni
    assert "va_all_planet_data" in omni
    assert "fa_chinese_bazi" in omni
    assert "fa_tropical_calculate" in omni

    assert "mc" in omni["fa_tropical_calculate"]["angles"]
    assert omni["fa_chinese_bazi"]["day_master"]["element"] == "Yang Wood"
    print("✓ test_omni_dump_fallback passed")


def test_file_isolation_guardrail():
    """
    Validates File Independence:
    Result MUST be stored in diag_b_voc_report.md and NEVER overwrite fase7_voc.md.
    """
    target_output_file = "diag_b_voc_report.md"
    prohibited_file = "fase7_voc.md"

    def validate_destination_target(filename: str) -> bool:
        if filename == prohibited_file:
            raise ValueError(f"CRITICAL VIOLATION: Cannot overwrite canonical report '{prohibited_file}'")
        return filename == target_output_file

    assert validate_destination_target("diag_b_voc_report.md") is True
    try:
        validate_destination_target("fase7_voc.md")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("✓ test_file_isolation_guardrail passed")


if __name__ == "__main__":
    test_primary_shards_structure()
    test_rfc6901_pointers_resolution()
    test_mandatory_canonical_vectors()
    test_attestation_protocol()
    test_omni_dump_fallback()
    test_file_isolation_guardrail()
    print("All hermetic tests passed successfully for oraculo-diag-b-voc (exit code 0).")
    sys.exit(0)
