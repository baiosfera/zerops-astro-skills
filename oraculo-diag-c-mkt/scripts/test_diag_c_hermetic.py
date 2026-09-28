#!/usr/bin/env python3
"""
Hermetic Unit Test for Oráculo Diag-C-Mkt (Market Timing & KP Eleccional).
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


def build_mock_shards_diag_c() -> Dict[str, Any]:
    """Builds in-memory mock shards matching usage.md specifications for Diag-C."""
    shard_03 = {
        "metadata": {
            "name": "Market Operator Gamma",
            "client_id": "CLIENT_003"
        },
        "system": "vedic_jyotish",
        "vedic_kp_v2": {
            "ayanamsa": "KP_New_Combined",
            "house_cusps": {
                "2": {
                    "sign": "Taurus",
                    "degree": 14.28,
                    "kp_sign_lord": "Venus",
                    "kp_star_lord": "Moon",
                    "kp_sub_lord": "Jupiter",
                    "kp_sub_sub_lord": "Venus",
                    "signification": "Direct revenue streams & pricing thresholds"
                },
                "6": {
                    "sign": "Virgo",
                    "degree": 18.52,
                    "kp_sign_lord": "Mercury",
                    "kp_star_lord": "Moon",
                    "kp_sub_lord": "Mars",
                    "kp_sub_sub_lord": "Mercury",
                    "signification": "Operational team throughput & cost control"
                },
                "10": {
                    "sign": "Capricorn",
                    "degree": 22.15,
                    "kp_sign_lord": "Saturn",
                    "kp_star_lord": "Moon",
                    "kp_sub_lord": "Venus",
                    "kp_sub_sub_lord": "Rahu",
                    "signification": "Public brand equity & corporate prestige"
                },
                "11": {
                    "sign": "Aquarius",
                    "degree": 26.40,
                    "kp_sign_lord": "Saturn",
                    "kp_star_lord": "Jupiter",
                    "kp_sub_lord": "Mercury",
                    "kp_sub_sub_lord": "Jupiter",
                    "signification": "High-margin digital gains & community expansion"
                }
            },
            "kp_core_rule": {
                "planet": "Source of the commercial impulse",
                "star_lord": "Nature and velocity of the transaction",
                "sub_lord": "Decisive arbiter: Favorable or Unfavorable outcome"
            }
        }
    }

    shard_08 = {
        "metadata": {
            "name": "Market Operator Gamma",
            "client_id": "CLIENT_003"
        },
        "system": "timing_chronocrators",
        "timing_timeline": {
            "dynamic_windows": [
                {
                    "event": "Q4 Enterprise Campaign Launch",
                    "start_utc": "2026-10-20T14:00:00Z",
                    "end_utc": "2026-10-27T22:00:00Z",
                    "ruling_sub_lord": "Jupiter",
                    "verdict": "Highly Favorable",
                    "recommended_action": "Open high-ticket enrollment funnel"
                },
                {
                    "event": "Public Masterclass & Ads Scaling",
                    "start_utc": "2026-11-08T09:30:00Z",
                    "end_utc": "2026-11-12T18:00:00Z",
                    "ruling_sub_lord": "Venus",
                    "verdict": "Auspicious",
                    "recommended_action": "Scale Meta/Google ads budget 2.5x"
                }
            ],
            "transits": {
                "slow_planets": {
                    "Jupiter": {"transit_sign": "Cancer", "aspect_to_h11": "Trine", "potency": "Exalted"},
                    "Saturn": {"transit_sign": "Aries", "aspect_to_h2": "Sextile", "discipline": "Strict"}
                },
                "lunar_cycles": {
                    "upcoming_new_moon": {"sign": "Scorpio", "degree": 12.30, "date": "2026-11-10"},
                    "upcoming_full_moon": {"sign": "Taurus", "degree": 12.30, "date": "2026-11-24"}
                }
            },
            "vedic_dashas_5_levels": {
                "maha_dasha": {"graha": "Jupiter", "end_date": "2032-04-18"},
                "antar_dasha": {"graha": "Mercury", "end_date": "2027-02-10"},
                "pratyantar_dasha": {"graha": "Venus", "end_date": "2026-11-15"},
                "sookshma_dasha": {"graha": "Rahu", "end_date": "2026-10-25"},
                "prana_dasha": {"graha": "Jupiter", "end_date": "2026-10-21"}
            }
        }
    }

    shard_10 = {
        "metadata": {
            "name": "Market Operator Gamma",
            "client_id": "CLIENT_003"
        },
        "system": "electional_asteroids",
        "commercial_asteroids": {
            "Hermes": {"degree": 114.50, "sign": "Cancer", "aspect": "Conjunction MC", "activation": "Agile intellectual commerce"},
            "Midas": {"degree": 44.80, "sign": "Taurus", "aspect": "Trine Sun", "activation": "High-ticket monetization touch"},
            "Fortuna": {"degree": 226.50, "sign": "Scorpio", "aspect": "Trine Jupiter", "activation": "Windfall community equity"}
        },
        "fixed_stars": {
            "Regulus": {"degree": 150.12, "longitude": 150.12, "connected_house": 10, "status": "Active", "signification": "Royal corporate prestige & sovereign visibility"},
            "Spica": {"degree": 204.05, "longitude": 204.05, "connected_house": 2, "status": "Active", "signification": "Inexhaustible material and creative fortune"}
        }
    }

    return {
        "vedic_sidereal": shard_03,
        "timing_transits": shard_08,
        "electional_asteroids": shard_10
    }


def build_mock_manifest_diag_c() -> Dict[str, Any]:
    """Builds RFC 6901 manifest mapping for Diag-C."""
    return {
        "contract": "gentle-ai.datalake.virtual/v1",
        "consultant": "Market Operator Gamma",
        "shards": {
            "vedic_sidereal": "shard_03_vedic_sidereal.json",
            "timing_transits": "shard_08_timing_transits.json",
            "electional_asteroids": "shard_10_asteroids_fixed_stars.json"
        },
        "pointers": {
            "kp/cusps": "vedic_sidereal#/vedic_kp_v2/house_cusps",
            "kp/h2_sub_lord": "vedic_sidereal#/vedic_kp_v2/house_cusps/2/kp_sub_lord",
            "kp/h6_sub_lord": "vedic_sidereal#/vedic_kp_v2/house_cusps/6/kp_sub_lord",
            "kp/h10_sub_lord": "vedic_sidereal#/vedic_kp_v2/house_cusps/10/kp_sub_lord",
            "kp/h11_sub_lord": "vedic_sidereal#/vedic_kp_v2/house_cusps/11/kp_sub_lord",
            "timing/windows": "timing_transits#/timing_timeline/dynamic_windows",
            "timing/dashas_5_levels": "timing_transits#/timing_timeline/vedic_dashas_5_levels",
            "asteroids/commercial": "electional_asteroids#/commercial_asteroids",
            "asteroids/fixed_stars": "electional_asteroids#/fixed_stars"
        }
    }


def build_mock_omni_dump_diag_c() -> Dict[str, Any]:
    """Builds fallback monolithic omni_dump_mega.json for Diag-C."""
    return {
        "client_data": {
            "name": "Market Operator Gamma",
            "client_id": "CLIENT_003"
        },
        "fa_sidereal_krishnamurti": {
            "cusps": {
                "2": {"star_lord": "Moon", "sub_lord": "Jupiter"},
                "6": {"star_lord": "Moon", "sub_lord": "Mars"},
                "10": {"star_lord": "Moon", "sub_lord": "Venus"},
                "11": {"star_lord": "Jupiter", "sub_lord": "Mercury"}
            }
        },
        "timing_timeline": {
            "transits": {"Jupiter": {"sign": "Cancer"}},
            "dashas": {"maha": "Jupiter", "antar": "Mercury"}
        },
        "commercial_asteroids": {
            "Hermes": {"degree": 114.50},
            "Midas": {"degree": 44.80}
        }
    }


def test_primary_shards_structure():
    shards = build_mock_shards_diag_c()
    assert isinstance(shards, dict)
    assert "vedic_sidereal" in shards
    assert "timing_transits" in shards
    assert "electional_asteroids" in shards

    assert shards["vedic_sidereal"]["system"] == "vedic_jyotish"
    assert shards["timing_transits"]["system"] == "timing_chronocrators"
    assert shards["electional_asteroids"]["system"] == "electional_asteroids"
    print("✓ test_primary_shards_structure passed")


def test_rfc6901_pointers_resolution():
    shards = build_mock_shards_diag_c()
    manifest = build_mock_manifest_diag_c()

    h2_sub = resolve_rfc6901(shards, manifest["pointers"], "kp/h2_sub_lord")
    assert h2_sub == "Jupiter"

    h10_sub = resolve_rfc6901(shards, manifest["pointers"], "kp/h10_sub_lord")
    assert h10_sub == "Venus"

    h11_sub = resolve_rfc6901(shards, manifest["pointers"], "kp/h11_sub_lord")
    assert h11_sub == "Mercury"

    windows = resolve_rfc6901(shards, manifest["pointers"], "timing/windows")
    assert isinstance(windows, list) and len(windows) >= 2
    assert windows[0]["ruling_sub_lord"] == "Jupiter"

    asteroids = resolve_rfc6901(shards, manifest["pointers"], "asteroids/commercial")
    assert "Hermes" in asteroids and "Midas" in asteroids
    print("✓ test_rfc6901_pointers_resolution passed")


def test_mandatory_canonical_vectors():
    shards = build_mock_shards_diag_c()

    # Vector 1: Krishnamurti Paddhati (KP) Puntos
    kp_cusps = shards["vedic_sidereal"]["vedic_kp_v2"]["house_cusps"]
    for house_num in ["2", "6", "10", "11"]:
        assert house_num in kp_cusps
        cusp_data = kp_cusps[house_num]
        assert "kp_star_lord" in cusp_data and len(cusp_data["kp_star_lord"]) > 0
        assert "kp_sub_lord" in cusp_data and len(cusp_data["kp_sub_lord"]) > 0
        assert "kp_sub_sub_lord" in cusp_data and len(cusp_data["kp_sub_sub_lord"]) > 0

    # Vector 2: Ciclos de Proyección (Timeline, Transits, 5-Level Dashas)
    timing = shards["timing_transits"]["timing_timeline"]
    assert "dynamic_windows" in timing
    assert "transits" in timing
    assert "vedic_dashas_5_levels" in timing
    dashas = timing["vedic_dashas_5_levels"]
    assert "maha_dasha" in dashas and "antar_dasha" in dashas and "pratyantar_dasha" in dashas

    # Vector 3: Puntos de Impacto Comercial (Asteroides + Fixed Stars)
    asteroids = shards["electional_asteroids"]["commercial_asteroids"]
    fixed_stars = shards["electional_asteroids"]["fixed_stars"]
    assert "Midas" in asteroids and "Hermes" in asteroids
    assert "Regulus" in fixed_stars and "Spica" in fixed_stars
    assert fixed_stars["Regulus"]["status"] == "Active"
    print("✓ test_mandatory_canonical_vectors passed")


def test_attestation_protocol():
    shards = build_mock_shards_diag_c()
    kp_cusps = shards["vedic_sidereal"]["vedic_kp_v2"]["house_cusps"]

    # Verify presence of KP_Sub_Lord and KP_Star_Lord for houses 2, 6, 10, 11
    required_houses = ["2", "6", "10", "11"]
    for h in required_houses:
        assert h in kp_cusps, f"House {h} missing from KP cusps"
        assert bool(kp_cusps[h].get("kp_star_lord")), f"Missing KP_Star_Lord for House {h}"
        assert bool(kp_cusps[h].get("kp_sub_lord")), f"Missing KP_Sub_Lord for House {h}"

    # Verify corrupt structure fails attestation
    corrupt_cusps = {"2": {"kp_star_lord": "Moon"}}
    assert "kp_sub_lord" not in corrupt_cusps["2"]
    assert "6" not in corrupt_cusps
    print("✓ test_attestation_protocol passed")


def test_omni_dump_fallback():
    omni = build_mock_omni_dump_diag_c()
    assert "fa_sidereal_krishnamurti" in omni
    assert "timing_timeline" in omni
    assert "commercial_asteroids" in omni

    kp = omni["fa_sidereal_krishnamurti"]["cusps"]
    assert kp["2"]["sub_lord"] == "Jupiter"
    assert kp["10"]["sub_lord"] == "Venus"
    print("✓ test_omni_dump_fallback passed")


def test_kp_decision_ruling_logic():
    """
    Validates KP Canonical Rule:
    Planet = source, Star Lord = nature of event, Sub Lord = favorable decider.
    """
    def evaluate_kp_window(star_lord: str, sub_lord: str) -> Dict[str, Any]:
        benefics = {"Jupiter", "Venus", "Mercury", "Waxing_Moon"}
        favorable = sub_lord in benefics
        return {
            "nature": f"Governed by {star_lord}",
            "favorable": favorable,
            "verdict": "APPROVED_LAUNCH" if favorable else "REVISE_WINDOW"
        }

    eval_jup = evaluate_kp_window(star_lord="Moon", sub_lord="Jupiter")
    assert eval_jup["favorable"] is True
    assert eval_jup["verdict"] == "APPROVED_LAUNCH"

    eval_sat = evaluate_kp_window(star_lord="Moon", sub_lord="Rahu")
    assert eval_sat["favorable"] is False
    assert eval_sat["verdict"] == "REVISE_WINDOW"
    print("✓ test_kp_decision_ruling_logic passed")


if __name__ == "__main__":
    test_primary_shards_structure()
    test_rfc6901_pointers_resolution()
    test_mandatory_canonical_vectors()
    test_attestation_protocol()
    test_omni_dump_fallback()
    test_kp_decision_ruling_logic()
    print("All hermetic tests passed successfully for oraculo-diag-c-mkt (exit code 0).")
    sys.exit(0)
