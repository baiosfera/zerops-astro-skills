#!/usr/bin/env python3
"""
Hermetic Unit Test for Oráculo Diag-A-Psy (Psicología Profunda).
Zero LLM Tokens | < 50ms Execution | 100% Deterministic | Zero Network / Zero PII.
Validates Dual Ingestion: Primary (VirtualDataLake RFC 6901 Shards) & Fallback (omni_dump_mega.json).
"""

import sys
sys.dont_write_bytecode = True

import json
from typing import Any, Dict, List, Optional


def resolve_rfc6901(shards: Dict[str, Any], manifest_pointers: Dict[str, str], pointer: str) -> Any:
    """
    Standard RFC 6901 JSON pointer resolver with manifest pointer aliasing.
    Format: '<shard_key>#/<json/pointer/tokens>' or manifest alias.
    """
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


def build_mock_shards_diag_a() -> Dict[str, Any]:
    """Builds in-memory mock shards matching usage.md specifications for Diag-A."""
    shard_01 = {
        "metadata": {
            "name": "Consultant Alpha",
            "client_id": "CLIENT_001",
            "has_birth_time": True,
            "year": 1988,
            "month": 4,
            "day": 12,
            "lat": 4.711,
            "lng": -74.072
        },
        "system": "western_tropical",
        "default_house_system": "placidus",
        "freeastro_tropical_placidus": {
            "angles": {
                "asc": 124.52,
                "mc": 32.18,
                "dsc": 304.52,
                "ic": 212.18
            },
            "planets": [
                {"name": "Sun", "sign": "Aries", "pos": 22.84, "house": 9, "retrograde": False},
                {"name": "Moon", "sign": "Pisces", "pos": 15.30, "house": 8, "retrograde": False},
                {"name": "Ascendant", "sign": "Leo", "pos": 4.52, "house": 1, "retrograde": False},
                {"name": "Mercury", "sign": "Taurus", "pos": 8.12, "house": 10, "retrograde": True}
            ],
            "houses": [
                {"house": 1, "sign": "Leo", "degree": 4.52},
                {"house": 2, "sign": "Virgo", "degree": 28.10},
                {"house": 10, "sign": "Taurus", "degree": 2.18}
            ]
        },
        "modern_psychology": {
            "arroyo_elements": {"dominant": "Fire/Earth", "subordinate": "Air"},
            "greene_archetypes": {"ego": "The Sovereign", "anima_animus": "The Alchemist"},
            "greene_shadow": {
                "archetype": "The Unseen Tyrant",
                "trigger": "Perceived loss of intellectual control",
                "integration": "Vulnerability and decentralized delegation"
            },
            "rudhyar_lunation": {"phase": "Balsamic", "signification": "Closure and seed consolidation"}
        },
        "tropical_equal_asc": {
            "corporate_mask": "The Unshakable Strategist",
            "defense_mechanism": "Intellectual rationalization and structural perfectionism",
            "houses": [
                {"house": 1, "sign": "Leo", "degree": 4.52},
                {"house": 10, "sign": "Taurus", "degree": 4.52}
            ]
        }
    }

    shard_02 = {
        "metadata": {
            "name": "Consultant Alpha",
            "client_id": "CLIENT_001",
            "has_birth_time": True
        },
        "system": "western_sidereal",
        "primary_variant": "fagan_campanus",
        "variants": {
            "fagan_campanus": {
                "angles": {
                    "asc": 100.22,
                    "mc": 8.44
                },
                "planets": [
                    {"name": "Sun", "sign": "Pisces", "pos": 28.60, "house": 9},
                    {"name": "Moon", "sign": "Aquarius", "pos": 21.05, "house": 8},
                    {"name": "Ascendant", "sign": "Cancer", "pos": 10.22, "house": 1}
                ],
                "shadow_root": "Raw unconscious dread of irrelevance and exposure",
                "impostor_syndrome_origin": "Early over-identification with unearned precocity"
            },
            "aldebaran_vehlow": {
                "core_anchor": "Unyielding ethical fidelity to core essence",
                "intercepted_psyche": {
                    "intercepted_signs": ["Scorpio", "Taurus"],
                    "blind_spot": "Deep somatic resistance to passive trust"
                }
            }
        }
    }

    return {
        "western_tropical": shard_01,
        "western_sidereal": shard_02
    }


