#!/usr/bin/env python3
"""
western_domain.py — Western Tropical & Psychological Astrology Engine for Oráculo.
Placidus / Campanus | Swiss Ephemeris | Stephen Arroyo Elements | Liz Greene Archetypes.

Synthesizes planetary coordinates, house cusps, aspectarian, elemental balance, and water houses.
Strict Bilingual Technical Gloss: English/Latin terms alongside Spanish technical explanations.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("oraculo.western_domain")

ELEMENT_SIGNS = {
    "Fire": ["Aries", "Leo", "Sagittarius"],
    "Earth": ["Taurus", "Virgo", "Capricorn"],
    "Air": ["Gemini", "Libra", "Aquarius"],
    "Water": ["Cancer", "Scorpio", "Pisces"],
}

ELEMENT_TRANSLATION = {
    "Fire": "Fuego (Iniciativa, Pasión, Visión)",
    "Earth": "Tierra (Estructura, Pragmatismo, Materialización)",
    "Air": "Aire (Comunicación, Intelecto, Relaciones)",
    "Water": "Agua (Intuición, Resonancia Emocional, Psique Profunda)",
}

SIGN_RULERS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Pluto / Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Uranus / Saturn", "Pisces": "Neptune / Jupiter"
}

SIGN_MAP = {
    "ari": "Aries", "aries": "Aries",
    "tau": "Taurus", "taurus": "Taurus",
    "gem": "Gemini", "gemini": "Gemini",
    "can": "Cancer", "cancer": "Cancer", "cnc": "Cancer",
    "leo": "Leo",
    "vir": "Virgo", "virgo": "Virgo",
    "lib": "Libra", "libra": "Libra",
    "sco": "Scorpio", "scorpio": "Scorpio",
    "sag": "Sagittarius", "sagittarius": "Sagittarius", "sgr": "Sagittarius",
    "cap": "Capricorn", "capricorn": "Capricorn",
    "aqu": "Aquarius", "aquarius": "Aquarius", "aqr": "Aquarius",
    "pis": "Pisces", "pisces": "Pisces", "psc": "Pisces",
}


def normalize_sign(raw_sign: Any) -> str:
    """Normalizes any sign abbreviation or casing to canonical English sign name."""
    if not raw_sign or not isinstance(raw_sign, (str, int, float)):
        return "Unknown"
    cleaned = str(raw_sign).strip().lower()
    return SIGN_MAP.get(cleaned, str(raw_sign).strip().title())


class WesternDomain:
    """Processes Western Tropical natal data from AstroWay, FreeAstro, and AstrologyAPI."""

    def __init__(self, crawler_entries: List[Dict[str, Any]], client_payload: Dict[str, Any]):
        self.entries = crawler_entries
        self.client = client_payload
        self.raw_data_map: Dict[str, Any] = {}
        for entry in self.entries:
            key = f"{entry['provider']}::{entry['file_name']}"
            self.raw_data_map[key] = entry["content"]

    def synthesize(self) -> Dict[str, Any]:
        """Synthesizes Western Tropical metrics into an encyclopedic data model."""
        planets: Dict[str, Dict[str, Any]] = {}
        houses: Dict[int, Dict[str, Any]] = {}
        aspects: List[Dict[str, Any]] = []

        # Zodiac sign reference for longitude conversion
        zodiac_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

        def _lon_to_sign_deg(lon_val: float) -> tuple[str, float]:
            l = float(lon_val) % 360.0
            idx = int(l // 30) % 12
            return zodiac_names[idx], round(l % 30.0, 2)

        # Sort keys to prioritize tropical/western over sidereal/vedic
        def _key_priority(k: str) -> int:
            k_low = k.lower()
            if "sidereal" in k_low or "fagan" in k_low or "lahiri" in k_low:
                return 2
            if "tropical" in k_low or "placidus" in k_low or "western" in k_low:
                return 0
            return 1

        sorted_keys = sorted(self.raw_data_map.keys(), key=_key_priority)

        # Extract planets, houses, angles, and aspects from available cache files
        for key in sorted_keys:
            content = self.raw_data_map[key]
            if not isinstance(content, dict):
                continue

            # Angles extraction (e.g. FreeAstro: angles.asc, angles.mc, angles.ic, angles.dc)
            angles_data = content.get("angles") or content.get("chart_data", {}).get("angles")
            if isinstance(angles_data, dict):
                if 1 not in houses and "asc" in angles_data and isinstance(angles_data["asc"], (int, float)):
                    asc_f = float(angles_data["asc"])
                    s_name, s_deg = _lon_to_sign_deg(asc_f)
                    houses[1] = {"house": 1, "sign": s_name, "degree": s_deg, "longitude": asc_f}
                if 10 not in houses and "mc" in angles_data and isinstance(angles_data["mc"], (int, float)):
                    mc_f = float(angles_data["mc"])
                    s_name, s_deg = _lon_to_sign_deg(mc_f)
                    houses[10] = {"house": 10, "sign": s_name, "degree": s_deg, "longitude": mc_f}
                if 4 not in houses and "ic" in angles_data and isinstance(angles_data["ic"], (int, float)):
                    ic_f = float(angles_data["ic"])
                    s_name, s_deg = _lon_to_sign_deg(ic_f)
                    houses[4] = {"house": 4, "sign": s_name, "degree": s_deg, "longitude": ic_f}
                if 7 not in houses and "dc" in angles_data and isinstance(angles_data["dc"], (int, float)):
                    dc_f = float(angles_data["dc"])
                    s_name, s_deg = _lon_to_sign_deg(dc_f)
                    houses[7] = {"house": 7, "sign": s_name, "degree": s_deg, "longitude": dc_f}

            # Check for houses in content first so planet house placement can be computed
            h_data = content.get("houses") or content.get("house_cusps") or content.get("chart_data", {}).get("houses")
            if isinstance(h_data, dict):
                # AstroWay pattern: {"system": "P", "cusps": [120.5, ...], "ascendant": 120.5}
                if "cusps" in h_data and isinstance(h_data["cusps"], list):
                    raw_cusps = h_data["cusps"]
                    if len(raw_cusps) == 13:
                        raw_cusps = raw_cusps[1:]
                    for idx, c_val in enumerate(raw_cusps[:12], 1):
                        if idx not in houses and isinstance(c_val, (int, float)):
                            s_name, s_deg = _lon_to_sign_deg(c_val)
                            houses[idx] = {
                                "house": idx,
                                "sign": s_name,
                                "degree": s_deg,
                                "longitude": float(c_val)
                            }
                # Standard keyed dict pattern: {"1": {...}, "2": {...}}
                for h_num, h_val in h_data.items():
                    try:
                        num = int(h_num)
                        if num not in houses and isinstance(h_val, dict):
                            lon_val = h_val.get("abs_pos") or h_val.get("longitude")
                            if lon_val is not None:
                                s_name, s_deg = _lon_to_sign_deg(lon_val)
                                lon_f = float(lon_val)
                            elif "cusp" in h_val and isinstance(h_val["cusp"], (int, float)) and h_val["cusp"] > 30.0:
                                s_name, s_deg = _lon_to_sign_deg(h_val["cusp"])
                                lon_f = float(h_val["cusp"])
                            else:
                                s_name = normalize_sign(h_val.get("sign_id") or h_val.get("sign") or h_val.get("sign_name"))
                                s_deg = float(h_val.get("pos") or h_val.get("degree") or h_val.get("cusp") or 0.0)
                                lon_f = 0.0
                            houses[num] = {
                                "house": num,
                                "sign": s_name,
                                "degree": s_deg,
                                "longitude": lon_f
                            }
                    except (ValueError, TypeError):
                        pass
            elif isinstance(h_data, list) and h_data:
                # AstroWay or Swiss Ephemeris list of floats: [c1, c2, ...]
                if isinstance(h_data[0], (int, float)):
                    raw_cusps = h_data
                    if len(raw_cusps) == 13:
                        raw_cusps = raw_cusps[1:]
                    for idx, c_val in enumerate(raw_cusps[:12], 1):
                        if idx not in houses and isinstance(c_val, (int, float)):
                            s_name, s_deg = _lon_to_sign_deg(c_val)
                            houses[idx] = {
                                "house": idx,
                                "sign": s_name,
                                "degree": s_deg,
                                "longitude": float(c_val)
                            }
                # Standard list of dicts: [{"house": 1, ...}]
                else:
                    for idx, h_item in enumerate(h_data, 1):
                        if isinstance(h_item, dict):
                            h_idx = int(h_item.get("house") or h_item.get("name") or idx)
                            if h_idx not in houses:
                                lon_val = h_item.get("abs_pos") or h_item.get("longitude")
                                if lon_val is not None:
                                    s_name, s_deg = _lon_to_sign_deg(lon_val)
                                    lon_f = float(lon_val)
                                else:
                                    s_name = normalize_sign(h_item.get("sign_id") or h_item.get("sign") or h_item.get("sign_name"))
                                    s_deg = float(h_item.get("pos") or h_item.get("degree") or h_item.get("cusp") or 0.0)
                                    lon_f = 0.0
                                houses[h_idx] = {
                                    "house": h_idx,
                                    "sign": s_name,
                                    "degree": s_deg,
                                    "longitude": lon_f
                                }

            # Check for planets in content
            p_data = content.get("planets") or content.get("bodies") or content.get("chart_data", {}).get("planets")
            if isinstance(p_data, dict):
                for p_raw_name, p_val in p_data.items():
                    if isinstance(p_val, dict):
                        p_name = str(p_val.get("name") or p_val.get("id") or p_raw_name).replace("_", " ").title()
                        if p_name not in planets:
                            lon_val = p_val.get("abs_pos") or p_val.get("longitude")
                            if lon_val is not None and float(lon_val) > 0.0:
                                s_name, s_deg = _lon_to_sign_deg(lon_val)
                                lon_f = float(lon_val)
                            else:
                                s_name = normalize_sign(p_val.get("sign_id") or p_val.get("sign") or p_val.get("sign_name"))
                                s_deg = float(p_val.get("pos") or p_val.get("degree") or p_val.get("norm_degree") or 0.0)
                                lon_f = 0.0
                            planets[p_name] = {
                                "name": p_name,
                                "sign": s_name,
                                "degree": s_deg,
                                "longitude": lon_f,
                                "house": int(p_val.get("house") or 1),
                                "retrograde": bool(p_val.get("is_retro") or p_val.get("isRetrograde") or p_val.get("retrograde", False)),
                                "speed": float(p_val.get("speed") or p_val.get("speedLong") or 1.0),
                            }
            elif isinstance(p_data, list):
                for p_item in p_data:
                    if isinstance(p_item, dict):
                        raw_id = p_item.get("name") or p_item.get("id") or p_item.get("planet")
                        if not raw_id:
                            continue
                        p_name = str(raw_id).replace("_", " ").title()
                        if p_name not in planets:
                            lon_val = p_item.get("abs_pos") or p_item.get("longitude")
                            if lon_val is not None and float(lon_val) > 0.0:
                                s_name, s_deg = _lon_to_sign_deg(lon_val)
                                lon_f = float(lon_val)
                            else:
                                s_name = normalize_sign(p_item.get("sign_id") or p_item.get("sign") or p_item.get("sign_name"))
                                s_deg = float(p_item.get("pos") or p_item.get("degree") or p_item.get("norm_degree") or 0.0)
                                lon_f = 0.0
                            planets[p_name] = {
                                "name": p_name,
                                "sign": s_name,
                                "degree": s_deg,
                                "longitude": lon_f,
                                "house": int(p_item.get("house") or 1),
                                "retrograde": bool(p_item.get("is_retro") or p_item.get("isRetrograde") or p_item.get("retrograde", False)),
                                "speed": float(p_item.get("speed") or p_item.get("speedLong") or 1.0),
                            }

            # Check for aspects
            asp_data = content.get("aspects") or content.get("chart_data", {}).get("aspects")
            if isinstance(asp_data, list) and not aspects:
                for a in asp_data:
                    if isinstance(a, dict):
                        b1 = a.get("body1") or a.get("planet1") or a.get("p1")
                        b2 = a.get("body2") or a.get("planet2") or a.get("p2")
                        asp_type = a.get("aspect") or a.get("type")
                        if isinstance(asp_type, dict):
                            asp_type = asp_type.get("name") or str(asp_type)
                        orb_val = float(a.get("orb") or a.get("exactAngle") or 0.0)
                        if b1 and b2 and asp_type:
                            aspects.append({
                                "body1": str(b1).replace("_", " ").title(),
                                "body2": str(b2).replace("_", " ").title(),
                                "aspect": str(asp_type).replace("_", " ").title(),
                                "orb": orb_val,
                            })

        # Re-compute planet house placements if houses cusps are available with valid longitudes
        if len(houses) == 12 and any(h.get("longitude", 0.0) > 0 for h in houses.values()):
            cusp_lons = {h_idx: houses[h_idx].get("longitude", 0.0) for h_idx in range(1, 13)}
            for p_name, p_info in planets.items():
                p_lon = p_info.get("longitude", 0.0)
                if p_lon > 0.0:
                    for h_idx in range(1, 13):
                        c_start = cusp_lons[h_idx]
                        c_end = cusp_lons[(h_idx % 12) + 1]
                        if c_start < c_end:
                            if c_start <= p_lon < c_end:
                                p_info["house"] = h_idx
                                break
                        else:  # wrap around 360
                            if p_lon >= c_start or p_lon < c_end:
                                p_info["house"] = h_idx
                                break

        # Calculate Arroyo's 4 Elements balance
        element_counts = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
        for p in planets.values():
            s = normalize_sign(p.get("sign", ""))
            for elem, signs in ELEMENT_SIGNS.items():
                if s in signs:
                    element_counts[elem] += 1

        total_pts = sum(element_counts.values()) or 1
        element_percentages = {k: round((v / total_pts) * 100, 1) for k, v in element_counts.items()}
        dominant_element = max(element_counts, key=element_counts.get) if any(v > 0 for v in element_counts.values()) else "Unknown"

        # Water Houses (Casas de Agua 4, 8, 12 - Stephen Arroyo)
        water_houses = {
            4: {"sign": normalize_sign(houses.get(4, {}).get("sign", "Unknown")), "degree": houses.get(4, {}).get("degree", 0.0)},
            8: {"sign": normalize_sign(houses.get(8, {}).get("sign", "Unknown")), "degree": houses.get(8, {}).get("degree", 0.0)},
            12: {"sign": normalize_sign(houses.get(12, {}).get("sign", "Unknown")), "degree": houses.get(12, {}).get("degree", 0.0)},
        }

        # Trípode de Hierro: Sol, MC, Casa 2
        mc_sign = normalize_sign(houses.get(10, {}).get("sign", "Unknown"))
        mc_ruler = SIGN_RULERS.get(mc_sign, "Unknown")
        sun_planet = planets.get("Sun", {"name": "Sun", "sign": "Unknown", "house": 1, "degree": 0.0})
        h2_sign = normalize_sign(houses.get(2, {}).get("sign", "Unknown"))

        # Tríada del Cliente: Casa 7, 8, 11 + Venus
        h7_sign = normalize_sign(houses.get(7, {}).get("sign", "Unknown"))
        h8_sign = normalize_sign(houses.get(8, {}).get("sign", "Unknown"))
        h11_sign = normalize_sign(houses.get(11, {}).get("sign", "Unknown"))
        venus_planet = planets.get("Venus", {"name": "Venus", "sign": "Unknown", "house": 1, "degree": 0.0})

        return {
            "domain": "western",
            "planets": planets,
            "houses": houses,
            "aspects_count": len(aspects),
            "aspects_sample": aspects[:15],
            "arroyo_elements": {
                "counts": element_counts,
                "percentages": element_percentages,
                "dominant_element": dominant_element,
                "water_houses": water_houses,
            },
            "tripod_of_iron": {
                "sun": sun_planet,
                "midheaven_house_10": {"sign": mc_sign, "ruler": mc_ruler},
                "house_2_wealth": {"sign": h2_sign},
            },
            "client_triad": {
                "house_7_mirror": h7_sign,
                "house_8_high_ticket": h8_sign,
                "house_11_community": h11_sign,
                "venus": venus_planet,
            },
            "source_files": list(self.raw_data_map.keys()),
        }

    def render_markdown_feed(self) -> str:
        """Renders the comprehensive Gold Feed markdown for Western Tropical."""
        d = self.synthesize()
        elem = d["arroyo_elements"]
        tripod = d["tripod_of_iron"]
        triad = d["client_triad"]

        lines = [
            "# Feed Enciclopédico de Astrología Occidental Tropical & Psicológica",
            "",
            "## 1. Balance de Elementos de Stephen Arroyo & Casas de Agua",
            f"- **Elemento Dominante de Esencia:** {elem['dominant_element']} ({ELEMENT_TRANSLATION.get(elem['dominant_element'], elem['dominant_element'])})",
            f"- **Distribución de Elementos:** Fuego: {elem['percentages']['Fire']}% | Tierra: {elem['percentages']['Earth']}% | Aire: {elem['percentages']['Air']}% | Agua: {elem['percentages']['Water']}%",
            "- **Casas de Agua (Transformación Psíquica y Memoria Inconsciente):**",
            f"  * Casa 4 (Raíces / Alma Privada): Cúspide en {elem['water_houses'][4].get('sign', 'N/D')}",
            f"  * Casa 8 (Alquimia / Valor Compartido): Cúspide en {elem['water_houses'][8].get('sign', 'N/D')}",
            f"  * Casa 12 (Trascendencia / Inconsciente Colectivo): Cúspide en {elem['water_houses'][12].get('sign', 'N/D')}",
            "",
            "## 2. Trípode de Hierro de la Marca (Fundación Arquetípica)",
            f"- **Sol (Core Purpose / El 'Por Qué'):** {tripod['sun'].get('sign', 'N/D')} en Casa {tripod['sun'].get('house', 'N/D')}",
            f"- **Medio Cielo / Casa 10 (Oficio, Autoridad Pública y Misión Comercial):** Signo {tripod['midheaven_house_10']['sign']} (Regente: {tripod['midheaven_house_10']['ruler']})",
            f"- **Casa 2 (Arquitectura de Precios, Monetización y Valor Auto-percibido):** Cúspide en {tripod['house_2_wealth']['sign']}",
            "",
            "## 3. Tríada Sistémica del Cliente Ideal (ICP)",
            f"- **Casa 7 (Espejo Relacional & Clientes Frontales):** Cúspide en {triad['house_7_mirror']}",
            f"- **Casa 8 (Inversión Profunda & Transformación High-Ticket):** Cúspide en {triad['house_8_high_ticket']}",
            f"- **Casa 11 (Comunidad, Audiencia Orgánica y Alianzas):** Cúspide en {triad['house_11_community']}",
            f"- **Venus (Vector de Deseabilidad y Estética de Atracción):** En {triad['venus'].get('sign', 'N/D')} (Casa {triad['venus'].get('house', 'N/D')})",
            "",
            "## 4. Coordenadas Planetarias Swiss Ephemeris",
        ]

        for p_name, p in d["planets"].items():
            retro = " (Rx - Retrógrado)" if p.get("retrograde") else ""
            lines.append(f"- **{p_name}:** {p.get('degree', 0.0):.2f}° en {p.get('sign', 'N/D')} (Casa {p.get('house', 'N/D')}){retro}")

        lines.extend([
            "",
            "## 5. Aspectario Mayor y Geometría Psicológica",
            f"- Aspectos calculados en caché: {d['aspects_count']}",
        ])
        for a in d["aspects_sample"]:
            lines.append(f"- {a.get('body1')} {a.get('aspect')} {a.get('body2')} (Orbe: {a.get('orb', 0.0):.2f}°)")

        lines.extend([
            "",
            f"- *Archivos consultados en caché: {len(d['source_files'])}*"
        ])

        return "\n".join(lines)
