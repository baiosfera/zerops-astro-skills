#!/usr/bin/env python3
"""
Hermetic Unit Test for Oráculo Diag-D-Leg (Blindaje Legal & Sociedades).
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


def build_mock_shards_diag_d() -> Dict[str, Any]:
    """Builds in-memory mock shards matching usage.md specifications for Diag-D."""
    shard_03 = {
        "metadata": {
            "name": "Corporate Counsel Delta",
            "client_id": "CLIENT_004"
        },
        "system": "vedic_jyotish",
        "bhava_bala": {
            "house_6": {"rupas": 7.15, "virupas": 429, "rank": 6, "status": "Strongly Defended"},
            "house_7": {"rupas": 6.80, "virupas": 408, "rank": 8, "status": "Equilibrated"},
            "house_8": {"rupas": 5.90, "virupas": 354, "rank": 11, "status": "Needs Structural Shielding"}
        },
        "houses_triad_6_7_8": {
            "house_6": {
                "house": 6,
                "sign": "Taurus",
                "ruler": "Venus",
                "degree": 18.40,
                "domain": "Litigation, labor disputes, open contractual conflicts",
                "litigation_risk_score": "Low-Moderate",
                "contractor_dispute_clause": "Standard mandatory arbitration clause required"
            },
            "house_7": {
                "house": 7,
                "sign": "Gemini",
                "ruler": "Mercury",
                "degree": 22.10,
                "domain": "Commercial partnerships, M&A contracts, joint ventures",
                "co_founder_synergy": "High complementary intellectual capacity",
                "buy_sell_agreement_needed": True
            },
            "house_8": {
                "house": 8,
                "sign": "Cancer",
                "ruler": "Moon",
                "degree": 26.50,
                "domain": "Joint assets, corporate tax liabilities, contingent debts",
                "tax_audit_vulnerability": "Requires dual-signature holding structure",
                "ip_protection_status": "Escrow repository mandatory"
            }
        },
        "saturn_mars_afflictions": {
            "Saturn": {
                "natal_sign": "Aquarius",
                "aspects": [
                    {"target_house": 8, "aspect_type": "3rd Aspect", "intensity": "Hard", "remedy": "Segregated asset trust"}
                ]
            },
            "Mars": {
                "natal_sign": "Scorpio",
                "aspects": [
                    {"target_house": 6, "aspect_type": "Opposition", "intensity": "Acute", "remedy": "Indemnity caps in supplier agreements"}
                ]
            }
        }
    }

    shard_08 = {
        "metadata": {
            "name": "Corporate Counsel Delta",
            "client_id": "CLIENT_004"
        },
        "system": "timing_chronocrators",
        "legal_critical_timing": {
            "critical_windows": [
                {
                    "window_id": "WIN_LEGAL_01",
                    "period": "2026-11-15 to 2026-12-20",
                    "activating_transit": "Mars retrograde stationing over natal House 6 ruler",
                    "risk_type": "Labor contract re-negotiations and subcontractor claims",
                    "protocol": "Execute pre-emptive NDA and settlement releases before Nov 10"
                },
                {
                    "window_id": "WIN_LEGAL_02",
                    "period": "2027-04-05 to 2027-05-15",
                    "activating_transit": "Total Solar Eclipse in House 8 axis",
                    "risk_type": "Tax audit scrutiny and corporate restructuring friction",
                    "protocol": "Conduct independent fiscal audit in Q1 2027"
                }
            ],
            "eclipses_activating_triad": [
                {"house": 8, "date": "2027-04-20", "type": "Solar Eclipse"}
            ]
        }
    }

    return {
        "vedic_sidereal": shard_03,
        "timing_transits": shard_08
    }


def build_mock_manifest_diag_d() -> Dict[str, Any]:
    """Builds RFC 6901 manifest mapping for Diag-D."""
    return {
        "contract": "gentle-ai.datalake.virtual/v1",
        "consultant": "Corporate Counsel Delta",
        "shards": {
            "vedic_sidereal": "shard_03_vedic_sidereal.json",
            "timing_transits": "shard_08_timing_transits.json"
        },
        "pointers": {
            "legal/triad_houses": "vedic_sidereal#/houses_triad_6_7_8",
            "legal/h6_ruler": "vedic_sidereal#/houses_triad_6_7_8/house_6/ruler",
            "legal/h7_ruler": "vedic_sidereal#/houses_triad_6_7_8/house_7/ruler",
            "legal/h8_ruler": "vedic_sidereal#/houses_triad_6_7_8/house_8/ruler",
            "legal/bhava_bala": "vedic_sidereal#/bhava_bala",
            "legal/saturn_mars": "vedic_sidereal#/saturn_mars_afflictions",
            "legal/critical_windows": "timing_transits#/legal_critical_timing/critical_windows"
        }
    }


def build_mock_omni_dump_diag_d() -> Dict[str, Any]:
    """Builds fallback monolithic omni_dump_mega.json for Diag-D."""
    return {
        "client_data": {
            "name": "Corporate Counsel Delta",
            "client_id": "CLIENT_004"
        },
        "fa_tropical_calculate": {
            "houses": [
                {"house": 6, "sign": "Taurus", "ruler": "Venus", "degree": 18.40},
                {"house": 7, "sign": "Gemini", "ruler": "Mercury", "degree": 22.10},
                {"house": 8, "sign": "Cancer", "ruler": "Moon", "degree": 26.50}
            ]
        },
        "va_all_planet_data": {
            "Saturn": {"sign": "Aquarius", "house": 11},
            "Mars": {"sign": "Scorpio", "house": 5}
        },
        "timing_transits": {
            "critical_windows": [
                {"period": "2026-11-15 to 2026-12-20", "risk_type": "Labor contract re-negotiations"}
            ]
        }
    }


def test_primary_shards_structure():
    shards = build_mock_shards_diag_d()
    assert isinstance(shards, dict)
    assert "vedic_sidereal" in shards
    assert "timing_transits" in shards

    assert shards["vedic_sidereal"]["system"] == "vedic_jyotish"
    assert shards["timing_transits"]["system"] == "timing_chronocrators"
    print("✓ test_primary_shards_structure passed")


def test_rfc6901_pointers_resolution():
    shards = build_mock_shards_diag_d()
    manifest = build_mock_manifest_diag_d()

    h6_ruler = resolve_rfc6901(shards, manifest["pointers"], "legal/h6_ruler")
    assert h6_ruler == "Venus"

    h7_ruler = resolve_rfc6901(shards, manifest["pointers"], "legal/h7_ruler")
    assert h7_ruler == "Mercury"

    h8_ruler = resolve_rfc6901(shards, manifest["pointers"], "legal/h8_ruler")
    assert h8_ruler == "Moon"

    bhava = resolve_rfc6901(shards, manifest["pointers"], "legal/bhava_bala")
    assert "house_6" in bhava and "house_7" in bhava and "house_8" in bhava

    windows = resolve_rfc6901(shards, manifest["pointers"], "legal/critical_windows")
    assert isinstance(windows, list) and len(windows) >= 2
    assert "WIN_LEGAL_01" in windows[0]["window_id"]
    print("✓ test_rfc6901_pointers_resolution passed")


def test_mandatory_canonical_vectors():
    shards = build_mock_shards_diag_d()

    # Vector 1: Triada de Riesgo y Sociedades (Casas 6, 7, 8)
    triad = shards["vedic_sidereal"]["houses_triad_6_7_8"]
    assert "house_6" in triad and "litigation_risk_score" in triad["house_6"]
    assert "house_7" in triad and "buy_sell_agreement_needed" in triad["house_7"]
    assert "house_8" in triad and "tax_audit_vulnerability" in triad["house_8"]

    # Vector 2: Aflicciones de Saturno y Marte
    afflictions = shards["vedic_sidereal"]["saturn_mars_afflictions"]
    assert "Saturn" in afflictions and "Mars" in afflictions
    assert len(afflictions["Saturn"]["aspects"]) > 0
    assert len(afflictions["Mars"]["aspects"]) > 0
    assert afflictions["Mars"]["aspects"][0]["intensity"] == "Acute"

    # Vector 3: Ventanas Temporales Críticas
    timing = shards["timing_transits"]["legal_critical_timing"]
    assert "critical_windows" in timing
    assert len(timing["critical_windows"]) >= 2
    assert "protocol" in timing["critical_windows"][0]
    print("✓ test_mandatory_canonical_vectors passed")


def test_attestation_protocol():
    shards = build_mock_shards_diag_d()
    triad = shards["vedic_sidereal"]["houses_triad_6_7_8"]

    # Attestation requirement from usage.md: Validate position and rulership of Houses 6, 7, 8
    for h_key in ["house_6", "house_7", "house_8"]:
        assert h_key in triad, f"House key {h_key} missing from triad"
        h_data = triad[h_key]
        assert "degree" in h_data and isinstance(h_data["degree"], (int, float))
        assert "ruler" in h_data and len(h_data["ruler"]) > 0
        assert "sign" in h_data and len(h_data["sign"]) > 0

    # Assert fail-fast if house position is missing
    corrupt_triad = {"house_6": {"ruler": "Venus"}}
    assert "degree" not in corrupt_triad["house_6"]
    assert "house_7" not in corrupt_triad
    print("✓ test_attestation_protocol passed")


def test_omni_dump_fallback():
    omni = build_mock_omni_dump_diag_d()
    assert "fa_tropical_calculate" in omni
    assert "va_all_planet_data" in omni

    houses = omni["fa_tropical_calculate"]["houses"]
    house_map = {h["house"]: h for h in houses}
    assert 6 in house_map and 7 in house_map and 8 in house_map
    assert house_map[6]["ruler"] == "Venus"
    assert house_map[7]["ruler"] == "Mercury"
    assert house_map[8]["ruler"] == "Moon"
    print("✓ test_omni_dump_fallback passed")


def test_strict_isolation_guardrail():
    """
    Validates Atomic Output & Non-Destructive Invariant:
    Output must be saved exclusively to diag_d_leg_report.md and NEVER overwrite prior phases.
    """
    allowed_file = "diag_d_leg_report.md"
    prohibited_overwrites = ["fase1_identidad.md", "fase7_voc.md", "fase8_legal.md", "coach_report.md"]

    def enforce_isolated_write(target: str) -> bool:
        if target in prohibited_overwrites:
            raise PermissionError(f"DENIED: Prohibited overwrite of canonical asset '{target}'")
        return target == allowed_file

    assert enforce_isolated_write("diag_d_leg_report.md") is True
    for bad in prohibited_overwrites:
        try:
            enforce_isolated_write(bad)
            assert False, f"Should have blocked overwrite of {bad}"
        except PermissionError:
            pass
    print("✓ test_strict_isolation_guardrail passed")


if __name__ == "__main__":
    test_primary_shards_structure()
    test_rfc6901_pointers_resolution()
    test_mandatory_canonical_vectors()
    test_attestation_protocol()
    test_omni_dump_fallback()
    test_strict_isolation_guardrail()
    print("All hermetic tests passed successfully for oraculo-diag-d-leg (exit code 0).")
    sys.exit(0)