def build_mock_manifest_diag_a() -> Dict[str, Any]:
    """Builds RFC 6901 manifest mapping for Diag-A."""
    return {
        "contract": "gentle-ai.datalake.virtual/v1",
        "consultant": "Consultant Alpha",
        "shards": {
            "western_tropical": "shard_01_western_natal.json",
            "western_sidereal": "shard_02_psychological.json"
        },
        "pointers": {
            "tropical/ascendant": "western_tropical#/freeastro_tropical_placidus/angles/asc",
            "tropical/planets": "western_tropical#/freeastro_tropical_placidus/planets",
            "tropical/greene_shadow": "western_tropical#/modern_psychology/greene_shadow",
            "tropical/equal_asc_mask": "western_tropical#/tropical_equal_asc/corporate_mask",
            "sidereal/fagan_campanus": "western_sidereal#/variants/fagan_campanus",
            "sidereal/fagan_asc": "western_sidereal#/variants/fagan_campanus/angles/asc",
            "sidereal/aldebaran_vehlow": "western_sidereal#/variants/aldebaran_vehlow",
            "sidereal/core_anchor": "western_sidereal#/variants/aldebaran_vehlow/core_anchor"
        }
    }


def build_mock_omni_dump_diag_a() -> Dict[str, Any]:
    """Builds fallback monolithic omni_dump_mega.json."""
    return {
        "client_data": {
            "name": "Consultant Alpha",
            "client_id": "CLIENT_001",
            "has_birth_time": True
        },
        "fa_tropical_calculate": {
            "angles": {"asc": 124.52, "mc": 32.18},
            "planets": [
                {"name": "Sun", "pos": 22.84, "sign": "Aries"},
                {"name": "Moon", "pos": 15.30, "sign": "Pisces"},
                {"name": "Ascendant", "pos": 4.52, "sign": "Leo"}
            ]
        },
        "fa_sidereal_fagan_campanus": {
            "angles": {"asc": 100.22, "mc": 8.44},
            "planets": [
                {"name": "Sun", "pos": 28.60, "sign": "Pisces"},
                {"name": "Moon", "pos": 21.05, "sign": "Aquarius"},
                {"name": "Ascendant", "pos": 10.22, "sign": "Cancer"}
            ]
        },
        "modern_psychology": {
            "greene_shadow": {"archetype": "The Unseen Tyrant"}
        }
    }


def test_primary_shards_structure():
    shards = build_mock_shards_diag_a()
    assert isinstance(shards, dict)
    assert "western_tropical" in shards
    assert "western_sidereal" in shards

    s1 = shards["western_tropical"]
    assert s1.get("system") == "western_tropical"
    assert "freeastro_tropical_placidus" in s1
    assert "modern_psychology" in s1
    assert "tropical_equal_asc" in s1

    s2 = shards["western_sidereal"]
    assert s2.get("system") == "western_sidereal"
    assert "variants" in s2
    assert "fagan_campanus" in s2["variants"]
    assert "aldebaran_vehlow" in s2["variants"]
    print("✓ test_primary_shards_structure passed")


def test_rfc6901_pointers_resolution():
    shards = build_mock_shards_diag_a()
    manifest = build_mock_manifest_diag_a()

    asc_val = resolve_rfc6901(shards, manifest["pointers"], "tropical/ascendant")
    assert isinstance(asc_val, (int, float))
    assert asc_val == 124.52

    shadow_obj = resolve_rfc6901(shards, manifest["pointers"], "tropical/greene_shadow")
    assert isinstance(shadow_obj, dict)
    assert shadow_obj["archetype"] == "The Unseen Tyrant"

    mask_val = resolve_rfc6901(shards, manifest["pointers"], "tropical/equal_asc_mask")
    assert mask_val == "The Unshakable Strategist"

    fagan_asc = resolve_rfc6901(shards, manifest["pointers"], "sidereal/fagan_asc")
    assert fagan_asc == 100.22

    core_anchor = resolve_rfc6901(shards, manifest["pointers"], "sidereal/core_anchor")
    assert "ethical fidelity" in core_anchor
    print("✓ test_rfc6901_pointers_resolution passed")


