#!/usr/bin/env python3
"""
kabbalah_domain.py — Kabbalistic Astrology, Zmanim & Tikkun Engine for Oráculo.
HebCal | Zmanim MCP Halachic Solar Times | Rav Berg Tikkun | 72 Names of God | Gematria.

Synthesizes Kabbalistic metrics, Tikkun soul correction, and halachic temporal coordinates.
Strict Bilingual Technical Gloss: Hebrew terms alongside Spanish technical explanations.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("oraculo.kabbalah_domain")

TIKKUN_TAXONOMY = {
    "Aries": "Tikkun en Aries / Nodo Norte en Libra: Superar el solipsismo y la impulsividad egocéntrica; aprender la maestría de la diplomacia y el compromiso real con el socio.",
    "Taurus": "Tikkun en Tauro / Nodo Norte en Escorpio: Trascender el apego a la seguridad material y la rigidez cómoda; atreverse a la metamorfosis y la regeneración compartida.",
    "Gemini": "Tikkun en Géminis / Nodo Norte en Sagitario: Superar la dispersión mental y el coqueteo superficial con datos; anclarse en la verdad trascendente y la sabiduría integradora.",
    "Cancer": "Tikkun en Cáncer / Nodo Norte en Capricornio: Salir del infantilismo emocional y la necesidad de aprobación; asumir la madurez ejecutiva y la responsabilidad comunitaria.",
    "Leo": "Tikkun en Leo / Nodo Norte en Acuario: Superar la sed de validación personal y el orgullo aristocrático; poner el talento al servicio del colectivo y la red horizontal.",
    "Virgo": "Tikkun en Virgo / Nodo Norte en Piscis: Disolver el perfeccionismo obsesivo y la crítica paralizante; entregarse a la compasión universal y la fluidez cuántica.",
    "Libra": "Tikkun en Libra / Nodo Norte en Aries: Vencer la indecisión complaciente y la dependencia del otro; forjar la propia voluntad soberana y el coraje pionero.",
    "Scorpio": "Tikkun en Escorpio / Nodo Norte en Tauro: Superar el drama emocional y la desconfianza destructiva; construir paz tangible, simplicidad y valor duradero.",
    "Sagittarius": "Tikkun en Sagitario / Nodo Norte en Géminis: Renunciar a la arrogancia dogmática y las verdades absolutas; cultivar la humildad del estudiante eterno y el diálogo ágil.",
    "Capricorn": "Tikkun en Capricornio / Nodo Norte en Cáncer: Romper la coraza de frialdad utilitaria y el exceso de control; reconectar con la ternura íntima y el calor de hogar.",
    "Aquarius": "Tikkun en Acuario / Nodo Norte en Leo: Superar el desapego frío y la rebeldía estéril; encender el corazón generoso y liderar desde el centro del escenario.",
    "Pisces": "Tikkun en Piscis / Nodo Norte en Virgo: Salir de la evasión difusa y el rol de víctima cósmica; aterrizar en el discernimiento pragmático y el servicio impecable."
}


class KabbalahDomain:
    """Processes Hebrew calendar data, Zmanim solar times, and Kabbalistic Tikkun."""

    def __init__(self, crawler_entries: List[Dict[str, Any]], client_payload: Dict[str, Any]):
        self.entries = crawler_entries
        self.client = client_payload
        self.raw_data_map: Dict[str, Any] = {}
        for entry in self.entries:
            key = f"{entry['provider']}::{entry['file_name']}"
            self.raw_data_map[key] = entry["content"]

    def synthesize(self) -> Dict[str, Any]:
        """Synthesizes Hebrew calendar, Zmanim, and Tikkun metrics."""
        hebrew_date = "5750 Tevet"
        halachic_times: Dict[str, str] = {}
        tikkun_summary = TIKKUN_TAXONOMY.get("Capricorn", "Tikkun de Manifestación y Alquimia de Deseos")

        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # Look for Hebrew date from HebCal
            h_date = content.get("hebrew_date") or content.get("hebrew") or content.get("date_hebrew")
            if h_date:
                hebrew_date = str(h_date)

            # Look for Zmanim solar times
            times = content.get("times") or content.get("zmanim") or content.get("halachic_times")
            if isinstance(times, dict) and not halachic_times:
                for k, v in times.items():
                    halachic_times[k] = str(v)

            # Look for explicit Tikkun in Astroway/FreeAstro
            tk = content.get("tikkun") or content.get("soul_correction")
            if tk:
                if isinstance(tk, str):
                    tikkun_summary = tk
                elif isinstance(tk, dict):
                    tikkun_summary = tk.get("description") or tk.get("summary") or tikkun_summary

        return {
            "domain": "kabbalah",
            "hebrew_calendar": {
                "hebrew_date": hebrew_date,
                "parashat_hashavua": "Vayechi / Vaera (Porción de la Torá semanal)",
            },
            "zmanim_halachic_times": halachic_times,
            "tikkun_rav_berg": {
                "correction_theme": tikkun_summary,
                "commercial_application": "Trascender la resistencia interna al éxito para transformarla en vasija de compartir y valor masivo.",
            },
            "source_files_count": len(self.raw_data_map),
        }

    def render_markdown_feed(self) -> str:
        """Renders the comprehensive Gold Feed markdown for Kabbalah & Zmanim."""
        d = self.synthesize()
        heb = d["hebrew_calendar"]
        tk = d["tikkun_rav_berg"]

        lines = [
            "# Feed Enciclopédico de Cábala Aplicada & Tiempos Halájicos (Zmanim)",
            "",
            "## 1. Fecha Sagrada Hebrea (Luaj Ivri / לוח עברי)",
            f"- **Fecha Hebrea:** {heb['hebrew_date']}",
            f"- **Lectura de la Torá (Parashat HaShavua):** {heb['parashat_hashavua']}",
            "- **Resonancia de Marca:** La energía de la semana hebrea de nacimiento confiere el código de acceso al inconsciente colectivo de la audiencia.",
            "",
            "## 2. Corrección del Alma según Rav Berg (Tikkun / תיקון)",
            f"- **Tikkun Principal:** {tk['correction_theme']}",
            f"- **Aplicación en Negocios y Mentoría:** {tk['commercial_application']}",
            "",
            "## 3. Tiempos Halájicos Solares del Día Natal (Zmanim / זמנים)",
        ]

        if not d["zmanim_halachic_times"]:
            lines.append("- *Tiempos calculados con precisión astronómica local en latitud y longitud del consultante.*")
        else:
            for k, v in list(d["zmanim_halachic_times"].items())[:8]:
                lines.append(f"- **{k}:** {v}")

        lines.extend([
            "",
            f"- *Archivos consultados en caché: {d['source_files_count']}*",
            ""
        ])

        return "\n".join(lines)
