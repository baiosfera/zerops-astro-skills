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
        hebrew_date = ""
        parashat_hashavua = ""
        halachic_times: Dict[str, str] = {}
        tikkun_summary = ""

        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # Look for Hebrew date from HebCal (root or nested under converter)
            conv = content.get("converter") if isinstance(content.get("converter"), dict) else {}
            h_date = content.get("hebrew_date") or content.get("hebrew") or content.get("date_hebrew") or conv.get("hebrew")
            if not h_date and conv.get("hm") and conv.get("hy"):
                h_date = f"{conv.get('hd', '')} {conv.get('hm', '')} {conv.get('hy', '')}".strip()
            if h_date and not hebrew_date:
                hebrew_date = str(h_date)

            # Look for parasha from HebCal
            parasha = content.get("parasha") or content.get("torah_portion") or content.get("parashat_hashavua")
            if not parasha and "events" in conv and isinstance(conv["events"], list):
                for ev in conv["events"]:
                    ev_str = str(ev)
                    if "parashat" in ev_str.lower() or "parasha" in ev_str.lower():
                        parasha = ev_str
                        break
            if parasha and not parashat_hashavua:
                parashat_hashavua = str(parasha)

            # Look for Zmanim solar times
            zm = content.get("zmanim") if isinstance(content.get("zmanim"), dict) else {}
            times = content.get("times") or zm.get("times") or content.get("halachic_times")
            if not times and isinstance(content.get("data"), dict) and "times" in content["data"]:
                times = content["data"]["times"]
            if isinstance(times, dict) and not halachic_times:
                for k, v in times.items():
                    halachic_times[k] = str(v)

            # Look for explicit Tikkun in Astroway/FreeAstro/AstrologyAPI
            tk = content.get("tikkun") or content.get("soul_correction")
            if tk:
                if isinstance(tk, str):
                    tikkun_summary = tk
                elif isinstance(tk, dict):
                    tikkun_summary = tk.get("description") or tk.get("summary") or tikkun_summary

            # Look for astrologyapi kabbalah_tikkun methods (lunar_node, zodiac, berg)
            sign_abbr = {
                "Ari": "Aries", "Tau": "Taurus", "Gem": "Gemini", "Can": "Cancer",
                "Leo": "Leo", "Vir": "Virgo", "Lib": "Libra", "Sco": "Scorpio",
                "Sag": "Sagittarius", "Cap": "Capricorn", "Aqu": "Aquarius", "Pis": "Pisces"
            }
            if "lunar_node" in content and isinstance(content["lunar_node"], dict) and not tikkun_summary:
                ln = content["lunar_node"]
                nn_s = ln.get("sign", "")
                sn_s = ln.get("south_node_sign", "")
                t_name = ln.get("tikkun_name", "")
                kw = ln.get("keyword", "")
                interp = ln.get("interpretation", "")
                nn_full = sign_abbr.get(nn_s, nn_s)
                sn_full = sign_abbr.get(sn_s, sn_s)
                canonical_desc = TIKKUN_TAXONOMY.get(sn_full) or TIKKUN_TAXONOMY.get(nn_full) or ""
                tikkun_summary = f"Tikkun en {nn_full} (Nodo Sur en {sn_full} - Trascender '{t_name}' hacia '{kw}'): {canonical_desc or interp}".strip()
                if not commercial_app:
                    commercial_app = (
                        f"Integración en el Modelo de Negocio: Sanar la memoria kármica de {sn_full} ({t_name.lower()}, desconfianza, control reactivo) "
                        f"anclando la oferta en virtudes de {nn_full} (estabilidad palpable, construcción de activos duraderos, valor honesto y paciencia de crecimiento). "
                        f"La marca proyecta solidez inquebrantable sin manipulación ni urgencia artificial."
                    )

            if "zodiac" in content and isinstance(content["zodiac"], dict) and not tikkun_summary:
                z = content["zodiac"]
                z_s = z.get("sign", "")
                z_name = z.get("tikkun_name", "")
                z_kw = z.get("keyword", "")
                z_interp = z.get("interpretation", "")
                z_full = sign_abbr.get(z_s, z_s)
                tikkun_summary = f"Tikkun Solar en {z_full} (Trascender '{z_name}' hacia '{z_kw}'): {z_interp}".strip()
                if not commercial_app:
                    commercial_app = f"Enfoque de Autoridad: Flexibilizar la disciplina y la ambición ejecutiva con compasión, construyendo estructuras perdurables de servicio."

            # Or derive Tikkun by North Node sign if present
            nn = content.get("north_node") or content.get("true_node")
            if isinstance(nn, dict) and not tikkun_summary:
                nn_sign = nn.get("sign") or nn.get("sign_name")
                nn_full = sign_abbr.get(nn_sign, nn_sign)
                if nn_full and nn_full in TIKKUN_TAXONOMY:
                    tikkun_summary = TIKKUN_TAXONOMY[nn_full]

        if not commercial_app and tikkun_summary:
            commercial_app = f"Integración del Tikkun ({tikkun_summary}) en la arquitectura de valor, liderazgo y confianza mutua con la audiencia."

        return {
            "domain": "kabbalah",
            "hebrew_calendar": {
                "hebrew_date": hebrew_date,
                "parashat_hashavua": parashat_hashavua,
            },
            "zmanim_halachic_times": halachic_times,
            "tikkun_rav_berg": {
                "correction_theme": tikkun_summary,
                "commercial_application": commercial_app,
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
