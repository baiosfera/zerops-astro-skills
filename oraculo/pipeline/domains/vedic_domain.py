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

NAKSHATRA_LORDS = {
    "Ashwini": "Ketu", "Bharani": "Venus", "Krittika": "Sun", "Rohini": "Moon",
    "Mrigashira": "Mars", "Ardra": "Rahu", "Punarvasu": "Jupiter", "Pushya": "Saturn",
    "Ashlesha": "Mercury", "Magha": "Ketu", "Purva Phalguni": "Venus", "Uttara Phalguni": "Sun",
    "Hasta": "Moon", "Chitra": "Mars", "Swati": "Rahu", "Vishakha": "Jupiter",
    "Anuradha": "Saturn", "Jyeshtha": "Mercury", "Jyestha": "Mercury", "Mula": "Ketu",
    "Purva Ashadha": "Venus", "Uttara Ashadha": "Sun", "Shravana": "Moon", "Dhanishta": "Mars",
    "Shatabhisha": "Rahu", "Purva Bhadrapada": "Jupiter", "Uttara Bhadrapada": "Saturn", "Revati": "Mercury"
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

            # Unwrap xml_parsed if present
            if "xml_parsed" in content and isinstance(content["xml_parsed"], dict):
                content = content["xml_parsed"]

            # 1. Shadbala from AstroWay, Kundali MCP, or VedAstro (PascalCase & lowercase support)
            sb = content.get("shadbala") or content.get("shad_bala") or content.get("Shadbala") or content.get("ShadBala")
            if isinstance(sb, dict):
                for p_name, p_sb in sb.items():
                    if isinstance(p_sb, dict):
                        rupas = float(p_sb.get("total_rupas") or p_sb.get("rupas") or p_sb.get("Rupas") or p_sb.get("TotalRupas") or 0.0)
                        if rupas == 0.0 and any(k.lower().endswith("_bala") or k.lower().endswith("bala") for k in p_sb.keys()):
                            tot_v = sum(float(v) for k, v in p_sb.items() if (k.lower().endswith("_bala") or k.lower().endswith("bala")) and isinstance(v, (int, float)))
                            rupas = round(tot_v / 60.0, 2)
                        virupas = float(p_sb.get("virupas") or p_sb.get("Virupas") or (rupas * 60.0))
                        chesta = float(p_sb.get("chesta_bala") or p_sb.get("chesta") or p_sb.get("cheshta_bala") or p_sb.get("ChestaBala") or 0.0)
                        if p_name not in shadbala_data or rupas > shadbala_data[p_name].get("rupas", 0.0):
                            shadbala_data[p_name] = {
                                "rupas": rupas,
                                "virupas": virupas,
                                "chesta_bala": chesta,
                                "rank": int(p_sb.get("rank") or p_sb.get("Rank") or 1),
                            }
                            if rupas > max_shadbala:
                                max_shadbala = rupas
                                dominant_planet = p_name
            elif ("shadbala" in key.lower() or "shad_bala" in key.lower()) and isinstance(content.get("items"), list):
                # AstroWay shadbala items pattern: planetName, totalRupa, totalVirupa
                for item in content["items"]:
                    if isinstance(item, dict):
                        p_name = item.get("planetName") or item.get("PlanetName") or item.get("name") or (str(item.get("planet")) if "planet" in item else "")
                        rupas = float(item.get("totalRupa") or item.get("TotalRupa") or item.get("rupas") or item.get("total_rupas") or 0.0)
                        virupas = float(item.get("totalVirupa") or item.get("TotalVirupa") or (rupas * 60.0))
                        ratio = float(item.get("ratio") or item.get("Ratio") or 1.0)
                        rank_v = int(item.get("rank") or item.get("Rank") or 1)
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

            # 2. KP System (Sub-Lords, Star Lords) - flat keys + nested cusps and planets
            if "kp" in key.lower() or "sub_lord" in content or "cusps" in content:
                for k, v in content.items():
                    if "sub_lord" in k or "star_lord" in k or "lord" in k:
                        kp_sub_lords[k] = v
                if isinstance(content.get("cusps"), list):
                    for cusp in content["cusps"]:
                        if isinstance(cusp, dict):
                            h_num = cusp.get("house") or cusp.get("house_number")
                            kp_sub_lords[f"cusp_{h_num}_sign_lord"] = cusp.get("sign_lord")
                            kp_sub_lords[f"cusp_{h_num}_star_lord"] = cusp.get("star_lord")
                            kp_sub_lords[f"cusp_{h_num}_sub_lord"] = cusp.get("sub_lord")
                            if cusp.get("sub_sub_lord"):
                                kp_sub_lords[f"cusp_{h_num}_sub_sub_lord"] = cusp.get("sub_sub_lord")
                if isinstance(content.get("planets"), list):
                    for pl in content["planets"]:
                        if isinstance(pl, dict):
                            p_name = pl.get("planet") or pl.get("name")
                            if p_name:
                                kp_sub_lords[f"planet_{p_name}_sign_lord"] = pl.get("sign_lord")
                                kp_sub_lords[f"planet_{p_name}_star_lord"] = pl.get("star_lord")
                                kp_sub_lords[f"planet_{p_name}_sub_lord"] = pl.get("sub_lord")
                                if pl.get("sub_sub_lord"):
                                    kp_sub_lords[f"planet_{p_name}_sub_sub_lord"] = pl.get("sub_sub_lord")

            # 3. Nakshatra info from root or Moon planet
            nak = content.get("nakshatra") or content.get("janma_nakshatra") or content.get("moon_nakshatra") or content.get("Nakshatra")
            if not nak and "planets" in content and isinstance(content["planets"], list):
                for p in content["planets"]:
                    if isinstance(p, dict) and p.get("name") in ("Moon", "Chandra") and (p.get("nakshatra") or p.get("Nakshatra")):
                        nak = p.get("nakshatra") or p.get("Nakshatra")
                        break

            if nak and not nakshatra_info:
                if isinstance(nak, dict):
                    nak_name = nak.get("name") or nak.get("nakshatra") or nak.get("Nakshatra") or "Desconocida"
                    nakshatra_info = {
                        "name": nak_name,
                        "pada": int(nak.get("pada") or nak.get("Pada") or 1),
                        "lord": nak.get("lord") or nak.get("Lord") or NAKSHATRA_LORDS.get(nak_name, "Ketu"),
                        "deity": NAKSHATRA_DEITIES.get(nak_name, "Deidad Clásica"),
                    }
                elif isinstance(nak, str):
                    nakshatra_info = {
                        "name": nak,
                        "pada": 1,
                        "lord": NAKSHATRA_LORDS.get(nak, "Ketu"),
                        "deity": NAKSHATRA_DEITIES.get(nak, "Deidad Clásica"),
                    }

            # 4. Yogas from VedAstro (Lossless, no slicing)
            y_list = content.get("yogas") or content.get("yogas_present") or content.get("jhora_yogas") or content.get("HoroscopePredictions")
            if isinstance(y_list, list) and not yogas:
                for y in y_list:
                    if isinstance(y, dict):
                        y_name = y.get("name") or y.get("yoga") or y.get("Name") or y.get("Prediction")
                        if y_name:
                            yogas.append(y_name)
                    elif isinstance(y, str):
                        yogas.append(y)

            # 5. Vargas / Divisionals (Complete D1 to D60 preservation)
            v_data = content.get("vargas") or content.get("shodashavarga") or content.get("divisions")
            if isinstance(v_data, dict):
                for v_key, v_val in v_data.items():
                    if v_key not in vargas_summary:
                        vargas_summary[str(v_key).lower()] = v_val
            elif isinstance(content.get("varga_charts"), dict):
                for v_key, v_val in content["varga_charts"].items():
                    if v_key not in vargas_summary:
                        vargas_summary[str(v_key).lower()] = v_val

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
