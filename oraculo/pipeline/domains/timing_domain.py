#!/usr/bin/env python3
"""
timing_domain.py — Multi-Tradition Predictive Timing Engine for Oráculo.
Vimshottari Dashas (5 Levels) | Hellenistic Zodiacal Releasing | Annual Profections | Firdaria.

Synthesizes predictive chronocrator cycles from VedAstro, AstroWay, FreeAstro, and AstrologyAPI.
Strict Bilingual Technical Gloss: Sanskrit/Greek/Arabic terms alongside Spanish technical explanations.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("oraculo.timing_domain")


class TimingDomain:
    """Processes multi-tradition predictive timing cycles, Dashas, and profections."""

    def __init__(self, crawler_entries: List[Dict[str, Any]], client_payload: Dict[str, Any]):
        self.entries = crawler_entries
        self.client = client_payload
        self.raw_data_map: Dict[str, Any] = {}
        for entry in self.entries:
            key = f"{entry['provider']}::{entry['file_name']}"
            self.raw_data_map[key] = entry["content"]

    def synthesize(self) -> Dict[str, Any]:
        """Synthesizes predictive chronocrator cycles."""
        current_mahadasha = ""
        current_antardasha = ""
        dasha_dates = ""

        # Hellenistic annual profection: (age % 12) + 1
        from datetime import datetime
        birth_year = self.client.get("year")
        current_year = datetime.now().year
        if birth_year and isinstance(birth_year, int):
            age = max(0, current_year - birth_year)
            profection_house = (age % 12) + 1
        else:
            profection_house = None
        profection_lord = ""
        firdaria_current = ""
        zr_spirit_peak = ""

        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # Look for Dashas from VedAstro or Kundali
            d_info = content.get("dasha") or content.get("dashas") or content.get("current_dasha")
            if isinstance(d_info, dict):
                current_mahadasha = d_info.get("mahadasha") or d_info.get("major") or current_mahadasha
                current_antardasha = d_info.get("antardasha") or d_info.get("sub") or current_antardasha
                dasha_dates = d_info.get("period") or d_info.get("dates") or dasha_dates

            # Look for Profections
            prof = content.get("profection") or content.get("annual_profection")
            if isinstance(prof, dict):
                if prof.get("house"):
                    profection_house = int(prof.get("house"))
                profection_lord = prof.get("lord") or prof.get("ruler") or profection_lord

            # Look for Firdaria
            fird = content.get("firdaria")
            if isinstance(fird, str):
                firdaria_current = fird

            # Look for Zodiacal Releasing
            zr = content.get("zodiacal_releasing")
            if isinstance(zr, str):
                zr_spirit_peak = zr

        commercial_meaning = f"Ventana bajo regencia de {current_mahadasha}-{current_antardasha}." if (current_mahadasha and current_antardasha) else ""
        activation_area = f"Casa {profection_house}: Activación por ciclo profectivo anual." if profection_house else ""

        return {
            "domain": "timing",
            "vimshottari_dasha": {
                "mahadasha": current_mahadasha,
                "antardasha": current_antardasha,
                "active_window": dasha_dates,
                "commercial_meaning": commercial_meaning,
            },
            "annual_profections": {
                "active_house": profection_house,
                "time_lord_ruler": profection_lord,
                "activation_area": activation_area,
            },
            "persian_firdaria": {
                "current_period": firdaria_current,
            },
            "hellenistic_zodiacal_releasing": {
                "spirit_career_peak": zr_spirit_peak,
            },
            "source_files_count": len(self.raw_data_map),
        }

    def render_markdown_feed(self) -> str:
        """Renders the comprehensive Gold Feed markdown for Timing and Chronocrators."""
        d = self.synthesize()
        vd = d["vimshottari_dasha"]
        ap = d["annual_profections"]

        lines = [
            "# Feed Enciclopédico de Timing Predictivo & Señores del Tiempo (Cronocratores)",
            "",
            "## 1. Vimshottari Dasha Védica (Ciclos Mayores y Sub-periodos)",
            f"- **Mahadasha Activa:** {vd['mahadasha']}",
            f"- **Antardasha Activa:** {vd['antardasha']}",
            f"- **Ventana Temporal:** {vd['active_window']}",
            f"- **Significado Estratégico para Lanzamientos:** {vd['commercial_meaning']}",
            "",
            "## 2. Profecciones Anuales Helenísticas (Annual Profections)",
            f"- **Casa Profeccionada:** Casa {ap['active_house']}",
            f"- **Señor del Año (Time Lord):** {ap['time_lord_ruler']}",
            f"- **Área Temática:** {ap['activation_area']}",
            "",
            "## 3. Firdaria Persa & Liberación Zodiacal (Zodiacal Releasing)",
            f"- **Firdaria Activa:** {d['persian_firdaria']['current_period']}",
            f"- **Zodiacal Releasing (ZR) de Espíritu (Carrera y Reputación):** {d['hellenistic_zodiacal_releasing']['spirit_career_peak']}",
            "",
            f"- *Archivos consultados en caché: {d['source_files_count']}*",
            ""
        ]

        return "\n".join(lines)
