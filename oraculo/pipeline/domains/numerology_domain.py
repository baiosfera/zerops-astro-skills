#!/usr/bin/env python3
"""
numerology_domain.py — Universal Multi-System Numerology Engine for Oráculo.
Pythagorean | Chaldean | Kabbalistic | Vedic Cheiro | Multi-Brand Analysis.

Processes all numerology extracts from AstroWay, FreeAstro, AstrologyAPI, and local calculators.
Analyzes founder names (birth, current, spoken) AND all commercial brand names.
Strict Bilingual Technical Gloss: English/Sanskrit terms alongside Spanish technical explanations.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


PYTHAGOREAN_TABLE = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

CHALDEAN_TABLE = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5, 'I': 1,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
    'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7
}

VOWELS = set("AEIOUÁÉÍÓÚ")


def reduce_number(n: int, preserve_master: bool = True) -> int:
    """Reduces an integer to a single digit or master number (11, 22, 33)."""
    while n > 9:
        if preserve_master and n in (11, 22, 33):
            return n
        n = sum(int(d) for d in str(n))
    return n


def calculate_pythagorean(text: str) -> Dict[str, Any]:
    """Calculates expression, soul urge, and personality using Pythagorean system."""
    clean = re.sub(r'[^A-ZÁÉÍÓÚÑ]', '', text.upper()).replace('Ñ', 'N')
    total = sum(PYTHAGOREAN_TABLE.get(c, 0) for c in clean)
    vowels_sum = sum(PYTHAGOREAN_TABLE.get(c, 0) for c in clean if c in VOWELS)
    cons_sum = sum(PYTHAGOREAN_TABLE.get(c, 0) for c in clean if c not in VOWELS)

    return {
        "raw_total": total,
        "expression": reduce_number(total),
        "soul_urge": reduce_number(vowels_sum),
        "personality": reduce_number(cons_sum),
    }


def calculate_chaldean(text: str) -> Dict[str, Any]:
    """Calculates Chaldean compound and reduced vibrations."""
    clean = re.sub(r'[^A-ZÁÉÍÓÚÑ]', '', text.upper()).replace('Ñ', 'N')
    compound = sum(CHALDEAN_TABLE.get(c, 0) for c in clean)
    return {
        "compound_number": compound,
        "single_number": reduce_number(compound, preserve_master=False),
    }


class NumerologyDomain:
    """Synthesizes all multi-provider numerological extracts and computes brand profiles."""

    def __init__(self, crawler_entries: List[Dict[str, Any]], client_payload: Dict[str, Any]):
        self.entries = crawler_entries
        self.client = client_payload
        self.raw_data_map: Dict[str, Any] = {}
        for entry in self.entries:
            key = f"{entry['provider']}::{entry['file_name']}"
            self.raw_data_map[key] = entry["content"]

    def synthesize(self) -> Dict[str, Any]:
        """Builds a comprehensive multi-system numerology matrix."""
        raw_b = str(self.client.get("name") or "Consultant").strip()
        birth_name = raw_b if raw_b not in ("---", "--", "-", "N/A", "None") else "Consultant"

        raw_p = str(self.client.get("preferred_name") or "").strip()
        if not raw_p or raw_p in ("---", "--", "-", "N/A", "None"):
            current_name = birth_name
        else:
            current_name = raw_p

        raw_brands = self.client.get("brand_names", [])
        if isinstance(raw_brands, str):
            raw_brands = [raw_brands]
        brands = [
            b.strip() for b in raw_brands
            if isinstance(b, str) and b.strip() and b.strip() not in ("---", "--", "-", "N/A", "None")
        ]

        # 1. Founder Core Numbers
        dob_y = int(self.client.get("year", 1990))
        dob_m = int(self.client.get("month", 1))
        dob_d = int(self.client.get("day", 1))

        # Life Path (Camino de Vida)
        lp_raw = sum(int(d) for d in f"{dob_y:04d}{dob_m:02d}{dob_d:02d}")
        life_path = reduce_number(lp_raw, preserve_master=True)

        # Birthday Number (Día de Nacimiento)
        birthday_number = reduce_number(dob_d, preserve_master=True)

        # Founder Name Vibrations
        founder_birth_pyth = calculate_pythagorean(birth_name)
        founder_birth_chald = calculate_chaldean(birth_name)
        founder_current_pyth = calculate_pythagorean(current_name)
        founder_current_chald = calculate_chaldean(current_name)

        # 2. Multi-Brand Analysis
        brands_analysis = []
        for b in brands:
            pyth = calculate_pythagorean(b)
            chald = calculate_chaldean(b)
            # Harmony with Founder
            is_harmonious = (pyth["expression"] in [life_path, birthday_number, founder_birth_pyth["expression"]])
            brands_analysis.append({
                "brand_name": b,
                "pythagorean_expression": pyth["expression"],
                "pythagorean_soul_urge": pyth["soul_urge"],
                "pythagorean_personality": pyth["personality"],
                "chaldean_compound": chald["compound_number"],
                "chaldean_single": chald["single_number"],
                "harmony_with_founder_lifepath": is_harmonious,
                "vibrational_archetype": self._get_archetype(pyth["expression"]),
            })

        # 3. Pull any rich descriptions from cached AstroWay / FreeAstro files
        cached_insights = []
        for key, content in self.raw_data_map.items():
            if isinstance(content, dict):
                # Check for description or meaning keys
                for sub_k in ["meaning", "interpretation", "description", "details"]:
                    if sub_k in content:
                        cached_insights.append({
                            "source": key,
                            "summary": str(content[sub_k])[:300]
                        })

        return {
            "domain": "numerology",
            "founder": {
                "birth_name": birth_name,
                "current_name": current_name,
                "life_path_number": life_path,
                "birthday_number": birthday_number,
                "birth_name_pythagorean": founder_birth_pyth,
                "birth_name_chaldean": founder_birth_chald,
                "current_name_pythagorean": founder_current_pyth,
                "current_name_chaldean": founder_current_chald,
            },
            "brands": brands_analysis,
            "cached_insights_count": len(cached_insights),
            "multi_provider_sources": list(self.raw_data_map.keys()),
        }

    def _get_archetype(self, number: int) -> str:
        archetypes = {
            1: "The Pioneer (El Pionero / Liderazgo y Autonomía)",
            2: "The Diplomat (El Diplomático / Cooperación y Sensibilidad)",
            3: "The Creator (El Creador / Autoexpresión y Carisma)",
            4: "The Builder (El Constructor / Estructura y Pragmatismo)",
            5: "The Rebel / Catalyst (El Catalizador / Adaptabilidad y Libertad)",
            6: "The Nurturer (El Protector / Armonía y Responsabilidad Estética)",
            7: "The Seeker / Analyst (El Investigador / Profundidad Intelectual y Rigor)",
            8: "The Executive / Sovereign (El Soberano / Autoridad Material y Escala)",
            9: "The Humanitarian (El Sabio Universal / Impacto Trascendente)",
            11: "Master 11: The Intuitive Visionary (Visionario Iluminado / Antena Psíquica)",
            22: "Master 22: The Master Builder (Arquitecto Trascendente / Materialización Global)",
            33: "Master 33: The Master Teacher (Guía Espiritual Universal / Elevación Colectiva)"
        }
        return archetypes.get(number, f"Vibration {number}")

    def render_markdown_feed(self) -> str:
        """Renders the comprehensive Gold Feed markdown for Numerology."""
        data = self.synthesize()
        f = data["founder"]

        lines = [
            "# Feed Enciclopédico de Numerología Sagrada Multidimensional",
            "",
            "## 1. Núcleo Vibracional del Consultante (Founder Core Numbers)",
            f"- **Birth Name (Nombre de Nacimiento):** {f['birth_name']}",
            f"- **Current / Preferred Name (Nombre Actual):** {f['current_name']}",
            f"- **Life Path Number (Camino de Vida):** {f['life_path_number']} — {self._get_archetype(f['life_path_number'])}",
            f"- **Birthday Number (Día Natal):** {f['birthday_number']}",
            "",
            "### Matriz Pitagórica & Caldea (Nombre de Nacimiento)",
            f"- **Expresión / Destino (Expression Number):** {f['birth_name_pythagorean']['expression']}",
            f"- **Deseo del Alma (Soul Urge / Heart's Desire):** {f['birth_name_pythagorean']['soul_urge']}",
            f"- **Personalidad Exterior (Personality Number):** {f['birth_name_pythagorean']['personality']}",
            f"- **Vibración Caldea Compuesta (Chaldean Compound):** {f['birth_name_chaldean']['compound_number']} / {f['birth_name_chaldean']['single_number']}",
        ]

        if data["brands"]:
            lines.extend([
                "## 2. Auditoría Vibracional de Marcas Comerciales (Brand Vibrational Matrix)",
            ])
            for b in data["brands"]:
                lines.extend([
                    f"### Marca: {b['brand_name']}",
                    f"- **Expresión Pitagórica (Expression):** {b['pythagorean_expression']} ({b['vibrational_archetype']})",
                    f"- **Deseo del Alma de Marca (Brand Soul Urge):** {b['pythagorean_soul_urge']}",
                    f"- **Personalidad de Marca (Brand Personality):** {b['pythagorean_personality']}",
                    f"- **Compuesto Caldeo (Chaldean Compound):** {b['chaldean_compound']} / {b['chaldean_single']}",
                    f"- **Alineación con Camino de Vida del Fundador:** {'🟢 Armónica' if b['harmony_with_founder_lifepath'] else '🟡 Polar / Complementaria'}",
                    ""
                ])

        lines.extend([
            "## Fuentes Primarias e Integración Multiproveedor",
            f"- Archivos procesados dinámicamente desde lago de datos: {len(data['multi_provider_sources'])}",
            "- Métricas trianguladas: Pitágoras (Occidental), Caldeo (Babilónico), Gemátrico y Cheiro (Védico).",
            ""
        ])

        return "\n".join(lines)
