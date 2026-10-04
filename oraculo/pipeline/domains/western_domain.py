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

        # Extract planets and houses from available cache files
        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # Check for planets in content
            p_data = content.get("planets") or content.get("bodies") or content.get("chart_data", {}).get("planets")
            if isinstance(p_data, dict):
                for p_name, p_val in p_data.items():
                    if isinstance(p_val, dict) and p_name not in planets:
                        planets[p_name] = {
                            "name": p_name,
                            "sign": p_val.get("sign") or p_val.get("sign_name", "Unknown"),
                            "degree": float(p_val.get("degree") or p_val.get("norm_degree") or 0.0),
                            "house": int(p_val.get("house") or 1),
                            "retrograde": bool(p_val.get("is_retro") or p_val.get("retrograde", False)),
                            "speed": float(p_val.get("speed") or 1.0),
                        }
            elif isinstance(p_data, list):
                for p_item in p_data:
                    if isinstance(p_item, dict):
                        p_name = p_item.get("name") or p_item.get("planet")
                        if p_name and p_name not in planets:
                            planets[p_name] = {
                                "name": p_name,
                                "sign": p_item.get("sign") or p_item.get("sign_name", "Unknown"),
                                "degree": float(p_item.get("degree") or p_item.get("norm_degree") or 0.0),
                                "house": int(p_item.get("house") or 1),
                                "retrograde": bool(p_item.get("is_retro") or p_item.get("retrograde", False)),
                                "speed": float(p_item.get("speed") or 1.0),
                            }

            # Check for houses in content
            h_data = content.get("houses") or content.get("house_cusps") or content.get("chart_data", {}).get("houses")
            if isinstance(h_data, dict):
                for h_num, h_val in h_data.items():
                    try:
                        num = int(h_num)
                        if num not in houses and isinstance(h_val, dict):
                            houses[num] = {
                                "house": num,
                                "sign": h_val.get("sign") or h_val.get("sign_name", "Unknown"),
                                "degree": float(h_val.get("degree") or h_val.get("cusp") or 0.0),
                            }
                    except (ValueError, TypeError):
                        pass
            elif isinstance(h_data, list):
                for idx, h_item in enumerate(h_data, 1):
                    if isinstance(h_item, dict) and idx not in houses:
                        houses[idx] = {
                            "house": int(h_item.get("house") or idx),
                            "sign": h_item.get("sign") or h_item.get("sign_name", "Unknown"),
                            "degree": float(h_item.get("degree") or h_item.get("cusp") or 0.0),
                        }

            # Check for aspects
            asp_data = content.get("aspects") or content.get("chart_data", {}).get("aspects")
            if isinstance(asp_data, list) and not aspects:
                for a in asp_data:
                    if isinstance(a, dict):
                        aspects.append({
                            "body1": a.get("body1") or a.get("planet1"),
                            "body2": a.get("body2") or a.get("planet2"),
                            "aspect": a.get("aspect") or a.get("type"),
                            "orb": float(a.get("orb") or 0.0),
                        })

        # Calculate Arroyo's 4 Elements balance
        element_counts = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
        for p in planets.values():
            s = p.get("sign", "")
            for elem, signs in ELEMENT_SIGNS.items():
                if s in signs:
                    element_counts[elem] += 1

        total_pts = sum(element_counts.values()) or 1
        element_percentages = {k: round((v / total_pts) * 100, 1) for k, v in element_counts.items()}
        dominant_element = max(element_counts, key=element_counts.get) if element_counts else "Unknown"

        # Water Houses (Casas de Agua 4, 8, 12 - Stephen Arroyo)
        water_houses = {
            4: houses.get(4, {"sign": "Unknown"}),
            8: houses.get(8, {"sign": "Unknown"}),
            12: houses.get(12, {"sign": "Unknown"}),
        }

        # Trípode de Hierro: Sol, MC, Casa 2
        mc_sign = houses.get(10, {}).get("sign", "Unknown")
        mc_ruler = SIGN_RULERS.get(mc_sign, "Unknown")
        sun_planet = planets.get("Sun", {"sign": "Unknown", "house": 1})
        h2_sign = houses.get(2, {}).get("sign", "Unknown")

        # Tríada del Cliente: Casa 7, 8, 11 + Venus
        h7_sign = houses.get(7, {}).get("sign", "Unknown")
        h8_sign = houses.get(8, {}).get("sign", "Unknown")
        h11_sign = houses.get(11, {}).get("sign", "Unknown")
        venus_planet = planets.get("Venus", {"sign": "Unknown", "house": 1})

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
