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

            # Look for Human Design properties: nested or directly at root (AstroWay unwrapped)
            hd = content.get("human_design") or content.get("bodygraph")
            if not hd and ("type" in content and ("strategy" in content or "authority" in content or "centers" in content)):
                hd = content

            if isinstance(hd, dict):
                if not hd_type and hd.get("type"):
                    hd_type = str(hd.get("type"))
                if not strategy and hd.get("strategy"):
                    strategy = str(hd.get("strategy"))
                if not authority and hd.get("authority"):
                    authority = str(hd.get("authority"))
                if not profile and hd.get("profile"):
                    prof_val = hd.get("profile")
                    if isinstance(prof_val, dict):
                        profile = prof_val.get("profile") or f"{prof_val.get('personalityLine')}/{prof_val.get('designLine')}"
                    else:
                        profile = str(prof_val)
                if not cross and (hd.get("cross") or hd.get("incarnation_cross")):
                    cross_val = hd.get("cross") or hd.get("incarnation_cross")
                    if isinstance(cross_val, dict):
                        cross = cross_val.get("name") or str(cross_val)
                    else:
                        cross = str(cross_val)

                # Centers (AstroWay centers is a list of dicts: [{"name": "Head", "defined": False, "open": True}, ...])
                if "centers" in hd and isinstance(hd["centers"], list) and not defined_centers:
                    for c in hd["centers"]:
                        if isinstance(c, dict):
                            c_name = c.get("name") or "Unknown"
                            if c.get("defined") is True:
                                defined_centers.append(c_name)
                            elif c.get("open") is True or c.get("defined") is False:
                                open_centers.append(c_name)
                        elif isinstance(c, str):
                            defined_centers.append(c)

                if "defined_centers" in hd and isinstance(hd["defined_centers"], list) and not defined_centers:
                    defined_centers = [str(c) for c in hd["defined_centers"]]
                if "open_centers" in hd and isinstance(hd["open_centers"], list) and not open_centers:
                    open_centers = [str(c) for c in hd["open_centers"]]

                # Channels (AstroWay channels is a list of dicts: [{"gate1": 3, "gate2": 60, "centerA": "Sacral", "centerB": "Root"}, ...])
                if "channels" in hd and isinstance(hd["channels"], list) and not active_channels:
                    for ch in hd["channels"]:
                        if isinstance(ch, dict):
                            g1 = ch.get("gate1") or ch.get("from_gate")
                            g2 = ch.get("gate2") or ch.get("to_gate")
                            cA = ch.get("centerA") or ""
                            cB = ch.get("centerB") or ""
                            if g1 and g2:
                                active_channels.append(f"{g1}-{g2} ({cA}-{cB})" if (cA and cB) else f"{g1}-{g2}")
                            elif "name" in ch:
                                active_channels.append(str(ch["name"]))
                        else:
                            active_channels.append(str(ch))

            # Look for Cosmobiology midpoints or 90 dial
            cb = content.get("cosmobiology") or content.get("dial_90") or content.get("midpoints")
            if not cb and ("dial90" in content or "midpoints" in content):
                cb = content
            if isinstance(cb, dict):
                mp_list = cb.get("midpoints") or cb.get("aspects_90") or cb.get("points")
                if isinstance(mp_list, list) and not cosmo_midpoints:
                    for mp in mp_list[:6]:
                        if isinstance(mp, dict):
                            cosmo_midpoints.append(f"{mp.get('planet1', '')}/{mp.get('planet2', '')} = {mp.get('focal', '')}")
                        else:
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
