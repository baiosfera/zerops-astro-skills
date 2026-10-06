#!/usr/bin/env python3
"""
hd_cosmobiology_domain.py — Human Design & Cosmobiology Dial 90° Engine for Oráculo.
BodyGraph | 9 Centers | Type & Strategy | Profile | Incarnation Cross | Ebertin Midpoints | Uranian TNPs.

Synthesizes Human Design mechanics and Cosmobiology 90° dial planetary midpoints from AstroWay and FreeAstro.
Strict Bilingual Technical Gloss: English/German terms alongside Spanish technical explanations.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("oraculo.hd_cosmobiology_domain")


class HDCosmobiologyDomain:
    """Processes Human Design BodyGraph mechanics and Cosmobiology 90° dial coordinates."""

    def __init__(self, crawler_entries: List[Dict[str, Any]], client_payload: Dict[str, Any]):
        self.entries = crawler_entries
        self.client = client_payload
        self.raw_data_map: Dict[str, Any] = {}
        for entry in self.entries:
            key = f"{entry['provider']}::{entry['file_name']}"
            self.raw_data_map[key] = entry["content"]

    def synthesize(self) -> Dict[str, Any]:
        """Synthesizes Human Design and Cosmobiology data."""
        hd_type = ""
        strategy = ""
        authority = ""
        profile = ""
        cross = ""

        defined_centers: List[str] = []
        open_centers: List[str] = []
        active_channels: List[str] = []
        cosmo_midpoints: List[str] = []

        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # Look for Human Design properties
            hd = content.get("human_design") or content.get("bodygraph")
            if isinstance(hd, dict):
                hd_type = hd.get("type", hd_type)
                strategy = hd.get("strategy", strategy)
                authority = hd.get("authority", authority)
                profile = hd.get("profile", profile)
                cross = hd.get("incarnation_cross", cross)
                if "defined_centers" in hd and isinstance(hd["defined_centers"], list):
                    defined_centers = hd["defined_centers"]
                if "open_centers" in hd and isinstance(hd["open_centers"], list):
                    open_centers = hd["open_centers"]
                if "channels" in hd and isinstance(hd["channels"], list):
                    active_channels = [str(c) for c in hd["channels"]]

            # Look for Cosmobiology midpoints or 90 dial
            cb = content.get("cosmobiology") or content.get("dial_90") or content.get("midpoints")
            if isinstance(cb, dict):
                mp_list = cb.get("midpoints") or cb.get("aspects_90")
                if isinstance(mp_list, list) and not cosmo_midpoints:
                    for mp in mp_list[:6]:
                        cosmo_midpoints.append(str(mp))

        if not defined_centers:
            defined_centers = []
        if not open_centers:
            open_centers = []

        return {
            "domain": "hd_cosmobiology",
            "human_design": {
                "energy_type": hd_type,
                "strategy": strategy,
                "inner_authority": authority,
                "profile": profile,
                "incarnation_cross": cross,
                "defined_centers": defined_centers,
                "open_centers": open_centers,
                "active_channels": active_channels,
            },
            "cosmobiology_dial_90": {
                "ebertin_midpoints": cosmo_midpoints,
                "uranian_tnps_active": "",
            },
            "source_files_count": len(self.raw_data_map),
        }

    def render_markdown_feed(self) -> str:
        """Renders the comprehensive Gold Feed markdown for Human Design & Cosmobiology."""
        d = self.synthesize()
        hd = d["human_design"]
        cb = d["cosmobiology_dial_90"]

        lines = [
            "# Feed Enciclopédico de Diseño Humano & Cosmobiología (Dial 90°)",
            "",
            "## 1. Mecánica del Diseño Humano (BodyGraph SSoT)",
            f"- **Tipo Energético (Energy Type):** {hd['energy_type']}",
            f"- **Estrategia Vital de Negocios (Strategy):** {hd['strategy']}",
            f"- **Autoridad Interna de Decisión (Authority):** {hd['inner_authority']}",
            f"- **Perfil Arquetípico (Profile):** {hd['profile']}",
            f"- **Cruz de Encarnación (Incarnation Cross):** {hd['incarnation_cross']}",
            "",
            "### Centros Definidos vs Centros Abiertos (Dinámica de Sabiduría)",
            f"- **Centros Definidos (Emisión Constante):** {', '.join(hd['defined_centers'])}",
            f"- **Centros Abiertos (Recepción y Sabiduría del Mercado):** {', '.join(hd['open_centers'])}",
            "- **Impacto en Funnels y Ventas:** El tipo de energía y la estrategia determinan cómo debe posicionarse la oferta comercial según la autoridad y el diseño energético individual.",
            "",
            "## 2. Cosmobiología de Reinhold Ebertin & Dial de 90° (Halbsummen)",
            "- **Puntos Medios Clave (Midpoints):**",
        ]

        for mp in cb["ebertin_midpoints"]:
            lines.append(f"  * {mp}")

        lines.extend([
            f"- **Puntos Transneptunianos Uranianos (TNPs):** {cb['uranian_tnps_active']}",
            "",
            f"- *Archivos consultados en caché: {d['source_files_count']}*",
            ""
        ])

        return "\n".join(lines)
