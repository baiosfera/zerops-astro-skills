#!/usr/bin/env python3
"""
acg_domain.py — Astrocartography (ACG) & Relocation Astrology Engine for Oráculo.
Planetary Lines (MC, AS, DS, IC) | Local Space Horizon Compass | Best Places (34,028 Cities) | GeoJSON.

Synthesizes planetary geographical lines, zenith crossings, and relocation power zones from AstroWay and FreeAstro.
Strict Bilingual Technical Gloss: English terms alongside Spanish technical explanations.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("oraculo.acg_domain")


class ACGDomain:
    """Processes Astrocartography, World Lines, Local Space, and City rankings."""

    def __init__(self, crawler_entries: List[Dict[str, Any]], client_payload: Dict[str, Any]):
        self.entries = crawler_entries
        self.client = client_payload
        self.raw_data_map: Dict[str, Any] = {}
        for entry in self.entries:
            key = f"{entry['provider']}::{entry['file_name']}"
            self.raw_data_map[key] = entry["content"]

    def synthesize(self) -> Dict[str, Any]:
        """Synthesizes Astrocartography power lines and city recommendations."""
        power_lines: List[Dict[str, str]] = []
        best_places: Dict[str, List[str]] = {
            "career_wealth": [],
            "love_partnerships": [],
            "creativity_fame": [],
            "spiritual_retreat": [],
        }
        geojson_features_count = 0

        seen_line_keys = set()

        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # Unwrap response envelopes (AstroWay / FreeAstro)
            data_body = content
            if isinstance(data_body, dict) and "data" in data_body and isinstance(data_body["data"], dict):
                data_body = data_body["data"]
                if "data" in data_body and isinstance(data_body["data"], dict):
                    data_body = data_body["data"]

            # Look for lines (FreeAstro: body, angle; AstroWay: planet, line_type)
            lines_data = data_body.get("lines") or data_body.get("planetary_lines") or content.get("lines") or content.get("planetary_lines")
            if isinstance(lines_data, list) and len(power_lines) < 8:
                for item in lines_data:
                    if isinstance(item, dict):
                        planet_raw = item.get("planet") or item.get("body")
                        angle_raw = item.get("line_type") or item.get("angle")
                        if planet_raw and angle_raw:
                            p_cap = str(planet_raw).capitalize()
                            a_up = str(angle_raw).upper()
                            line_sig = f"{p_cap}_{a_up}"
                            if line_sig not in seen_line_keys:
                                seen_line_keys.add(line_sig)
                                desc = item.get("description") or (
                                    "Expansión comercial, reputación y máxima proyección pública." if a_up == "MC"
                                    else "Identidad visual de marca y magnetismo personal." if a_up == "ASC"
                                    else "Alianzas estratégicas y atracción de clientes ideales." if a_up == "DSC"
                                    else "Fundaciones sólidas de marca y raíces operativas." if a_up == "IC"
                                    else f"Línea de influencia geográfica de {p_cap} en {a_up}."
                                )
                                power_lines.append({
                                    "planet": p_cap,
                                    "line_type": a_up,
                                    "description": desc
                                })
                                if len(power_lines) >= 8:
                                    break

            # Look for best places / cities (AstroWay places, FreeAstro recommendations)
            bp = data_body.get("best_places") or data_body.get("top_cities") or data_body.get("cities") or content.get("best_places")
            if isinstance(bp, dict):
                for cat, city_list in bp.items():
                    if isinstance(city_list, list) and cat in best_places and not best_places[cat]:
                        best_places[cat] = [str(c) for c in city_list[:5]]

            # AstroWay best_places format: {"category": {"id": "career"}, "places": [{"name": "Ishim", "country": "Russia"}]}
            if "category" in data_body and "places" in data_body and isinstance(data_body["places"], list):
                cat_info = data_body.get("category", {})
                cat_id = cat_info.get("id", "").lower() if isinstance(cat_info, dict) else str(cat_info).lower()
                target_cat = (
                    "career_wealth" if "career" in cat_id or "wealth" in cat_id
                    else "love_partnerships" if "love" in cat_id or "partner" in cat_id
                    else "creativity_fame" if "creativ" in cat_id or "fame" in cat_id
                    else "spiritual_retreat" if "spirit" in cat_id or "retreat" in cat_id
                    else "career_wealth"
                )
                if not best_places[target_cat]:
                    c_list = []
                    for p_item in data_body["places"][:5]:
                        if isinstance(p_item, dict):
                            p_name = p_item.get("name") or "Desconocido"
                            p_country = p_item.get("country") or ""
                            c_list.append(f"{p_name}, {p_country}".strip(", "))
                        elif isinstance(p_item, str):
                            c_list.append(p_item)
                    if c_list:
                        best_places[target_cat] = c_list

            # GeoJSON count
            if content.get("type") == "FeatureCollection" or "features" in content or "features" in data_body:
                feats = content.get("features") or data_body.get("features", [])
                if isinstance(feats, list):
                    geojson_features_count = max(geojson_features_count, len(feats))

        if not power_lines:
            power_lines = []

        if not best_places["career_wealth"]:
            best_places["career_wealth"] = []
        if not best_places["love_partnerships"]:
            best_places["love_partnerships"] = []

        return {
            "domain": "acg",
            "planetary_lines": power_lines,
            "best_places_ranking": best_places,
            "local_space_compass": "Brújula Azimutal Local: Vectores planetarios proyectados sobre el horizonte geográfico de 360°.",
            "geojson_features_count": geojson_features_count,
            "source_files_count": len(self.raw_data_map),
        }

    def render_markdown_feed(self) -> str:
        """Renders the comprehensive Gold Feed markdown for Astrocartography."""
        d = self.synthesize()

        lines = [
            "# Feed Enciclopédico de Astrocartografía (ACG & Relocalización Estratégica)",
            "",
            "## 1. Líneas Planetarias de Poder Geográfico (World Lines)",
        ]

        for pl in d["planetary_lines"]:
            lines.append(f"- **Línea {pl['planet']} en {pl['line_type']}:** {pl['description']}")

        lines.extend([
            "",
            "## 2. Ranking de Mejores Ciudades del Mundo (Best Places Engine - 34,028 Ciudades)",
            "### Carrera, Negocios y Riqueza (Jupiter / Sun / MC):",
        ])
        for c in d["best_places_ranking"]["career_wealth"]:
            lines.append(f"  * {c}")

        lines.extend([
            "### Alianzas, Socios y Deseabilidad (Venus / Moon / AS-DS):",
        ])
        for c in d["best_places_ranking"]["love_partnerships"]:
            lines.append(f"  * {c}")

        lines.extend([
            "",
            "## 3. Astrología del Espacio Local (Local Space Horizon)",
            f"- **Principio Operativo:** {d['local_space_compass']}",
            "- **Aplicación en Negocios:** Orientación espacial de oficinas, dirección de pauta publicitaria digital y viajes de negociación.",
            "",
            f"- *Archivos consultados en caché: {d['source_files_count']}*",
            ""
        ])

        return "\n".join(lines)