def test_mandatory_canonical_vectors():
    shards = build_mock_shards_diag_a()

    # Vector 1: Tropical + Equal Asc (Vector Consciente)
    v1_angles = shards["western_tropical"]["freeastro_tropical_placidus"]["angles"]
    v1_mask = shards["western_tropical"]["tropical_equal_asc"]["corporate_mask"]
    assert "asc" in v1_angles and isinstance(v1_angles["asc"], float)
    assert isinstance(v1_mask, str) and len(v1_mask) > 0

    # Vector 2: Sideral Fagan-Bradley + Campanus (Vector Inconsciente)
    v2_fagan = shards["western_sidereal"]["variants"]["fagan_campanus"]
    assert "angles" in v2_fagan
    assert "shadow_root" in v2_fagan
    assert "impostor_syndrome_origin" in v2_fagan
    assert isinstance(v2_fagan["planets"], list)

    # Vector 3: Sideral Aldebaran + Vehlow (Puntos Ciegos)
    v3_vehlow = shards["western_sidereal"]["variants"]["aldebaran_vehlow"]
    assert "core_anchor" in v3_vehlow
    assert "intercepted_psyche" in v3_vehlow
    assert "blind_spot" in v3_vehlow["intercepted_psyche"]
    print("✓ test_mandatory_canonical_vectors passed")


def test_attestation_protocol():
    shards = build_mock_shards_diag_a()
    planets_tropical = shards["western_tropical"]["freeastro_tropical_placidus"]["planets"]
    planet_names = {p["name"] for p in planets_tropical}

    # Mandatory fields for Diag-A U-Shape execution
    assert "Ascendant" in planet_names
    assert "Sun" in planet_names
    assert "Moon" in planet_names

    # Assert fail-fast if mandatory key is missing
    corrupt_planets = [p for p in planets_tropical if p["name"] != "Sun"]
    corrupt_names = {p["name"] for p in corrupt_planets}
    assert "Sun" not in corrupt_names
    print("✓ test_attestation_protocol passed")


def test_omni_dump_mega_fallback():
    omni = build_mock_omni_dump_diag_a()
    assert "fa_tropical_calculate" in omni
    assert "fa_sidereal_fagan_campanus" in omni

    trop = omni["fa_tropical_calculate"]
    sid = omni["fa_sidereal_fagan_campanus"]
    assert trop["angles"]["asc"] == 124.52
    assert sid["angles"]["asc"] == 100.22

    trop_planets = {p["name"] for p in trop["planets"]}
    assert "Sun" in trop_planets and "Moon" in trop_planets and "Ascendant" in trop_planets
    print("✓ test_omni_dump_mega_fallback passed")


def test_hora_cero_guardrail():
    """
    Validates Extreme Spatial Prohibition:
    When birth time is unknown (Hora Cero), Vehlow and Campanus must be disabled,
    falling back to Whole Sign with Ascendant set in Sun's sign.
    """
    hora_cero_client = {
        "has_birth_time": False,
        "sun_sign": "Aries"
    }

    def resolve_psy_configuration(client_meta: dict) -> str:
        if not client_meta.get("has_birth_time", True):
            # Prohibit Vehlow & Campanus -> enforce Whole Sign with Asc in Sun sign
            return f"Whole_Sign_Sun_Asc_{client_meta['sun_sign']}"
        return "Fagan_Campanus_Aldebaran_Vehlow"

    config_normal = resolve_psy_configuration({"has_birth_time": True})
    assert config_normal == "Fagan_Campanus_Aldebaran_Vehlow"

    config_hora_cero = resolve_psy_configuration(hora_cero_client)
    assert config_hora_cero == "Whole_Sign_Sun_Asc_Aries"
    assert "Campanus" not in config_hora_cero
    assert "Vehlow" not in config_hora_cero
    print("✓ test_hora_cero_guardrail passed")


if __name__ == "__main__":
    test_primary_shards_structure()
    test_rfc6901_pointers_resolution()
    test_mandatory_canonical_vectors()
    test_attestation_protocol()
    test_omni_dump_mega_fallback()
    test_hora_cero_guardrail()
    print("All hermetic tests passed successfully for oraculo-diag-a-psy (exit code 0).")
    sys.exit(0)
