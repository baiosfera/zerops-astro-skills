#!/usr/bin/env python3
"""
bazi_domain.py — BaZi Chinese Astrology & Four Pillars Engine for Oráculo.
True Solar Time | 4 Pillars (JiaZi) | 10 Gods (Shi Shen) | Yong Shen | TCM Meridian Health.

Synthesizes BaZi Chinese Metaphysics from bazi_mcp, FreeAstro, and AstroWay.
Strict Bilingual Technical Gloss: Pinyin/Chinese terms alongside Spanish technical explanations.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("oraculo.bazi_domain")

STEMS_ELEMENTS = {
    "Jia": ("Wood", "Yang"), "Yi": ("Wood", "Yin"),
    "Bing": ("Fire", "Yang"), "Ding": ("Fire", "Yin"),
    "Wu": ("Earth", "Yang"), "Ji": ("Earth", "Yin"),
    "Geng": ("Metal", "Yang"), "Xin": ("Metal", "Yin"),
    "Ren": ("Water", "Yang"), "Gui": ("Water", "Yin"),
}

ELEMENT_TRANSLATIONS = {
    "Wood": "Madera (Crecimiento, Visión, Expansión)",
    "Fire": "Fuego (Claridad, Pasión, Visibilidad)",
    "Earth": "Tierra (Estabilidad, Nutrición, Confianza)",
    "Metal": "Metal (Estructura, Disciplina, Precisión)",
    "Water": "Agua (Sabiduría, Flujo, Profundidad)",
}

TCM_ORGAN_MAP = {
    "Wood": "Hígado y Vesícula Biliar (Tensión ocular, ira, visión estratégica)",
    "Fire": "Corazón e Intestino Delgado (Circulación, alegría, presencia radiante)",
    "Earth": "Bazo y Estómago (Digestión, rumiación mental, arraigo pragmático)",
    "Metal": "Pulmones e Intestino Grueso (Respiración, soltar duelos, límites)",
    "Water": "Riñones y Vejiga (Energía vital Jing, miedos, reservas profundas)",
}


class BaZiDomain:
    """Processes Chinese Astrology, Four Pillars, and TCM health metrics."""

    def __init__(self, crawler_entries: List[Dict[str, Any]], client_payload: Dict[str, Any]):
        self.entries = crawler_entries
        self.client = client_payload
        self.raw_data_map: Dict[str, Any] = {}
        for entry in self.entries:
            key = f"{entry['provider']}::{entry['file_name']}"
            self.raw_data_map[key] = entry["content"]

    def synthesize(self) -> Dict[str, Any]:
        """Synthesizes BaZi Four Pillars, Day Master, 10 Gods, and Yong Shen."""
        four_pillars: Dict[str, Any] = {}
        day_master = ""
        dm_element = ""
        dm_polarity = ""
        yong_shen = ""

        ten_gods: Dict[str, str] = {}
        tcm_balance: Dict[str, Any] = {}

        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # Look for four pillars
            fp = content.get("four_pillars") or content.get("pillars") or content.get("bazi_chart")
            if isinstance(fp, dict) and not four_pillars:
                four_pillars = fp

            # Look for Day Master
            dm = content.get("day_master") or content.get("dm")
            if dm and isinstance(dm, (str, dict)):
                if isinstance(dm, str):
                    day_master = dm
                elif isinstance(dm, dict):
                    day_master = dm.get("name") or dm.get("stem") or day_master
                    dm_element = dm.get("element", dm_element)
                    dm_polarity = dm.get("polarity", dm_polarity)

            # Look for Yong Shen (Useful God)
            ys = content.get("yong_shen") or content.get("useful_god") or content.get("favorable_element")
            if ys and isinstance(ys, str):
                yong_shen = ys

            # 10 Gods (Shi Shen)
            sg = content.get("ten_gods") or content.get("shi_shen")
            if isinstance(sg, dict) and not ten_gods:
                for k, v in sg.items():
                    ten_gods[k] = str(v)

        # Zero mock fallbacks if raw nested format missing
        if not four_pillars:
            four_pillars = {}

        # TCM organ balance
        tcm_balance = {
            "predominant_organs": TCM_ORGAN_MAP.get(dm_element, "Sistema Integral"),
            "elemental_nourishment": f"Nutrir el elemento balancín ({yong_shen}) para optimizar vitalidad y claridad mental.",
        }

        return {
            "domain": "bazi",
            "four_pillars": four_pillars,
            "day_master": {
                "name": day_master,
                "element": dm_element,
                "polarity": dm_polarity,
                "archetype": f"{dm_polarity} {dm_element}".strip() or "Arquetipo BaZi",
            },
            "yong_shen": {
                "element": yong_shen,
                "translation": ELEMENT_TRANSLATIONS.get(yong_shen, yong_shen),
                "strategic_role": f"Elemento Balancín y Correctivo: {yong_shen}" if yong_shen else "Balance Elemental",
            },
            "ten_gods": ten_gods,
            "tcm_health": tcm_balance,
            "source_files_count": len(self.raw_data_map),
        }

    def render_markdown_feed(self) -> str:
        """Renders the comprehensive Gold Feed markdown for BaZi."""
        d = self.synthesize()
        dm = d["day_master"]
        ys = d["yong_shen"]
        fp = d["four_pillars"]

        lines = [
            "# Feed Enciclopédico de Metafísica China BaZi (Cuatro Pilares del Destino)",
            "",
            "## 1. Amo del Día (Day Master / 日主 Ri Zhu)",
            f"- **Day Master:** {dm.get('name', 'N/D')} ({dm.get('archetype', 'Arquetipo')})",
            f"- **Elemento y Polaridad:** {dm.get('element', 'N/D')} {dm.get('polarity', '')}",
            "- **Resonancia Psicológica y de Negocio:** Define la naturaleza íntima del consultante, su ritmo de combustión mental y su postura ante el mercado.",
            "",
            "## 2. Los Cuatro Pilares (JiaZi / 四柱)",
        ]

        for p_name, p_val in fp.items():
            if isinstance(p_val, dict):
                lines.append(f"- **{p_name.replace('_', ' ').title()}:** Tronco {p_val.get('stem', 'N/D')} / Rama {p_val.get('branch', 'N/D')} ({p_val.get('element', '')})")
            else:
                lines.append(f"- **{p_name.replace('_', ' ').title()}:** {p_val}")

        lines.extend([
            "",
            "## 3. Elemento Balancín y Correctivo (Yong Shen / 用神)",
            f"- **Yong Shen Identificado:** {ys.get('element', 'N/D')} ({ys.get('translation', 'N/D')})",
            f"- **Función Estratégica en Marca:** {ys['strategic_role']}",
            "- **Aplicación en Paleta de Color:** El Yong Shen dicta el color correctivo y de contraste indispensable en el Brandbook para evitar la fatiga psíquica del fundador.",
            "",
            "## 4. Balance de Medicina Tradicional China (TCM & Cinco Elementos)",
            f"- **Meridianos y Órganos Clave:** {d['tcm_health']['predominant_organs']}",
            f"- **Pauta de Regulación Vital:** {d['tcm_health']['elemental_nourishment']}",
            "",
            f"- *Archivos consultados en caché: {d['source_files_count']}*",
            ""
        ])

        return "\n".join(lines)
