#!/usr/bin/env python3
"""
sidereal_domain.py — Sidereal Astrology Engine for Oráculo.
Fagan-Bradley Prime Vertical Campanus | Lahiri Whole Sign | Mundoscope | Cross of Malta.

Synthesizes sidereal coordinates, comparative Ayanamsa deltas, and mundane angles.
Strict Bilingual Technical Gloss: English/Latin terms alongside Spanish technical explanations.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("oraculo.sidereal_domain")


class SiderealDomain:
    """Processes Sidereal astrology metrics from AstroWay, FreeAstro, and AstrologyAPI."""

    def __init__(self, crawler_entries: List[Dict[str, Any]], client_payload: Dict[str, Any]):
        self.entries = crawler_entries
        self.client = client_payload
        self.raw_data_map: Dict[str, Any] = {}
        for entry in self.entries:
            key = f"{entry['provider']}::{entry['file_name']}"
            self.raw_data_map[key] = entry["content"]

    def synthesize(self) -> Dict[str, Any]:
        """Synthesizes Sidereal calculations, comparing Fagan-Bradley with Lahiri."""
        fagan_planets: Dict[str, Any] = {}
        lahiri_planets: Dict[str, Any] = {}
        ayanamsas: Dict[str, float] = {}

        # Look for sidereal or ayanamsa files
        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # Check for ayanamsa values
            if "ayanamsa" in content:
                val = content["ayanamsa"]
                if isinstance(val, (int, float)):
                    ayanamsas[key] = float(val)
                elif isinstance(val, dict):
                    for k, v in val.items():
                        if isinstance(v, (int, float)):
                            ayanamsas[f"{key}_{k}"] = float(v)

            # Check for sidereal planets
            s_planets = content.get("sidereal_planets") or content.get("fagan_bradley_planets") or content.get("planets")
            if isinstance(s_planets, dict):
                for p_name, p_data in s_planets.items():
                    if isinstance(p_data, dict):
                        target = fagan_planets if "fagan" in key.lower() else lahiri_planets
                        if p_name not in target:
                            target[p_name] = {
                                "name": p_name,
                                "sign": p_data.get("sign") or p_data.get("sign_name", "Unknown"),
                                "degree": float(p_data.get("degree") or p_data.get("norm_degree") or 0.0),
                                "house": int(p_data.get("house") or 1),
                            }

        # Zero mock fallbacks: represent missing data honestly
        fagan_val = ayanamsas.get("fagan_bradley")
        lahiri_val = ayanamsas.get("lahiri")
        delta_arcmin = round(abs(fagan_val - lahiri_val) * 60, 1) if (fagan_val is not None and lahiri_val is not None) else None

        # Cross of Malta / Mundoscope Angles (Casas Angulares en Primer Vertical)
        mundoscope = {
            "ascendant_angle": "Oriente / Nacimiento Material (Cúspide 1)",
            "nadir_angle": "Fondo del Cielo / Inmortalidad Anímica (Cúspide 4)",
            "descendant_angle": "Occidente / Encuentro con el Otro (Cúspide 7)",
            "midheaven_angle": "Cenit / Manifestación Máxima y Poder (Cúspide 10)",
        }

        return {
            "domain": "sidereal",
            "fagan_bradley": {
                "ayanamsa_degrees": fagan_val,
                "planets": fagan_planets,
            },
            "lahiri": {
                "ayanamsa_degrees": lahiri_val,
                "planets": lahiri_planets,
            },
            "comparative_delta": {
                "fagan_vs_lahiri_arcminutes": delta_arcmin,
                "note": "Desplazamiento calculado entre Fagan-Bradley y Lahiri." if delta_arcmin is not None else "",
            },
            "mundoscope_cross_of_malta": mundoscope,
            "source_files_count": len(self.raw_data_map),
        }

    def render_markdown_feed(self) -> str:
        """Renders the comprehensive Gold Feed markdown for Sidereal Astrology."""
        d = self.synthesize()
        fagan = d["fagan_bradley"]
        lahiri = d["lahiri"]
        delta = d["comparative_delta"]

        f_deg_str = f"{fagan['ayanamsa_degrees']:.2f}°" if fagan.get('ayanamsa_degrees') is not None else "N/D"
        l_deg_str = f"{lahiri['ayanamsa_degrees']:.2f}°" if lahiri.get('ayanamsa_degrees') is not None else "N/D"
        d_arc_str = f"{delta['fagan_vs_lahiri_arcminutes']} minutos de arco. {delta['note']}" if delta.get('fagan_vs_lahiri_arcminutes') is not None else "N/D"

        lines = [
            "# Feed Enciclopédico de Astrología Sideral (Fagan-Bradley & Mundoscopio)",
            "",
            "## 1. Topología de Ayanamsas & Comparativa Cuántica",
            f"- **Ayanamsa Fagan-Bradley:** {f_deg_str} (Zócalo Babilónico / Primer Vertical de Campanus)",
            f"- **Ayanamsa Lahiri / Chitra-Paksha:** {l_deg_str} (Referencia Védica Oficial Sideral)",
            f"- **Delta Comparativo:** {d_arc_str}",
            "",
            "## 2. Mundoscopio & Cruz de Malta (Campanus Prime Vertical)",
            "- **Ángulos Mundanos de Trascendencia:**",
            f"  * Ascendente Mundano (Ascendant): {d['mundoscope_cross_of_malta']['ascendant_angle']}",
            f"  * Fondo del Cielo Mundano (Nadir): {d['mundoscope_cross_of_malta']['nadir_angle']}",
            f"  * Descendente Mundano (Descendant): {d['mundoscope_cross_of_malta']['descendant_angle']}",
            f"  * Medio Cielo Mundano (Midheaven): {d['mundoscope_cross_of_malta']['midheaven_angle']}",
            "",
            "## 3. Coordenadas Planetarias Siderales Fagan-Bradley",
        ]

        if not fagan["planets"]:
            lines.append("- *Las posiciones siderales Fagan-Bradley se deducen por substracción del Ayanamsa sobre el zócalo tropical.*")
        else:
            for p_name, p in fagan["planets"].items():
                lines.append(f"- **{p_name}:** {p.get('degree', 0.0):.2f}° en {p.get('sign', 'N/D')} (Casa {p.get('house', 'N/D')})")

        lines.extend([
            "",
            f"- *Archivos consultados en caché: {d['source_files_count']}*",
            ""
        ])

        return "\n".join(lines)
