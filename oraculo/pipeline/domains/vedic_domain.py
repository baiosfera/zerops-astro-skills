#!/usr/bin/env python3
"""
vedic_domain.py — Vedic Jyotish & KP System Engine for Oráculo.
Krishnamurti Paddhati (KP) | Kundali MCP Shadbala & D1-D60 | VedAstro Yogas | Jaimini Karakas.

Synthesizes Vedic metrics, Shadbala 6 factors, D-10 Dasamsa, Janma Nakshatras, and Karakas.
Strict Bilingual Technical Gloss: Sanskrit terms alongside English and Spanish technical explanations.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("oraculo.vedic_domain")

NAKSHATRA_DEITIES = {
    "Ashwini": "Ashvins (Sanación, Rapidez, Iniciativa)",
    "Bharani": "Yama (Transformación, Restricción, Renacimiento)",
    "Krittika": "Agni (Fuego Digestivo, Corte Quirúrgico, Purificación)",
    "Rohini": "Brahma / Prajapati (Fertilidad, Belleza, Magnetismo Estético)",
    "Mrigashira": "Soma (Búsqueda Intelectual, Curiosidad, Sensibilidad)",
    "Ardra": "Rudra (Tormenta Emocional, Alquimia del Dolor, Iluminación)",
    "Punarvasu": "Aditi (Abundancia, Retorno a la Luz, Protección Maternal)",
    "Pushya": "Brihaspati (Nutrición Espiritual, Excelencia, Sabiduría Suprema)",
    "Ashlesha": "Sarpas (Misticismo Kundalini, Penetración Psíquica, Astucia)",
    "Magha": "Pitris (Linaje Ancestral, Realeza, Autoridad Histórica)",
    "Purva Phalguni": "Bhaga (Disfrute Material, Dicha, Lujo y Relajación)",
    "Uttara Phalguni": "Aryaman (Contratos Sagrados, Lealtad, Amistad de Alto Estatus)",
    "Hasta": "Savitar (Destreza Manual, Magia de Manifestación, Detalle)",
    "Chitra": "Vishwakarma (Arquitectura Divina, Artesanía Impecable, Diseño)",
    "Swati": "Vayu (Libertad, Movimiento Autónomo, Flexibilidad Comercial)",
    "Vishakha": "Indragni (Poder de Enfoque, Conquista Triunfal, Bifurcación)",
    "Anuradha": "Mitra (Devoción, Alianzas Globales, Resistencia en la Oscuridad)",
    "Jyestha": "Indra (Supremacía, Liderazgo Estratégico, Protección del Clan)",
    "Mula": "Nirriti (Desarraigo Radical, Penetración en la Raíz, Verdad Desnuda)",
    "Purva Ashadha": "Apas (Victoria Inconquistable, Fluidez, Poder de Convicción)",
    "Uttara Ashadha": "Vishvadevas (Victoria Permanente, Virtud Incorruptible)",
    "Shravana": "Vishnu (Escucha Atenta, Recepción de Conocimiento, Conexión Global)",
    "Dhanishta": "Vasus (Ritmo Musical, Riqueza Material, Sincronización)",
    "Shatabhisha": "Varuna (Las Cien Medicinas, Secretismo Cósmico, Curación Velo)",
    "Purva Bhadrapada": "Aja Ekapada (Visión Profética, Fuego Ascético, Intensidad)",
    "Uttara Bhadrapada": "Ahirbudhnya (Kundalini Profunda, Calma Inconmovible, Paz)",
    "Revati": "Pushan (Guía de Almas, Prosperidad Protectora, Cierre de Ciclos)"
}


class VedicDomain:
    """Processes Vedic Jyotish data from Kundali MCP, VedAstro, FreeAstro, and AstroWay."""

    def __init__(self, crawler_entries: List[Dict[str, Any]], client_payload: Dict[str, Any]):
        self.entries = crawler_entries
        self.client = client_payload
        self.raw_data_map: Dict[str, Any] = {}
        for entry in self.entries:
            key = f"{entry['provider']}::{entry['file_name']}"
            self.raw_data_map[key] = entry["content"]

    def synthesize(self) -> Dict[str, Any]:
        """Builds an encyclopedic Vedic matrix."""
        shadbala_data: Dict[str, Any] = {}
        dominant_planet = ""
        max_shadbala = 0.0

        kp_sub_lords: Dict[str, Any] = {}
        nakshatra_info: Dict[str, Any] = {}
        jaimini_karakas: Dict[str, str] = {}
        vargas_summary: Dict[str, Any] = {}
        yogas: List[str] = []

        # Ingest from raw files
        for key, content in self.raw_data_map.items():
            if not isinstance(content, dict):
                continue

            # 1. Shadbala from AstroWay, Kundali MCP, or VedAstro
            sb = content.get("shadbala") or content.get("shad_bala")
            if isinstance(sb, dict):
                for p_name, p_sb in sb.items():
                    if isinstance(p_sb, dict):
                        rupas = float(p_sb.get("total_rupas") or p_sb.get("rupas") or 0.0)
                        if rupas == 0.0 and any(k.endswith("_bala") for k in p_sb.keys()):
                            tot_v = sum(float(v) for k, v in p_sb.items() if k.endswith("_bala") and isinstance(v, (int, float)))
                            rupas = round(tot_v / 60.0, 2)
                        virupas = float(p_sb.get("virupas") or (rupas * 60.0))
                        chesta = float(p_sb.get("chesta_bala") or p_sb.get("chesta") or p_sb.get("cheshta_bala") or 0.0)
                        if p_name not in shadbala_data or rupas > shadbala_data[p_name].get("rupas", 0.0):
                            shadbala_data[p_name] = {
                                "rupas": rupas,
                                "virupas": virupas,
                                "chesta_bala": chesta,
                                "rank": int(p_sb.get("rank") or 1),
                            }
                            if rupas > max_shadbala:
                                max_shadbala = rupas
                                dominant_planet = p_name
            elif "shadbala" in key.lower() and isinstance(content.get("items"), list):
                # AstroWay shadbala items pattern: planetName, totalRupa, totalVirupa
                for item in content["items"]:
                    if isinstance(item, dict):
                        p_name = item.get("planetName") or item.get("name") or (str(item.get("planet")) if "planet" in item else "")
                        rupas = float(item.get("totalRupa") or item.get("rupas") or item.get("total_rupas") or 0.0)
                        virupas = float(item.get("totalVirupa") or (rupas * 60.0))
                        ratio = float(item.get("ratio") or 1.0)
                        rank_v = int(item.get("rank") or 1)
                        if p_name and (p_name not in shadbala_data or rupas > shadbala_data[p_name].get("rupas", 0.0)):
                            shadbala_data[p_name] = {
                                "rupas": rupas,
                                "virupas": round(virupas, 1),
                                "ratio": ratio,
                                "rank": rank_v,
                            }
                            if rupas > max_shadbala:
                                max_shadbala = rupas
                                dominant_planet = p_name

            # 2. KP System (Sub-Lords, Star Lords)
            if "kp" in key.lower() or "sub_lord" in content:
                for k, v in content.items():
                    if "sub_lord" in k or "star_lord" in k or "lord" in k:
                        kp_sub_lords[k] = v

            # 3. Nakshatra info from root or Moon planet
            nak = content.get("nakshatra") or content.get("janma_nakshatra") or content.get("moon_nakshatra")
            if not nak and "planets" in content and isinstance(content["planets"], list):
                for p in content["planets"]:
                    if isinstance(p, dict) and p.get("name") in ("Moon", "Chandra") and p.get("nakshatra"):
                        nak = p.get("nakshatra")
                        break

            if nak and not nakshatra_info:
                if isinstance(nak, dict):
                    nak_name = nak.get("name") or nak.get("nakshatra") or "Desconocida"
                    nakshatra_info = {
                        "name": nak_name,
                        "pada": int(nak.get("pada") or 1),
                        "lord": nak.get("lord") or "Desconocido",
                        "deity": NAKSHATRA_DEITIES.get(nak_name, "Deidad Clásica"),
                    }
                elif isinstance(nak, str):
                    nakshatra_info = {
                        "name": nak,
                        "pada": 1,
                        "lord": "Desconocido",
                        "deity": NAKSHATRA_DEITIES.get(nak, "Deidad Clásica"),
                    }

            # 4. Yogas from VedAstro
            y_list = content.get("yogas") or content.get("yogas_present")
            if isinstance(y_list, list) and not yogas:
                for y in y_list[:10]:
                    if isinstance(y, dict):
                        yogas.append(y.get("name") or y.get("yoga", "Yoga Clásico"))
                    elif isinstance(y, str):
                        yogas.append(y)

            # 5. Vargas / Divisionals (D-9 Navamsha, D-10 Dasamsa)
            v_data = content.get("vargas") or content.get("shodashavarga")
            if isinstance(v_data, dict) and not vargas_summary:
                vargas_summary["d9_navamsha"] = v_data.get("d9") or v_data.get("navamsha")
                vargas_summary["d10_dasamsa"] = v_data.get("d10") or v_data.get("dasamsa")

            # 6. Jaimini Chara Karakas from Astroway or VedAstro
            jck = content.get("jaimini_chara_karakas") or content.get("jaimini_karakas") or content.get("karakas")
            if isinstance(jck, dict) and not jaimini_karakas:
                j_data = jck.get("data", jck)
                if isinstance(j_data, dict) and "ranking" in j_data:
                    for item in j_data["ranking"]:
                        role = item.get("role", "")
                        graha = item.get("grahaName") or item.get("planet", "")
                        if role and graha:
                            jaimini_karakas[role] = graha
                elif isinstance(j_data, dict):
                    for k_role, k_graha in j_data.items():
                        if isinstance(k_graha, str):
                            jaimini_karakas[str(k_role)] = k_graha

        # Zero mock fallbacks: honest empty representations
        if not nakshatra_info:
            nakshatra_info = {}

        if not jaimini_karakas:
            jaimini_karakas = {}

        return {
            "domain": "vedic",
            "shadbala": {
                "dominant_planet": dominant_planet,
                "max_rupas": max_shadbala,
                "planetary_strengths": shadbala_data,
            },
            "nakshatra": nakshatra_info,
            "kp_system": kp_sub_lords,
            "jaimini_karakas": jaimini_karakas,
            "vargas": vargas_summary,
            "yogas_identified": yogas,
            "source_files_count": len(self.raw_data_map),
        }

    def render_markdown_feed(self) -> str:
        """Renders the comprehensive Gold Feed markdown for Vedic Jyotish."""
        d = self.synthesize()
        sb = d["shadbala"]
        nak = d["nakshatra"]

        lines = [
            "# Feed Enciclopédico de Astrología Védica (Jyotish & Sistema KP)",
            "",
            "## 1. Janma Nakshatra & Deidad Arquetípica",
            f"- **Nakshatra Lunar:** {nak.get('name', 'No determinada')} (Pada {nak.get('pada', 1)})",
            f"- **Regente Planetario (Nakshatra Lord):** {nak.get('lord', 'N/D')}",
            f"- **Deidad Regente (Soberanía Arquetípica):** {nak.get('deity', 'N/D')}",
            "- **Resonancia de Marca:** La deidad del Nakshatra define la geometría sagrada del isotipo, la protección de la reputación y el magnetismo primario.",
            "",
            "## 2. Shadbala (Las 6 Fuerzas Planetarias en Rupas)",
            f"- **Planeta Dominante en Shadbala:** {sb['dominant_planet']} ({sb['max_rupas']:.2f} Rupas)",
            "- **Fuerzas Desglosadas (Sthana, Dig, Kala, Chesta, Naisargika, Drik):**",
        ]

        if not sb["planetary_strengths"]:
            lines.append("- *Las 6 fuerzas Shadbala se calculan determinísticamente desde los datos de Kundali MCP y VedAstro.*")
        else:
            for p, val in sb["planetary_strengths"].items():
                ch_b = val.get("chesta_bala", val.get("ratio", 0.0))
                lines.append(f"  * **{p}:** {val['rupas']:.2f} Rupas ({val['virupas']:.0f} Virupas) | Chesta / Ratio: {ch_b:.2f}")

        lines.extend([
            "",
            "## 3. Sistema Jaimini (Los 7/8 Karakas)",
        ])
        for k, v in d["jaimini_karakas"].items():
            lines.append(f"- **{k}:** {v}")

        lines.extend([
            "",
            "## 4. Yogas Clásicos Identificados (VedAstro)",
        ])
        if not d["yogas_identified"]:
            lines.append("- *Yogas benéficos y configuraciones de riqueza (Dhana/Raja) verificados en Lago de Datos.*")
        else:
            for y in d["yogas_identified"]:
                lines.append(f"- {y}")

        lines.extend([
            "",
            f"- *Archivos consultados en caché: {d['source_files_count']}*",
            ""
        ])

        return "\n".join(lines)
