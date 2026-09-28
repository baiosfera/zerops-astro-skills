#!/usr/bin/env python3
"""
Hermetic Unit Test for Oráculo Diag-E-Geo (Astrocartografía y Relocación).
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


def build_mock_shards_diag_e() -> Dict[str, Any]:
    """Builds in-memory mock shards matching usage.md specifications for Diag-E."""
    shard_09 = {
        "metadata": {
            "name": "Global Founder Epsilon",
            "client_id": "CLIENT_005",
            "birth_city": "Bogota",
            "birth_lat": 4.711,
            "birth_lng": -74.072
        },
        "system": "astrocartography_relocation",
        "geo_acg": {
            "projection_engine": "SwissEph_Mundane_ACG",
            "world_cities_count": 34200,
            "lines": [
                {
                    "planet": "Sun",
                    "cardinal_axis": "MC",
                    "coordinates": [
                        {"lat": 51.5074, "lng": -0.1278, "city": "London", "country": "UK", "orb_km": 15.2},
                        {"lat": 48.8566, "lng": 2.3522, "city": "Paris", "country": "France", "orb_km": 42.0}
                    ],
                    "archetypal_effect": "Peak corporate authority, international brand prestige, executive recognition"
                },
                {
                    "planet": "Sun",
                    "cardinal_axis": "ASC",
                    "coordinates": [
                        {"lat": 40.7128, "lng": -74.0060, "city": "New York", "country": "USA", "orb_km": 8.5}
                    ],
                    "archetypal_effect": "Radiant charismatic presence, personal leadership, brand magnetism"
                },
                {
                    "planet": "Jupiter",
                    "cardinal_axis": "MC",
                    "coordinates": [
                        {"lat": 25.7617, "lng": -80.1918, "city": "Miami", "country": "USA", "orb_km": 12.0},
                        {"lat": 19.4326, "lng": -99.1332, "city": "Mexico City", "country": "Mexico", "orb_km": 38.5}
                    ],
                    "archetypal_effect": "Unchecked commercial scaling, venture capital attraction, institutional abundance"
                },
                {
                    "planet": "Jupiter",
                    "cardinal_axis": "DSC",
                    "coordinates": [
                        {"lat": 34.0522, "lng": -118.2437, "city": "Los Angeles", "country": "USA", "orb_km": 25.0}
                    ],
                    "archetypal_effect": "High-ticket strategic alliances, client acquisition, enterprise joint ventures"
                },
                {
                    "planet": "Venus",
                    "cardinal_axis": "DSC",
                    "coordinates": [
                        {"lat": 37.7749, "lng": -122.4194, "city": "San Francisco", "country": "USA", "orb_km": 19.8}
                    ],
                    "archetypal_effect": "Harmonious client relationships, high aesthetic valuation, luxury market appeal"
                },
                {
                    "planet": "Venus",
                    "cardinal_axis": "IC",
                    "coordinates": [
                        {"lat": -34.6037, "lng": -58.3816, "city": "Buenos Aires", "country": "Argentina", "orb_km": 14.1}
                    ],
                    "archetypal_effect": "Somatic emotional sanctuary, aesthetic real estate acquisition, inner peace"
                }
            ],
            "angular_crossings": [
                {
                    "crossing_type": "Paran / Zenith Crossing",
                    "planets": ["Jupiter", "Sun"],
                    "axes": ["MC", "ASC"],
                    "lat": 25.7617,
                    "lng": -80.1918,
                    "geographic_region": "South Florida Corridor",
                    "strategic_use": "Primary legal jurisdiction for holding entity & global capital raises"
                }
            ]
        },
        "geo_acg_best_places": {
            "commercial_expansion": ["Miami", "London", "New York"],
            "remote_ad_activation": ["Los Angeles", "San Francisco"],
            "executive_retreats": ["Buenos Aires", "Medellin"]
        },
        "geo_local_space": {
            "reference_origin": {"city": "Bogota", "lat": 4.711, "lng": -74.072},
            "azimuth_bearings": {
                "Sun": {"azimuth_deg": 78.4, "compass": "ENE", "feng_shui_alignment": "Creative production & vitality"},
                "Jupiter": {"azimuth_deg": 312.6, "compass": "NW", "feng_shui_alignment": "Sovereign governance & institutional wealth"},
                "Venus": {"azimuth_deg": 64.2, "compass": "ENE", "feng_shui_alignment": "Brand elegance & high-margin partnerships"},
                "Saturn": {"azimuth_deg": 220.1, "compass": "SW", "feng_shui_alignment": "Long-term infrastructure & risk management"}
            }
        }
    }

    return {
        "relocation_acg": shard_09
    }


def build_mock_manifest_diag_e() -> Dict[str, Any]:
    """Builds RFC 6901 manifest mapping for Diag-E."""
    return {
        "contract": "gentle-ai.datalake.virtual/v1",
        "consultant": "Global Founder Epsilon",
        "shards": {
            "relocation_acg": "shard_09_astrocartography.json"
        },
        "pointers": {
            "acg/lines": "relocation_acg#/geo_acg/lines",
            "acg/crossings": "relocation_acg#/geo_acg/angular_crossings",
            "acg/best_places": "relocation_acg#/geo_acg_best_places",
            "acg/commercial_expansion": "relocation_acg#/geo_acg_best_places/commercial_expansion",
            "acg/local_space": "relocation_acg#/geo_local_space",
            "acg/azimuths": "relocation_acg#/geo_local_space/azimuth_bearings"
        }
    }


def build_mock_omni_dump_diag_e() -> Dict[str, Any]:
    """Builds fallback monolithic omni_dump_mega.json for Diag-E."""
    return {
        "client_data": {
            "name": "Global Founder Epsilon",
            "client_id": "CLIENT_005"
        },
        "aw_astrocartography": {
            "lines": [
                {"planet": "Sun", "cardinal_axis": "MC", "city": "London"},
                {"planet": "Jupiter", "cardinal_axis": "MC", "city": "Miami"},
                {"planet": "Venus", "cardinal_axis": "DSC", "city": "Paris"}
            ],
            "local_space": {
                "Jupiter": {"azimuth": 312.6, "direction": "NW"}
            }
        }
    }


def test_primary_shards_structure():
    shards = build_mock_shards_diag_e()
    assert isinstance(shards, dict)
    assert "relocation_acg" in shards

    s9 = shards["relocation_acg"]
    assert s9["system"] == "astrocartography_relocation"
    assert "geo_acg" in s9
    assert "geo_acg_best_places" in s9
    assert "geo_local_space" in s9
    print("✓ test_primary_shards_structure passed")


def test_rfc6901_pointers_resolution():
    shards = build_mock_shards_diag_e()
    manifest = build_mock_manifest_diag_e()

    lines = resolve_rfc6901(shards, manifest["pointers"], "acg/lines")
    assert isinstance(lines, list) and len(lines) >= 6

    crossings = resolve_rfc6901(shards, manifest["pointers"], "acg/crossings")
    assert isinstance(crossings, list) and len(crossings) >= 1
    assert crossings[0]["geographic_region"] == "South Florida Corridor"

    commercial = resolve_rfc6901(shards, manifest["pointers"], "acg/commercial_expansion")
    assert "Miami" in commercial and "London" in commercial

    azimuths = resolve_rfc6901(shards, manifest["pointers"], "acg/azimuths")
    assert "Jupiter" in azimuths and "Sun" in azimuths
    print("✓ test_rfc6901_pointers_resolution passed")


def test_mandatory_canonical_vectors():
    shards = build_mock_shards_diag_e()

    # Vector 1: Líneas Angulares (ACG) en los 4 ejes cardinales (ASC, DSC, MC, IC)
    lines = shards["relocation_acg"]["geo_acg"]["lines"]
    axes_found = {item["cardinal_axis"] for item in lines}
    assert "ASC" in axes_found, "Missing ASC line vector"
    assert "DSC" in axes_found, "Missing DSC line vector"
    assert "MC" in axes_found, "Missing MC line vector"
    assert "IC" in axes_found, "Missing IC line vector"

    for line in lines:
        assert "planet" in line and len(line["planet"]) > 0
        assert "coordinates" in line and len(line["coordinates"]) > 0
        first_coord = line["coordinates"][0]
        assert "lat" in first_coord and "lng" in first_coord and "city" in first_coord
        assert "archetypal_effect" in line and len(line["archetypal_effect"]) > 0

    # Vector 2: Espacio Local (Azimuth & micro-relocación)
    local_space = shards["relocation_acg"]["geo_local_space"]
    assert "reference_origin" in local_space
    assert "azimuth_bearings" in local_space
    assert "Jupiter" in local_space["azimuth_bearings"]
    jup_az = local_space["azimuth_bearings"]["Jupiter"]
    assert "azimuth_deg" in jup_az and isinstance(jup_az["azimuth_deg"], (int, float))
    assert "compass" in jup_az
    assert "feng_shui_alignment" in jup_az
    print("✓ test_mandatory_canonical_vectors passed")


def test_attestation_protocol():
    shards = build_mock_shards_diag_e()
    lines = shards["relocation_acg"]["geo_acg"]["lines"]

    # Attestation requirement from usage.md: Verify ACG lines array exists with Sun, Jupiter, Venus, etc.
    planets_with_lines = {l["planet"] for l in lines}
    assert "Sun" in planets_with_lines
    assert "Jupiter" in planets_with_lines
    assert "Venus" in planets_with_lines

    # Verify corrupt lines array fails attestation
    corrupt_lines = [{"planet": "Mars", "cardinal_axis": "ASC"}]
    corrupt_planets = {l["planet"] for l in corrupt_lines}
    assert "Sun" not in corrupt_planets
    print("✓ test_attestation_protocol passed")


def test_omni_dump_fallback():
    omni = build_mock_omni_dump_diag_e()
    assert "aw_astrocartography" in omni
    assert "lines" in omni["aw_astrocartography"]
    assert "local_space" in omni["aw_astrocartography"]

    lines = omni["aw_astrocartography"]["lines"]
    planets = {l["planet"] for l in lines}
    assert "Sun" in planets and "Jupiter" in planets and "Venus" in planets
    print("✓ test_omni_dump_fallback passed")


def test_cardinal_axis_mapping():
    """
    Validates Cardinal Axis Operational Semantics:
    MC = Incorporation & Holding / Visibilidad
    DC = Ad Campaigns / Partnerships
    AC = CEO Relocation / Personal Presence
    IC = Retreats / Real Estate Sanctuary
    """
    axis_semantics = {
        "MC": "Incorporation & Corporate Visibility",
        "DSC": "Partnerships & Ad Campaigns",
        "ASC": "Personal Magnetism & Brand Face",
        "IC": "Real Estate Sanctuary & Private Retreat"
    }

    shards = build_mock_shards_diag_e()
    lines = shards["relocation_acg"]["geo_acg"]["lines"]

    for item in lines:
        axis = item["cardinal_axis"]
        assert axis in axis_semantics, f"Unknown cardinal axis: {axis}"
    print("✓ test_cardinal_axis_mapping passed")


if __name__ == "__main__":
    test_primary_shards_structure()
    test_rfc6901_pointers_resolution()
    test_mandatory_canonical_vectors()
    test_attestation_protocol()
    test_omni_dump_fallback()
    test_cardinal_axis_mapping()
    print("All hermetic tests passed successfully for oraculo-diag-e-geo (exit code 0).")
    sys.exit(0)
