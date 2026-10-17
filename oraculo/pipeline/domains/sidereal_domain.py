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

    def __init__(self, crawler_entries: List[Dict[str, Any]], client_payload: Dict[str, Any], tropical_planets: Optional[Dict[str, Any]] = None, tropical_houses: Optional[Dict[str, Any]] = None):
        self.entries = crawler_entries
        self.client = client_payload
        self.tropical_planets = tropical_planets or {}
        self.tropical_houses = tropical_houses or {}
        self.raw_data_map: Dict[str, Any] = {}
        for entry in self.entries:
            key = f"{entry['provider']}::{entry['file_name']}"
            self.raw_data_map[key] = entry["content"]

    def synthesize(self) -> Dict[str, Any]:
        """Synthesizes Sidereal calculations, comparing Fagan-Bradley with Lahiri."""
        fagan_planets: Dict[str, Any] = {}
        lahiri_planets: Dict[str, Any] = {}
        ayanamsas: Dict[str, float] = {}

        zodiac_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

        def _resolve_sign(val: Any) -> str:
            if isinstance(val, int) and 0 <= val < 12:
                return zodiac_names[val]
            if isinstance(val, int) and 1 <= val <= 12:
                return zodiac_names[val - 1]
            if isinstance(val, str) and val.strip():
                return val.strip()
            return "Unknown"

        # Look for sidereal or ayanamsa files
        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # Unwrap response envelopes (AstroWay / FreeAstro)
            data_body = content
            if "data" in data_body and isinstance(data_body["data"], dict):
                data_body = data_body["data"]
                if "data" in data_body and isinstance(data_body["data"], dict):
                    data_body = data_body["data"]

            # Check for ayanamsa / ayanamsha values
            ay_raw = (
                data_body.get("ayanamsa")
                or data_body.get("ayanamsha")
                or content.get("ayanamsa")
                or content.get("ayanamsha")
            )
            if ay_raw is not None:
                if isinstance(ay_raw, (int, float)):
                    ay_float = float(ay_raw)
                    ayanamsas[key] = ay_float
                    if "fagan" in key.lower():
                        ayanamsas["fagan_bradley"] = ay_float
                    else:
                        if "lahiri" not in ayanamsas:
                            ayanamsas["lahiri"] = ay_float
                elif isinstance(ay_raw, dict):
                    for k, v in ay_raw.items():
                        if isinstance(v, (int, float)):
                            ayanamsas[f"{key}_{k}"] = float(v)

            # Check for sidereal planets (dict or list format) - avoid harmonic vargas (D9/D10)
            s_planets = content.get("sidereal_planets") or content.get("fagan_bradley_planets") or (content.get("planets") if "sidereal" in key.lower() and "varga" not in key.lower() else None)
            target = fagan_planets if "fagan" in key.lower() else lahiri_planets
            if isinstance(s_planets, dict):
                for p_name, p_data in s_planets.items():
                    if isinstance(p_data, dict) and p_name not in target:
                        target[p_name] = {
                            "name": p_name,
                            "sign": _resolve_sign(p_data.get("sign") or p_data.get("sign_name")),
                            "degree": float(p_data.get("degree") or p_data.get("degreeInSign") or p_data.get("degree_in_sign") or 0.0),
                            "house": int(p_data.get("house") or 1),
                        }
            elif isinstance(s_planets, list):
                for p_item in s_planets:
                    if isinstance(p_item, dict):
                        p_name = p_item.get("name") or p_item.get("planet")
                        if p_name and p_name not in target:
                            target[p_name] = {
                                "name": p_name,
                                "sign": _resolve_sign(p_item.get("sign") or p_item.get("sign_name")),
                                "degree": float(p_item.get("degree") or p_item.get("degreeInSign") or p_item.get("degree_in_sign") or 0.0),
                                "house": int(p_item.get("house") or 1),
                            }

        # Derive astronomical Ayanamsas if not supplied directly in cache
        if not ayanamsas.get("lahiri") and not ayanamsas.get("fagan_bradley"):
            b_year = float(self.client.get("year", 2000))
            delta_y = b_year - 2000.0
            precession_deg = delta_y * (50.29 / 3600.0)
            ayanamsas["lahiri"] = round(23.858 + precession_deg, 4)
            ayanamsas["fagan_bradley"] = round(24.739 + precession_deg, 4)
        elif "lahiri" in ayanamsas and "fagan_bradley" not in ayanamsas:
            ayanamsas["fagan_bradley"] = round(ayanamsas["lahiri"] + (55.0 / 60.0), 4)
        elif "fagan_bradley" in ayanamsas and "lahiri" not in ayanamsas:
            ayanamsas["lahiri"] = round(ayanamsas["fagan_bradley"] - (55.0 / 60.0), 4)

        fagan_val = ayanamsas.get("fagan_bradley")
        lahiri_val = ayanamsas.get("lahiri")

        # Mathematical astronomical derivation: lambda_sidereal = (lambda_tropical - ayanamsa) % 360
        if self.tropical_planets:
            for p_name, p_data in self.tropical_planets.items():
                if not isinstance(p_data, dict):
                    continue
                t_long = p_data.get("longitude")
                if t_long is None and "degree" in p_data and "sign" in p_data:
                    sign_str = str(p_data.get("sign"))
                    if sign_str in zodiac_names:
                        s_idx = zodiac_names.index(sign_str)
                        t_long = (s_idx * 30.0) + float(p_data.get("degree", 0.0))

                if t_long is not None:
                    # 1. Fagan-Bradley sidereal position
                    if fagan_val is not None:
                        existing = fagan_planets.get(p_name)
                        if not existing or existing.get("degree") == 0.0 or existing.get("sign") == "Unknown":
                            fb_long = (float(t_long) - fagan_val) % 360.0
                            fb_sign_idx = int(fb_long // 30)
                            fb_deg = round(fb_long % 30, 2)
                            fagan_planets[p_name] = {
                                "name": p_name,
                                "sign": zodiac_names[fb_sign_idx],
                                "degree": fb_deg,
                                "longitude": round(fb_long, 3),
                                "house": int(p_data.get("house") or 1),
                            }
                    # 2. Lahiri sidereal position
                    if lahiri_val is not None:
                        existing = lahiri_planets.get(p_name)
                        if not existing or existing.get("degree") == 0.0 or existing.get("sign") == "Unknown":
                            lah_long = (float(t_long) - lahiri_val) % 360.0
                            lah_sign_idx = int(lah_long // 30)
                            lah_deg = round(lah_long % 30, 2)
                            lahiri_planets[p_name] = {
                                "name": p_name,
                                "sign": zodiac_names[lah_sign_idx],
                                "degree": lah_deg,
                                "longitude": round(lah_long, 3),
                                "house": int(p_data.get("house") or 1),
                            }

        # Calculate Sidereal Ascendant (Lagna) and Midheaven (MC)
        fagan_asc = {}
        lahiri_asc = {}
        if self.tropical_houses:
            h1 = self.tropical_houses.get(1) or self.tropical_houses.get("1", {})
            t_asc_long = h1.get("longitude")
            if t_asc_long is None and "degree" in h1 and "sign" in h1:
                s_str = str(h1.get("sign"))
                if s_str in zodiac_names:
                    t_asc_long = (zodiac_names.index(s_str) * 30.0) + float(h1.get("degree", 0.0))

            if t_asc_long is not None:
                if fagan_val is not None:
                    fb_asc_long = (float(t_asc_long) - fagan_val) % 360.0
                    fb_asc_idx = int(fb_asc_long // 30)
                    fb_asc_deg = round(fb_asc_long % 30, 2)
                    fagan_asc = {
                        "sign": zodiac_names[fb_asc_idx],
                        "degree": fb_asc_deg,
                        "longitude": round(fb_asc_long, 3),
                        "cusp": 1,
                        "description": f"Ascendente Sideral Fagan-Bradley en {zodiac_names[fb_asc_idx]} a {fb_asc_deg:.2f}°."
                    }
                if lahiri_val is not None:
                    lah_asc_long = (float(t_asc_long) - lahiri_val) % 360.0
                    lah_asc_idx = int(lah_asc_long // 30)
                    lah_asc_deg = round(lah_asc_long % 30, 2)
                    lahiri_asc = {
                        "sign": zodiac_names[lah_asc_idx],
                        "degree": lah_asc_deg,
                        "longitude": round(lah_asc_long, 3),
                        "cusp": 1,
                        "description": f"Ascendente Sideral Lahiri (Lagna Védico) en {zodiac_names[lah_asc_idx]} a {lah_asc_deg:.2f}°."
                    }

            h10 = self.tropical_houses.get(10) or self.tropical_houses.get("10", {})
            t_mc_long = h10.get("longitude")
            if t_mc_long is None and "degree" in h10 and "sign" in h10:
                s_str = str(h10.get("sign"))
                if s_str in zodiac_names:
                    t_mc_long = (zodiac_names.index(s_str) * 30.0) + float(h10.get("degree", 0.0))

            fagan_mc = {}
            lahiri_mc = {}
            if t_mc_long is not None:
                if fagan_val is not None:
                    fb_mc_long = (float(t_mc_long) - fagan_val) % 360.0
                    fb_mc_idx = int(fb_mc_long // 30)
                    fb_mc_deg = round(fb_mc_long % 30, 2)
                    fagan_mc = {
                        "sign": zodiac_names[fb_mc_idx],
                        "degree": fb_mc_deg,
                        "longitude": round(fb_mc_long, 3),
                        "cusp": 10,
                        "description": f"Medio Cielo Sideral Fagan-Bradley en {zodiac_names[fb_mc_idx]} a {fb_mc_deg:.2f}°."
                    }
                if lahiri_val is not None:
                    lah_mc_long = (float(t_mc_long) - lahiri_val) % 360.0
                    lah_mc_idx = int(lah_mc_long // 30)
                    lah_mc_deg = round(lah_mc_long % 30, 2)
                    lahiri_mc = {
                        "sign": zodiac_names[lah_mc_idx],
                        "degree": lah_mc_deg,
                        "longitude": round(lah_mc_long, 3),
                        "cusp": 10,
                        "description": f"Medio Cielo Sideral Lahiri en {zodiac_names[lah_mc_idx]} a {lah_mc_deg:.2f}°."
                    }
        else:
            fagan_mc = {}
            lahiri_mc = {}

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
                "ascendant": fagan_asc,
                "midheaven": fagan_mc,
                "planets": fagan_planets,
            },
            "lahiri": {
                "ayanamsa_degrees": lahiri_val,
                "ascendant": lahiri_asc,
                "midheaven": lahiri_mc,
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
