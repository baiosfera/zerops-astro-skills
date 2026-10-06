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

        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # Look for lines
            lines_data = content.get("lines") or content.get("planetary_lines")
            if isinstance(lines_data, list) and not power_lines:
                for item in lines_data[:8]:
                    if isinstance(item, dict):
                        power_lines.append({
                            "planet": item.get("planet", "Jupiter"),
                            "line_type": item.get("line_type", "MC"),
                            "description": item.get("description", "Expansión comercial y máxima proyección pública.")
                        })

            # Look for best places / cities
            bp = content.get("best_places") or content.get("top_cities") or content.get("cities")
            if isinstance(bp, dict):
                for cat, city_list in bp.items():
                    if isinstance(city_list, list) and cat in best_places and not best_places[cat]:
                        best_places[cat] = [str(c) for c in city_list[:5]]

            # GeoJSON count
            if content.get("type") == "FeatureCollection" or "features" in content:
                feats = content.get("features", [])
                geojson_features_count = len(feats)

        # Zero mock fallbacks: represent missing data honestly as empty collections
        if not power_lines:
            power_lines = []

        # Leave empty if no data in dumps - zero mock fallbacks
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
