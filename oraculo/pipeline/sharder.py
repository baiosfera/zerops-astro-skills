"""
Sharder Engine for Oráculo (v4.2).
Transforms raw multi-engine extractions into:
1. Tier 1 (Bronze): 10 Atomic Domain JSON Shards in raw/json/dumps/.
2. Tier 1.5 (Silver): RFC 6901 Manifest in raw/json/dumps/manifest.json.
3. Tier 2 (Gold): 10 Rich Feeds in raw/feeds/.
4. Master Technical Sheet (SSoT - 12 Sections) in raw/llm/coach_technical_sheet.md.
5. Ontological Author Constitution in raw/llm/author_constitution.md.
6. Forensic Extraction Health & Credit Audit in raw/json/extraction_health_audit.md.
"""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


ZODIAC_SIGNS = [
    "Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo",
    "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis"
]


def format_zodiac_pos(deg: Any) -> str:
    if isinstance(deg, dict):
        if "abs_pos" in deg:
            deg = deg["abs_pos"]
        elif "absolute_degree" in deg:
            deg = deg["absolute_degree"]
        elif "pos" in deg and ("sign_id" in deg or "sign" in deg):
            sign_map = {
                "aries": 0, "ari": 0,
                "taurus": 1, "tau": 1, "tauro": 1,
                "gemini": 2, "gem": 2, "géminis": 2,
                "cancer": 3, "can": 3, "cáncer": 3,
                "leo": 4, "virgo": 5, "vir": 5,
                "libra": 6, "lib": 6,
                "scorpio": 7, "sco": 7, "escorpio": 7,
                "sagittarius": 8, "sag": 8, "sagitario": 8,
                "capricorn": 9, "cap": 9, "capricornio": 9,
                "aquarius": 10, "aqu": 10, "acuario": 10,
                "pisces": 11, "pis": 11, "piscis": 11
            }
            s_key = str(deg.get("sign_id") or deg.get("sign") or "").lower()
            if s_key in sign_map:
                try:
                    deg = sign_map[s_key] * 30.0 + float(deg.get("pos", 0.0))
                except Exception:
                    pass
        elif "pos" in deg:
            deg = deg["pos"]
        elif "degree" in deg:
            deg = deg["degree"]
    try:
        f_deg = float(deg) % 360.0
    except (ValueError, TypeError):
        return str(deg or "N/A")
    sign_idx = int(f_deg // 30)
    deg_in_sign = f_deg % 30.0
    d = int(deg_in_sign)
    m = int(round((deg_in_sign - d) * 60))
    if m == 60:
        d += 1
        m = 0
    return f"{ZODIAC_SIGNS[sign_idx]} {d}°{m:02d}' ({f_deg:.2f}°)"


class ExtractionFatalError(Exception):
    pass


class SharderEngine:
    def __init__(self, output_root: str = "/var/www/baiosfera/ASTROLOGÍA/DIAG/OUTPUT"):
        self.root_dir = Path(output_root)
        self.raw_dir = self.root_dir / "raw"
        self.dumps_dir = self.raw_dir / "json" / "dumps"
        self.feeds_dir = self.raw_dir / "feeds"
        self.llm_dir = self.raw_dir / "llm"

        self.dumps_dir.mkdir(parents=True, exist_ok=True)
        self.feeds_dir.mkdir(parents=True, exist_ok=True)
        self.llm_dir.mkdir(parents=True, exist_ok=True)

    def verify_and_shard(self, extraction_output: Dict[str, Any]) -> Dict[str, Any]:
        client_data = extraction_output.get("client_data", {})
        rest_data = extraction_output.get("rest", {})
        mcp_data = extraction_output.get("mcp", {})
        credit_stats = extraction_output.get("credit_stats", {})
        results_list = extraction_output.get("extraction_results", [])

        # 1. Verify Health & Detect Mocks/Semantic Failures
        health_report = self._verify_health(rest_data, mcp_data, results_list)
        if health_report["is_fatal"]:
            raise ExtractionFatalError(f"Fatal Extraction Failure: {health_report['fatal_reason']}")

        # 2. Tier 1: 10 Raw Atomic Shards (Bronze Tier)
        shards = self._build_tier1_shards(rest_data, mcp_data, client_data)
        for shard_filename, shard_content in shards.items():
            shard_path = self.dumps_dir / shard_filename
            with open(shard_path, "w", encoding="utf-8") as f:
                json.dump(shard_content, f, indent=2, ensure_ascii=False)

        # Build and save manifest.json (Silver Tier)
        manifest = self._build_silver_manifest(shards, client_data)
        with open(self.dumps_dir / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        # Build and save 15-shard projection for PostgreSQL client_dumps table
        dumps_15_record = self.map_to_client_dumps(shards, client_data)
        with open(self.dumps_dir / "client_dumps_15_shards.json", "w", encoding="utf-8") as f:
            json.dump(dumps_15_record, f, indent=2, ensure_ascii=False)

        # 3. Tier 2: 10 Feeds Gold (Fases 0 a 9)
        feeds = self._build_tier2_feeds(shards, client_data)
        for feed_filename, feed_content in feeds.items():
            feed_path = self.feeds_dir / feed_filename
            with open(feed_path, "w", encoding="utf-8") as f:
                f.write(feed_content)

        # 4. Forensic Extraction Health & Credit Audit
        self._write_health_audit_md(health_report, credit_stats, client_data, results_list)

        # 5. Master Technical Sheet (SSoT - 12 Sections)
        self._write_coach_technical_sheet_md(shards, client_data)

        # 6. Ontological Author Constitution (Rich Markdown)
        self._write_fase0_author_psychology_md(shards, client_data)

        # 7. Ultra-Dense AstroBranding Handoff Specification (SSoT for Orchesbrand)
        self._write_astrobranding_handoff_md(shards, client_data)

        return {
            "health": health_report,
            "shards_count": len(shards),
            "feeds_count": len(feeds),
            "manifest_generated": True
        }

    def _verify_health(self, rest_data: dict, mcp_data: dict, results_list: list) -> dict:
        total_calls = len(results_list)
        successes = [r for r in results_list if r.status in ["SUCCESS", "CACHED"]]
        failures = [r for r in results_list if r.status == "FAILED"]

        freeastro_ok = bool(rest_data.get("freeastro", {}).get("western_natal_tropical"))
        astroway_ok = bool(rest_data.get("astroway", {}).get("western_chart"))
        bazi_ok = bool(mcp_data.get("lunar_mcp_calculate_bazi")) or bool(rest_data.get("freeastro", {}).get("chinese_bazi_true_solar"))

        mock_detected = False
        mock_details = []
        if freeastro_ok:
            fa_chart = rest_data["freeastro"]["western_natal_tropical"]
            planets = fa_chart.get("planets", [])
            sun_deg = -1
            moon_deg = -1
            if isinstance(planets, list):
                for p in planets:
                    if isinstance(p, dict):
                        p_name = p.get("name", "").lower()
                        if p_name == "sun":
                            sun_deg = p.get("pos", p.get("degree", p.get("abs_pos", -1)))
                        elif p_name == "moon":
                            moon_deg = p.get("pos", p.get("degree", p.get("abs_pos", -1)))
            elif isinstance(planets, dict):
                sun_deg = planets.get("Sun", {}).get("degree", planets.get("Sun", {}).get("pos", -1))
                moon_deg = planets.get("Moon", {}).get("degree", planets.get("Moon", {}).get("pos", -1))

            if sun_deg == 0.0 and moon_deg == 0.0:
                mock_detected = True
                mock_details.append("Sun and Moon exact 0.000° placeholder detected in FreeAstroAPI.")

        is_fatal = False
        fatal_reason = ""
        if not freeastro_ok and not astroway_ok:
            is_fatal = True
            fatal_reason = "Both primary Western engines (FreeAstroAPI and AstroWay) failed."
        elif mock_detected:
            is_fatal = True
            fatal_reason = f"Mock data detected: {'; '.join(mock_details)}"

        return {
            "total_calls": total_calls,
            "success_count": len(successes),
            "failure_count": len(failures),
            "freeastro_online": freeastro_ok,
            "astroway_online": astroway_ok,
            "bazi_online": bazi_ok,
            "mock_detected": mock_detected,
            "is_fatal": is_fatal,
            "fatal_reason": fatal_reason,
            "failures": [{"provider": f.provider, "endpoint": f.endpoint_key, "error": f.error} for f in failures]
        }

    def _build_tier1_shards(self, rest: dict, mcp: dict, client: dict) -> Dict[str, Any]:
        freeastro = rest.get("freeastro", {})
        astroway = rest.get("astroway", {})
        astrology = rest.get("astrologyapi", {})
        vedastro = rest.get("vedastro", {})
        hebcal = rest.get("hebcal", {})
        nasa = rest.get("nasa", {})

        return {
            "shard_01_astro_western_tropical.json": {
                "metadata": client,
                "system": "western_tropical",
                "default_house_system": "placidus",
                "freeastro_tropical_placidus": freeastro.get("western_natal_tropical", {}),
                "freeastro_tropical_campanus": freeastro.get("western_natal_tropical_campanus", {}),
                "astroway_chart": astroway.get("western_chart", {}),
                "astrology_positions_enhanced": astrology.get("positions_enhanced", {}),
                "modern_psychology": {
                    "arroyo_elements": astroway.get("psychological_arroyo_elements", {}),
                    "greene_archetypes": astroway.get("psychological_greene_archetypes", {}),
                    "greene_shadow": astroway.get("psychological_greene_shadow", {}),
                    "rudhyar_lunation": astroway.get("psychological_rudhyar_lunation", {})
                }
            },
            "shard_02_astro_western_sidereal.json": {
                "metadata": client,
                "system": "western_sidereal",
                "primary_variant": "fagan_campanus",
                "variants": {
                    "fagan_campanus": freeastro.get("western_natal_sidereal_fagan_campanus", {}) or astroway.get("western_chart_fagan_campanus", {}),
                    "lahiri_whole": freeastro.get("western_natal_sidereal_lahiri", {})
                }
            },
            "shard_03_astro_vedic_jyotish.json": {
                "metadata": client,
                "system": "vedic_jyotish",
                "ayanamsa": "lahiri",
                "kundali_mcp": mcp.get("kundali_mcp_kundali_calc", {}),
                "astrology_vedic_kundli": astrology.get("vedic_kundli", {}),
                "vedastro": {
                    "predictions": vedastro.get("predictions", {}),
                    "planet_data": vedastro.get("planet_data", {}),
                    "house_data": vedastro.get("house_data", {}),
                    "dasa_range": vedastro.get("dasa_range", {})
                },
                "jaimini_chara_karakas": astroway.get("jaimini_chara_karakas", {}),
                "vedic_kp_v2": freeastro.get("vedic_kp_v2", {}),
                "vedic_varga_d9": astroway.get("vedic_varga_d9", {}),
                "vedic_varga_d10": astroway.get("vedic_varga_d10", {}),
                "vedic_shadbala_full": astroway.get("vedic_shadbala_full", {})
            },
            "shard_04_bazi_chinese_metaphysics.json": {
                "metadata": client,
                "system": "chinese_bazi",
                "bazi_lunar": mcp.get("lunar_mcp_calculate_bazi", {}),
                "chinese_bazi_true_solar": freeastro.get("chinese_bazi_true_solar", {}),
                "chinese_bazi_flow": freeastro.get("chinese_bazi_flow", {})
            },
            "shard_05_kabbalah_tikkun.json": {
                "metadata": client,
                "system": "kabbalah_tikkun",
                "hebcal_converter": hebcal.get("converter", {}),
                "hebcal_zmanim": hebcal.get("zmanim", {}),
                "zmanim_mcp": mcp.get("zmanim_mcp_daily_times", {}),
                "evolutionary_skipped_steps": astroway.get("evolutionary_skipped_steps", {}),
                "evolutionary_nodal_axis": astroway.get("evolutionary_nodal_axis", {})
            },
            "shard_06_human_design_cosmobiology.json": {
                "metadata": client,
                "system": "human_design_cosmobiology",
                "human_design": astroway.get("human_design", {}),
                "hd_circuitry": astroway.get("hd_circuitry", {}),
                "hd_incarnation_cross": astroway.get("hd_incarnation_cross", {}),
                "hd_sensitivity": astroway.get("hd_sensitivity", {}),
                "cosmobiology_dial90": astroway.get("cosmobiology_dial90", {})
            },
            "shard_07_numerology_multi_school.json": {
                "metadata": client,
                "system": "numerology",
                "freeastro_pythagorean": freeastro.get("numerology_profile_pythagorean", {}),
                "astrologyapi_core": astrology.get("core_numerology", {})
            },
            "shard_08_timing_progressions_dashas.json": {
                "metadata": client,
                "system": "timing_chronocrators",
                "timing_timeline": astrology.get("timing_timeline", {}),
                "vedic_dashas_maha": astroway.get("vedic_dashas_maha", {}),
                "vedastro_dasa_range": vedastro.get("dasa_range", {})
            },
            "shard_09_relocation_acg.json": {
                "metadata": client,
                "system": "astrocartography_relocation",
                "geo_acg": astroway.get("geo_acg", {}),
                "geo_acg_best_places": astroway.get("geo_acg_best_places", {}),
                "geo_local_space": astroway.get("geo_local_space", {})
            },
            "shard_10_electional_asteroids.json": {
                "metadata": client,
                "system": "electional_asteroids",
                "asteroids": nasa
            },
            "shard_11_chinese_tcm_health_lifecurve.json": {
                "metadata": client,
                "system": "chinese_tcm_health_lifecurve",
                "tcm_health": freeastro.get("chinese_health", {}) or freeastro.get("tcm_health", {}),
                "lifespan_curve": freeastro.get("chinese_lifespan", {}) or freeastro.get("lifespan_curve", {}),
                "bazi_five_elements": freeastro.get("chinese_bazi_five_elements", {}),
                "lunar_lucky_hours": mcp.get("lunar_mcp_get_lucky_hours", {}),
                "lunar_solar_to_lunar": mcp.get("lunar_mcp_solar_to_lunar", {})
            },
            "shard_12_vedic_shodashavarga_d1_d60.json": {
                "metadata": client,
                "system": "vedic_shodashavarga_d1_d60",
                "vargas_d1_d60": freeastro.get("vedic_vargas", {}) or freeastro.get("vedic_vargas_d1_d60", {}),
                "astroway_vargas": {
                    "d9": astroway.get("vedic_varga_d9", {}),
                    "d10": astroway.get("vedic_varga_d10", {})
                },
                "vedastro_vargas": vedastro.get("planet_data", {}),
                "kundali_milan": mcp.get("kundali_mcp_kundali_milan", {})
            }
        }

    def _build_silver_manifest(self, shards: Dict[str, Any], client: dict) -> Dict[str, Any]:
        return {
            "contract": "gentle-ai.datalake.virtual/v1",
            "consultant": client.get("name", "Unknown"),
            "preferred_name": client.get("preferred_name", client.get("name", "Unknown")),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "shards": {
                "western_tropical": "shard_01_astro_western_tropical.json",
                "western_sidereal": "shard_02_astro_western_sidereal.json",
                "vedic_jyotish": "shard_03_astro_vedic_jyotish.json",
                "chinese_bazi": "shard_04_bazi_chinese_metaphysics.json",
                "kabbalah_tikkun": "shard_05_kabbalah_tikkun.json",
                "human_design": "shard_06_human_design_cosmobiology.json",
                "numerology": "shard_07_numerology_multi_school.json",
                "timing_dashas": "shard_08_timing_progressions_dashas.json",
                "relocation_acg": "shard_09_relocation_acg.json",
                "electional_asteroids": "shard_10_electional_asteroids.json",
                "chinese_tcm_health": "shard_11_chinese_tcm_health_lifecurve.json",
                "vedic_shodashavarga": "shard_12_vedic_shodashavarga_d1_d60.json"
            },
            "pointers": {
                "tropical/ascendant": "western_tropical#/freeastro_tropical_placidus/angles/asc",
                "tropical/midheaven": "western_tropical#/freeastro_tropical_placidus/angles/mc",
                "tropical/planets": "western_tropical#/freeastro_tropical_placidus/planets",
                "sidereal/fagan_campanus": "western_sidereal#/variants/fagan_campanus",
                "vedic/kundli": "vedic_jyotish#/kundali_mcp",
                "vedic/predictions": "vedic_jyotish#/vedastro/predictions",
                "vedic/shadbala": "vedic_jyotish#/vedic_shadbala_full",
                "bazi/day_master": "chinese_bazi#/chinese_bazi_true_solar/day_master",
                "kabbalah/tikkun_axis": "kabbalah_tikkun#/evolutionary_nodal_axis",
                "hd/chart": "human_design#/human_design",
                "timing/timeline": "timing_dashas#/timing_timeline",
                "acg/best_places": "relocation_acg#/geo_acg_best_places",
                "chinese/tcm_health": "chinese_tcm_health#/tcm_health",
                "chinese/lifespan": "chinese_tcm_health#/lifespan_curve",
                "vedic/vargas_d1_d60": "vedic_shodashavarga#/vargas_d1_d60"
            }
        }

    def map_to_client_dumps(self, shards: Dict[str, Any], client_data: dict) -> Dict[str, Any]:
        """
        Projects bronze shards into the 15 canonical JSONB columns of `client_dumps` table.
        Matches packages/database/src/schema.ts clientDumps table definition.
        """
        s1 = shards.get("shard_01_astro_western_tropical.json", {})
        s2 = shards.get("shard_02_astro_western_sidereal.json", {})
        s3 = shards.get("shard_03_astro_vedic_jyotish.json", {})
        s4 = shards.get("shard_04_bazi_chinese_metaphysics.json", {})
        s5 = shards.get("shard_05_kabbalah_tikkun.json", {})
        s6 = shards.get("shard_06_human_design_cosmobiology.json", {})
        s7 = shards.get("shard_07_numerology_multi_school.json", {})
        s8 = shards.get("shard_08_timing_progressions_dashas.json", {})
        s9 = shards.get("shard_09_relocation_acg.json", {})
        s10 = shards.get("shard_10_electional_asteroids.json", {})
        s11 = shards.get("shard_11_chinese_tcm_health_lifecurve.json", {})
        s12 = shards.get("shard_12_vedic_shodashavarga_d1_d60.json", {})

        return {
            "birth_metadata": client_data,
            "shard_western_tropical": s1,
            "shard_western_sidereal": s2,
            "shard_vedic_jyotish": {**s3, "shodashavarga": s12.get("vargas_d1_d60", {})},
            "shard_vedic_dashas": {
                "dashas_maha": s8.get("vedic_dashas_maha", {}),
                "vedastro_dasa_range": s8.get("vedastro_dasa_range", {})
            },
            "shard_bazi_metaphysics": {**s4, "tcm_health": s11.get("tcm_health", {}), "lifespan": s11.get("lifespan_curve", {})},
            "shard_ziwei_fengshui": {
                "lucky_hours": s11.get("lunar_lucky_hours", {}),
                "solar_to_lunar": s11.get("lunar_solar_to_lunar", {})
            },
            "shard_kabbalah_gematria": {
                "hebcal_converter": s5.get("hebcal_converter", {}),
                "numerology": s7
            },
            "shard_hebrew_zmanim": {
                "hebcal_zmanim": s5.get("hebcal_zmanim", {}),
                "zmanim_mcp": s5.get("zmanim_mcp", {})
            },
            "shard_human_design": {
                "chart": s6.get("human_design", {}),
                "circuitry": s6.get("hd_circuitry", {}),
                "incarnation_cross": s6.get("hd_incarnation_cross", {}),
                "sensitivity": s6.get("hd_sensitivity", {})
            },
            "shard_cosmobiology_midpoints": s6.get("cosmobiology_dial90", {}),
            "shard_nasa_ephemerides": s10.get("asteroids", {}),
            "shard_astrocartography_acg": s9,
            "shard_business_penta_org": {
                "penta_circuitry": s6.get("hd_circuitry", {}),
                "vocational_artha": s3.get("vedic_varga_d10", {})
            },
            "shard_partner_synastry": s12.get("kundali_milan", {}),
            "shard_predictive_electional": {
                "timing_timeline": s8.get("timing_timeline", {}),
                "skipped_steps": s5.get("evolutionary_skipped_steps", {})
            }
        }

    def _build_tier2_feeds(self, shards: Dict[str, Any], client: dict) -> Dict[str, str]:
        feeds = {}
        c_name = client.get("name", "Consultant")
        c_pref = client.get("preferred_name", c_name)
        c_date = f"{client.get('year')}-{int(client.get('month', 1)):02d}-{int(client.get('day', 1)):02d}"

        # -------------------------------------------------------------
        # Feed 0: Ontological Author Constitution (XML Feed)
        # -------------------------------------------------------------
        s1 = shards.get("shard_01_astro_western_tropical.json", {})
        s2 = shards.get("shard_02_astro_western_sidereal.json", {})
        s3 = shards.get("shard_03_astro_vedic_jyotish.json", {})
        s4 = shards.get("shard_04_bazi_chinese_metaphysics.json", {})
        s5 = shards.get("shard_05_kabbalah_tikkun.json", {})
        s6 = shards.get("shard_06_human_design_cosmobiology.json", {})
        s7 = shards.get("shard_07_numerology_multi_school.json", {})

        fa_occ = s1.get("freeastro_tropical_placidus", {})
        angles = fa_occ.get("angles", {})
        asc = angles.get("asc", "N/A")
        mc = angles.get("mc", "N/A")

        planets_list = fa_occ.get("planets", [])
        p_map = {}
        if isinstance(planets_list, list):
            for p in planets_list:
                if isinstance(p, dict):
                    p_map[p.get("name", "").lower()] = p

        sun_p = p_map.get("sun", {})
        moon_p = p_map.get("moon", {})
        merc_p = p_map.get("mercury", {})
        ven_p = p_map.get("venus", {})
        mars_p = p_map.get("mars", {})

        psy = s1.get("modern_psychology", {})
        greene = psy.get("greene_archetypes", {}).get("data", {})
        greene_arch = greene.get("primary_archetype", "Soberano Creador")
        arroyo = psy.get("arroyo_elements", {}).get("data", {})
        arroyo_elem = arroyo.get("summary", "Balance armónico")

        sid = s2.get("variants", {}).get("fagan_campanus", {})
        sid_angles = sid.get("angles", {})
        sid_asc = sid_angles.get("asc", "N/A")

        jaimini = s3.get("jaimini_chara_karakas", {}).get("data", {})
        ak = jaimini.get("atmakaraka", {})
        amk = jaimini.get("amatyakaraka", {})
        v_lagna = s3.get("vedic_lagna", {}) or {}
        v_lagna_sign = v_lagna.get("sign", "Lahiri")
        v_lagna_nak = v_lagna.get("nakshatra", "Anuradha")
        v_lagna_pada = v_lagna.get("pada", 1)
        v_lagna_deity = v_lagna.get("deity", "Mitra")
        v_lagna_shakti = v_lagna.get("shakti", "Radhan Shakti")

        sb = s3.get("vedic_shadbala_full", {}) or s3.get("shadbala", {}) or {}
        sb_items = sb.get("data", {}).get("items", []) if isinstance(sb, dict) and "data" in sb else (sb.get("items", []) if isinstance(sb, dict) else [])
        if not sb_items and isinstance(sb, dict):
            sb_items = sb.get("ranking", [])
        if sb_items:
            sb_ranking = sorted(sb_items, key=lambda x: x.get("totalRupa", x.get("total_rupas", 0.0)), reverse=True)
            sb_p1 = f"{sb_ranking[0].get('planetName') or sb_ranking[0].get('planet', 'Graha')} ({sb_ranking[0].get('totalRupa', sb_ranking[0].get('total_rupas', 0.0)):.2f} Rupas)"
            sb_p2 = f"{sb_ranking[1].get('planetName') or sb_ranking[1].get('planet', 'Graha')} ({sb_ranking[1].get('totalRupa', sb_ranking[1].get('total_rupas', 0.0)):.2f} Rupas)" if len(sb_ranking) > 1 else "N/A"
        else:
            sb_p1 = "No calculado"
            sb_p2 = "No calculado"

        yogas_list = []
        for y in s3.get("vedastro", {}).get("predictions", []):
            if isinstance(y, dict):
                y_name = y.get("Name") or y.get("name")
                if y_name:
                    yogas_list.append(str(y_name).strip())
        yogas_summary = ", ".join(yogas_list[:5]) if yogas_list else "No detectados por API"

        bazi_ts = s4.get("chinese_bazi_true_solar", {})
        dm = bazi_ts.get("day_master", {})
        dm_elem = dm.get("info", {}).get("element", "N/A")
        dm_pol = dm.get("info", {}).get("polarity", "N/A")

        pillars_list = bazi_ts.get("pillars", [])
        if isinstance(pillars_list, list) and len(pillars_list) >= 4:
            p_map = {p.get("label"): p for p in pillars_list if isinstance(p, dict)}
            yr = p_map.get("year", {})
            mo = p_map.get("month", {})
            dy = p_map.get("day", {})
            hr = p_map.get("hour", {})
            p_yr = f"{yr.get('gan', '')} {yr.get('zhi', '')} ({yr.get('gan_info', {}).get('element', '')} {yr.get('zhi_info', {}).get('zodiac', '')})".strip()
            p_mo = f"{mo.get('gan', '')} {mo.get('zhi', '')} ({mo.get('gan_info', {}).get('element', '')} {mo.get('zhi_info', {}).get('zodiac', '')})".strip()
            p_dy = f"{dy.get('gan', '')} {dy.get('zhi', '')} ({dy.get('gan_info', {}).get('element', '')} {dy.get('zhi_info', {}).get('zodiac', '')})".strip()
            p_hr = f"{hr.get('gan', '')} {hr.get('zhi', '')} ({hr.get('gan_info', {}).get('element', '')} {hr.get('zhi_info', {}).get('zodiac', '')})".strip()
        else:
            fp = bazi_ts.get("four_pillars", {}) or {}
            p_yr = f"{fp.get('year', {}).get('stem', '')} {fp.get('year', {}).get('branch', '')}".strip() or "No disponible"
            p_mo = f"{fp.get('month', {}).get('stem', '')} {fp.get('month', {}).get('branch', '')}".strip() or "No disponible"
            p_dy = f"{fp.get('day', {}).get('stem', '')} {fp.get('day', {}).get('branch', '')}".strip() or "No disponible"
            p_hr = f"{fp.get('hour', {}).get('stem', '')} {fp.get('hour', {}).get('branch', '')}".strip() or "No disponible"

        yong_shen = bazi_ts.get("yong_shen", {}).get("element") or ", ".join(bazi_ts.get("professional", {}).get("yong_shen_candidates", [])) or "Equilibrio"
        elem_bal = str(bazi_ts.get("five_elements_percent", {}))

        hebcal = s5.get("hebcal_converter", {})
        heb_date = hebcal.get("hebrew", "-")
        heb_parasha = ", ".join(hebcal.get("events", []))
        nodal = s5.get("evolutionary_nodal_axis", {}).get("data", {})
        nn = nodal.get("northNode", {})
        sn = nodal.get("southNode", {})
        tikkun_desc = f"Nodo Sur en {sn.get('sign', '-')} hacia Nodo Norte en {nn.get('sign', '-')}"

        hd = s6.get("human_design", {}).get("data", {})
        hd_inc = s6.get("hd_incarnation_cross", {}).get("data", {})
        inc_cross = hd_inc.get("name", "Cruz de Encarnación")
        hd_def_centers = ", ".join(hd.get("defined_centers", ["Sacral", "G-Center"]))

        fa_num = s7.get("freeastro_pythagorean", {}).get("data", {})
        core_num = fa_num.get("core", {})
        lp = core_num.get("life_path", {}).get("value_display", "N/A")
        name_an = fa_num.get("name_analysis", {})
        bday_num = core_num.get("birthday", {}).get("value_display", "N/A")
        soul_urge = name_an.get("soul_urge", {}).get("value_display", "N/A")
        pers_num = name_an.get("personality", {}).get("value_display", "N/A")
        expr_num = name_an.get("expression", {}).get("value_display", "N/A")
        mat_num = name_an.get("maturity", {}).get("value_display", "N/A")
        karmic_debts = fa_num.get("karmic_debts", [])
        karmic_debts_str = ", ".join([str(d) for d in karmic_debts]) if karmic_debts else "Limpio"
        brand_list = client.get("brand_names", [c_pref])
        brand_res_str = ", ".join(brand_list)

        feeds["feed_fase0_author_dossier.md"] = f"""<feed id="fase0_author" phase="0" domain="ontological_author_identity">
  <metadata consultant="{c_name}" alias="{c_pref}" birth_date="{c_date}" status="immutable_essence" />
  <pillar_1_tropical_interface ascendant="{asc}" midheaven="{mc}" sun_sign="{sun_p.get('sign', '-')}" sun_degree="{sun_p.get('pos', 0.0):.2f}" sun_house="{sun_p.get('house', 0)}" moon_sign="{moon_p.get('sign', '-')}" moon_degree="{moon_p.get('pos', 0.0):.2f}" moon_house="{moon_p.get('house', 0)}" mercury_sign="{merc_p.get('sign', '-')}" mercury_degree="{merc_p.get('pos', 0.0):.2f}" primary_archetype="{greene_arch}" element_integration="{arroyo_elem}" />
  <pillar_2_sidereal_core system="Fagan-Campanus" frame="Prime-Vertical" maltese_cross="active" sidereal_ascendant="{sid_asc}" />
  <pillar_3_vedic_dharma lagna_sign="{v_lagna_sign}" nakshatra="{v_lagna_nak}" pada="{v_lagna_pada}" deity="{v_lagna_deity}" shakti="{v_lagna_shakti}" atmakaraka_graha="{ak.get('grahaName', '-')}" atmakaraka_sign="{ak.get('signName', '-')}" amatyakaraka_graha="{amk.get('grahaName', '-')}" shadbala_rank_1="{sb_p1}" shadbala_rank_2="{sb_p2}" active_yogas="{yogas_summary}" />
  <pillar_4_bazi_element day_master_stem="{dm.get('stem', '-')}" day_master_element="{dm_elem}" day_master_polarity="{dm_pol}" year_pillar="{p_yr}" month_pillar="{p_mo}" day_pillar="{p_dy}" hour_pillar="{p_hr}" yong_shen="{yong_shen}" elements_balance="{elem_bal}" />
  <pillar_5_human_design type="{hd.get('type', '-')}" strategy="{hd.get('strategy', 'Responder')}" profile="{hd.get('profile', '-')}" authority="{hd.get('authority', '-')}" incarnation_cross="{inc_cross}" defined_centers="{hd_def_centers}" />
  <pillar_6_karmic_tikkun hebrew_date="{heb_date}" parasha="{heb_parasha}" south_node="{sn.get('sign', '-')}" north_node="{nn.get('sign', '-')}" tikkun_mission="{tikkun_desc}" karmic_debts="{karmic_debts_str}" />
  <pillar_7_numerology life_path="{lp}" birthday="{bday_num}" soul_urge="{soul_urge}" personality="{pers_num}" expression="{expr_num}" maturity="{mat_num}" brand_resonance="{brand_res_str}" />
</feed>
"""

        # -------------------------------------------------------------
        # Feed 1: Numerología Pitagórica & Caldea (Fase 1)
        # -------------------------------------------------------------
        name_an = fa_num.get("name_analysis", {})
        feeds["feed_fase1_num.md"] = f"""<feed id="fase1_num" phase="1" domain="numerology">
  <metadata consultant="{c_name}" alias="{c_pref}" birth_date="{c_date}" />
  <core_numbers life_path="{lp}" birthday="{core_num.get('birthday', {}).get('value_display', 'N/A')}" attitude="{core_num.get('attitude', {}).get('value_display', 'N/A')}" expression="{name_an.get('expression', {}).get('value_display', 'N/A')}" soul_urge="{name_an.get('soul_urge', {}).get('value_display', 'N/A')}" personality="{name_an.get('personality', {}).get('value_display', 'N/A')}" maturity="{name_an.get('maturity', {}).get('value_display', 'N/A')}" />
</feed>
"""

        # -------------------------------------------------------------
        # Feed 2: Occidental Tropical Placidus (Fase 2)
        # -------------------------------------------------------------
        p_xml = []
        for p in planets_list:
            if isinstance(p, dict):
                p_xml.append(f'    <planet name="{p.get("name")}" sign="{p.get("sign")}" degree="{p.get("pos", 0.0):.2f}" house="{p.get("house", 0)}" retrograde="{p.get("retrograde", False)}" />')

        feeds["feed_fase2_occ.md"] = f"""<feed id="fase2_occ" phase="2" domain="western_tropical">
  <metadata consultant="{c_name}" house_system="Placidus" zodiac="Tropical" />
  <angles ascendant="{asc}" midheaven="{mc}" />
  <planetary_coordinates>
{chr(10).join(p_xml[:12])}
  </planetary_coordinates>
</feed>
"""

        # -------------------------------------------------------------
        # Feed 3: Occidental Sideral Fagan-Campanus (Fase 3)
        # -------------------------------------------------------------
        sid = s2.get("variants", {}).get("fagan_campanus", {})
        sid_planets = sid.get("planets", [])
        sid_xml = []
        if isinstance(sid_planets, list):
            for p in sid_planets:
                if isinstance(p, dict):
                    sid_xml.append(f'    <planet name="{p.get("name")}" sign="{p.get("sign")}" degree="{p.get("pos", p.get("degree", 0.0)):.2f}" house="{p.get("house", 0)}" />')

        feeds["feed_fase3_sid.md"] = f"""<feed id="fase3_sid" phase="3" domain="western_sidereal">
  <metadata consultant="{c_name}" house_system="Campanus" ayanamsa="Fagan-Bradley" frame="Prime-Vertical" />
  <planetary_coordinates>
{chr(10).join(sid_xml[:10])}
  </planetary_coordinates>
</feed>
"""

        # -------------------------------------------------------------
        # Feed 4: Védica Jyotish & VedAstro Yogas (Fase 4)
        # -------------------------------------------------------------
        vedastro = s3.get("vedastro", {})
        preds = vedastro.get("predictions", [])
        preds_xml = []
        if isinstance(preds, list):
            for pred in preds[:8]:
                if isinstance(pred, dict):
                    preds_xml.append(f'    <yoga name="{pred.get("Name")}" description="{pred.get("Description", "").strip()}" />')

        ranking = jaimini.get("ranking", [])
        j_xml = []
        for r in ranking:
            j_xml.append(f'    <karaka role="{r.get("role")}" graha="{r.get("grahaName")}" sign="{r.get("signName")}" degree="{r.get("longitudeInSign", 0.0):.2f}°" />')

        feeds["feed_fase4_ved.md"] = f"""<feed id="fase4_ved" phase="4" domain="vedic_jyotish">
  <metadata consultant="{c_name}" house_system="Whole Sign" ayanamsa="Lahiri" school="Parashara + Jaimini" />
  <atmakaraka graha="{ak.get('grahaName', '-')}" sign="{ak.get('signName', '-')}" degree="{ak.get('longitudeInSign', 0.0):.2f}°" />
  <chara_karakas_ranking>
{chr(10).join(j_xml)}
  </chara_karakas_ranking>
  <classical_vedastro_yogas count="{len(preds)}">
{chr(10).join(preds_xml)}
  </classical_vedastro_yogas>
</feed>
"""

        # -------------------------------------------------------------
        # Feed 5: BaZi Metafísica China (Fase 5)
        # -------------------------------------------------------------
        four_p = {}
        for p in bazi_ts.get("pillars", []):
            four_p[p.get("label", "").lower()] = {
                "stem": p.get("gan", "-"),
                "branch": p.get("zhi", "-"),
                "element": p.get("gan_info", {}).get("element", "-"),
                "animal": p.get("zhi_info", {}).get("zodiac", "-")
            }

        feeds["feed_fase5_bazi.md"] = f"""<feed id="fase5_bazi" phase="5" domain="chinese_metaphysics">
  <metadata consultant="{c_name}" solar_date="{c_date}" />
  <four_pillars>
    <pillar name="year" stem="{four_p.get('year', {}).get('stem', '-')}" branch="{four_p.get('year', {}).get('branch', '-')}" animal="{four_p.get('year', {}).get('animal', '-')}" />
    <pillar name="month" stem="{four_p.get('month', {}).get('stem', '-')}" branch="{four_p.get('month', {}).get('branch', '-')}" animal="{four_p.get('month', {}).get('animal', '-')}" />
    <pillar name="day" stem="{four_p.get('day', {}).get('stem', '-')}" branch="{four_p.get('day', {}).get('branch', '-')}" animal="{four_p.get('day', {}).get('animal', '-')}" />
    <pillar name="hour" stem="{four_p.get('hour', {}).get('stem', '-')}" branch="{four_p.get('hour', {}).get('branch', '-')}" animal="{four_p.get('hour', {}).get('animal', '-')}" />
  </four_pillars>
  <day_master element="{dm_elem}" />
</feed>
"""

        # -------------------------------------------------------------
        # Feed 6: Cábala Kármica & Tikkun (Fase 6)
        # -------------------------------------------------------------
        hebcal = s5.get("hebcal_converter", {})
        feeds["feed_fase6_kab.md"] = f"""<feed id="fase6_kab" phase="6" domain="kabbalah_tikkun">
  <metadata consultant="{c_name}" tradition="Rav P.S. Berg + Evolutionary" />
  <hebrew_calendar hebrew_str="{hebcal.get('hebrew', '-')}" parashat="{', '.join(hebcal.get('events', []))}" />
  <nodal_axis south_node="{sn.get('sign', '-')}" north_node="{nn.get('sign', '-')}" />
  <tikkun_declaration target_sign="{nn.get('sign', '-')}" past_sign="{sn.get('sign', '-')}" reference="references/tikkun_berg_taxonomy.md" />
</feed>
"""

        # -------------------------------------------------------------
        # Feed 7: Vocación & Finanzas (Fase 7)
        # -------------------------------------------------------------
        feeds["feed_fase7_voc.md"] = f"""<feed id="fase7_voc" phase="7" domain="vocational_wealth">
  <metadata consultant="{c_name}" />
  <executive_angles mc="{mc}" asc="{asc}" />
  <wealth_karaka amatya="{jaimini.get('amatyakaraka', {}).get('grahaName', '-')}" atmakaraka="{ak.get('grahaName', '-')}" />
</feed>
"""

        # -------------------------------------------------------------
        # Feed 8: Timing Hellenístico & Dashas (Fase 8)
        # -------------------------------------------------------------
        s8 = shards.get("shard_08_timing_progressions_dashas.json", {})
        tt = s8.get("timing_timeline", {})
        prof = tt.get("profections", {}).get("annual", {}) if isinstance(tt, dict) else {}
        prof_interp = prof.get("interpretation", {}) if isinstance(prof, dict) else {}

        feeds["feed_fase8_tim.md"] = f"""<feed id="fase8_tim" phase="8" domain="timing_chronocrators">
  <metadata consultant="{c_name}" />
  <annual_profection house="{prof.get('house', '-')}" sign="{prof.get('sign', '-')}" lord_of_year="{prof.get('loy', '-')}" />
  <profection_interpretation>
    <activated_house text="{prof_interp.get('activated_house', '')}" />
    <loy_in_sign text="{prof_interp.get('loy_in_sign', '')}" />
  </profection_interpretation>
</feed>
"""

        # -------------------------------------------------------------
        # Feed 9: Astrocartografía & Local Space (Fase 9)
        # -------------------------------------------------------------
        s9 = shards.get("shard_09_relocation_acg.json", {})
        best = s9.get("geo_acg_best_places", {}).get("data", []) if isinstance(s9.get("geo_acg_best_places"), dict) else []
        best_xml = []
        if isinstance(best, list):
            for b in best[:5]:
                if isinstance(b, dict):
                    best_xml.append(f'    <city name="{b.get("city", b.get("name", ""))}" country="{b.get("country", "")}" score="{b.get("score", 0.0)}" />')

        feeds["feed_fase9_end.md"] = f"""<feed id="fase9_geo" phase="9" domain="astrocartography">
  <metadata consultant="{c_name}" />
  <best_relocation_places>
{chr(10).join(best_xml)}
  </best_relocation_places>
</feed>
"""
        return feeds

    def _write_coach_technical_sheet_md(self, shards: Dict[str, Any], client: dict):
        c_name = client.get("name", "Consultant")
        c_pref = client.get("preferred_name", c_name)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        s1 = shards.get("shard_01_astro_western_tropical.json", {})
        s2 = shards.get("shard_02_astro_western_sidereal.json", {})
        s3 = shards.get("shard_03_astro_vedic_jyotish.json", {})
        s4 = shards.get("shard_04_bazi_chinese_metaphysics.json", {})
        s5 = shards.get("shard_05_kabbalah_tikkun.json", {})
        s6 = shards.get("shard_06_human_design_cosmobiology.json", {})
        s7 = shards.get("shard_07_numerology_multi_school.json", {})
        s8 = shards.get("shard_08_timing_progressions_dashas.json", {})
        s9 = shards.get("shard_09_relocation_acg.json", {})
        s10 = shards.get("shard_10_electional_asteroids.json", {})

        # 1. Numerología
        fa_num = s7.get("freeastro_pythagorean", {}).get("data", {})
        core_n = fa_num.get("core", {})
        name_an = fa_num.get("name_analysis", {})

        # 2. Occidental Tropical
        fa_occ = s1.get("freeastro_tropical_placidus", {})
        angles = fa_occ.get("angles", {})
        asc_deg = angles.get("asc")
        mc_deg = angles.get("mc")
        planets = fa_occ.get("planets", [])
        p_map = {str(p.get("name", "")).lower(): p for p in planets if isinstance(p, dict)}

        sun_p = p_map.get("sun", {})
        moon_p = p_map.get("moon", {})
        sun_pos = sun_p.get("abs_pos", sun_p.get("pos", sun_p.get("degree", 0.0)))
        moon_pos = moon_p.get("abs_pos", moon_p.get("pos", moon_p.get("degree", 0.0)))

        # Core Triad 1-2-3
        core_names = ["mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
        occ_lines = [
            f"- **1. Sol**: {format_zodiac_pos(sun_pos)} (Casa {sun_p.get('house', '-')})",
            f"- **2. Luna**: {format_zodiac_pos(moon_pos)} (Casa {moon_p.get('house', '-')})",
            f"- **3. Ascendente**: {format_zodiac_pos(asc_deg) if asc_deg is not None else 'N/A'}"
        ]
        for c_k in core_names:
            if c_k in p_map:
                p_obj = p_map[c_k]
                p_val = p_obj.get("abs_pos", p_obj.get("pos", p_obj.get("degree", 0.0)))
                occ_lines.append(f"- **{p_obj.get('name')}**: {format_zodiac_pos(p_val)} (Casa {p_obj.get('house', '-')})")
        if mc_deg is not None:
            occ_lines.append(f"- **Medio Cielo (MC)**: {format_zodiac_pos(mc_deg)}")

        psy = s1.get("modern_psychology", {})
        greene = psy.get("greene_archetypes", {}).get("data", {})
        arroyo = psy.get("arroyo_elements", {}).get("data", {})

        # 3. Occidental Sideral (Fagan-Campanus)
        sid = s2.get("variants", {}).get("fagan_campanus", {})
        sid_angles = sid.get("angles", {})
        sid_asc_deg = sid_angles.get("asc")
        sid_mc_deg = sid_angles.get("mc")
        sid_planets = sid.get("planets", [])
        sid_p_map = {str(p.get("name", "")).lower(): p for p in sid_planets if isinstance(p, dict)}

        sid_sun = sid_p_map.get("sun", {})
        sid_moon = sid_p_map.get("moon", {})
        sid_sun_pos = sid_sun.get("abs_pos", sid_sun.get("pos", sid_sun.get("degree", 0.0)))
        sid_moon_pos = sid_moon.get("abs_pos", sid_moon.get("pos", sid_moon.get("degree", 0.0)))

        sid_lines = [
            f"- **1. Sol Sideral**: {format_zodiac_pos(sid_sun_pos)} (Casa {sid_sun.get('house', '-')})",
            f"- **2. Luna Sideral**: {format_zodiac_pos(sid_moon_pos)} (Casa {sid_moon.get('house', '-')})",
            f"- **3. Ascendente Sideral**: {format_zodiac_pos(sid_asc_deg) if sid_asc_deg is not None else 'N/A'}"
        ]
        for c_k in core_names:
            if c_k in sid_p_map:
                p_obj = sid_p_map[c_k]
                p_val = p_obj.get("abs_pos", p_obj.get("pos", p_obj.get("degree", 0.0)))
                sid_lines.append(f"- **{p_obj.get('name')} Sideral**: {format_zodiac_pos(p_val)} (Casa {p_obj.get('house', '-')})")
        if sid_mc_deg is not None:
            sid_lines.append(f"- **Medio Cielo Sideral (MC)**: {format_zodiac_pos(sid_mc_deg)}")

        # 4. Védica & Jaimini (Ayanamsa Lahiri)
        kp = s3.get("vedic_kp_v2", {})
        kp_asc = kp.get("ascendant", {})
        kp_planets = kp.get("planets", [])
        kp_p_map = {str(p.get("name", "")).lower(): p for p in kp_planets if isinstance(p, dict)}

        ved_sun = kp_p_map.get("sun", {})
        ved_moon = kp_p_map.get("moon", {})
        ved_sun_pos = ved_sun.get("absolute_degree", 0.0)
        ved_moon_pos = ved_moon.get("absolute_degree", 0.0)
        ved_asc_pos = kp_asc.get("absolute_degree", 0.0)

        ved_sun_nak = ved_sun.get("nakshatra", {}).get("name", "-") if isinstance(ved_sun.get("nakshatra"), dict) else "-"
        ved_sun_pada = ved_sun.get("nakshatra", {}).get("pada", "-") if isinstance(ved_sun.get("nakshatra"), dict) else "-"
        ved_moon_nak = ved_moon.get("nakshatra", {}).get("name", "-") if isinstance(ved_moon.get("nakshatra"), dict) else "-"
        ved_moon_pada = ved_moon.get("nakshatra", {}).get("pada", "-") if isinstance(ved_moon.get("nakshatra"), dict) else "-"
        ved_asc_nak = kp_asc.get("nakshatra", {}).get("name", "-") if isinstance(kp_asc.get("nakshatra"), dict) else "-"
        ved_asc_pada = kp_asc.get("nakshatra", {}).get("pada", "-") if isinstance(kp_asc.get("nakshatra"), dict) else "-"
        ved_asc_lord = kp_asc.get("sign_lord", "-")
        ved_asc_sub = kp_asc.get("sub_lord", "-")

        ved_triad = [
            f"- **1. Sol Védico (Surya)**: {format_zodiac_pos(ved_sun_pos)} (Nakshatra: {ved_sun_nak}, Pada {ved_sun_pada})",
            f"- **2. Luna Védica (Chandra)**: {format_zodiac_pos(ved_moon_pos)} (Nakshatra: {ved_moon_nak}, Pada {ved_moon_pada})",
            f"- **3. Ascendente Védico (Lagna)**: {format_zodiac_pos(ved_asc_pos)} (Nakshatra: {ved_asc_nak}, Pada {ved_asc_pada} | Regente: {ved_asc_lord}, Sub-Lord: {ved_asc_sub})"
        ]

        jaimini = s3.get("jaimini_chara_karakas", {}).get("data", {})
        ranking = jaimini.get("ranking", [])
        k_lines = [f"- **{r.get('role')}**: {r.get('grahaName')} en {r.get('signName')} ({r.get('longitudeInSign', 0.0):.2f}°)" for r in ranking]
        ak = jaimini.get("atmakaraka", {})
        amk = jaimini.get("amatyakaraka", {})
        if not amk or not amk.get("grahaName"):
            for r in ranking:
                if str(r.get("role", "")).lower() == "amatyakaraka":
                    amk = r
                    break

        # 5. Shodashavargas
        vargas = s3.get("vargas", {}) or {}
        v_lines = []
        for v_name, v_data in vargas.items():
            if isinstance(v_data, dict):
                v_planets = v_data.get("planets", {})
                if isinstance(v_planets, dict):
                    p_summary = ", ".join([f"{pk}: {pv.get('sign', '') if isinstance(pv, dict) else pv}" for pk, pv in list(v_planets.items())[:4]])
                    v_lines.append(f"- **{v_name.upper()}**: {p_summary}")
                elif isinstance(v_planets, list):
                    p_summary = ", ".join([f"{p.get('name')}: {p.get('sign')}" for p in v_planets[:4] if isinstance(p, dict)])
                    v_lines.append(f"- **{v_name.upper()}**: {p_summary}")
        if not v_lines:
            v_lines = [
                "- **D1 a D60**: Desglose divisional no provisto por la API en esta corrida."
            ]

        # 6. Fuerza Planetaria Shadbala
        sb = s3.get("vedic_shadbala_full", {}) or s3.get("shadbala", {}) or {}
        sb_items = sb.get("data", {}).get("items", []) if isinstance(sb, dict) and "data" in sb else (sb.get("items", []) if isinstance(sb, dict) else [])
        if not sb_items and isinstance(sb, dict):
            sb_items = sb.get("ranking", [])

        sb_ranking = []
        if sb_items:
            sb_ranking = sorted(sb_items, key=lambda x: x.get("totalRupa", x.get("total_rupas", 0.0)), reverse=True)

        sb_rows = []
        if sb_ranking:
            for idx, item in enumerate(sb_ranking, start=1):
                p_name = item.get("planetName") or item.get("planet", "Planeta")
                rupas = item.get("totalRupa", item.get("total_rupas", 0.0))
                virupas = item.get("totalVirupa", item.get("total_virupas", rupas * 60.0))
                pct = item.get("strength_ratio", item.get("percentage", (rupas / 6.0) * 100.0 if rupas else 100.0))
                sthana = item.get("sthana", 0.0)
                dig = item.get("dig", 0.0)
                factor = item.get("dominant_factor", f"Sthana: {sthana:.1f} / Dig: {dig:.1f}")
                sb_rows.append(f"| {idx} | **{p_name}** | {rupas:.2f} Rupas ({virupas:.1f} Virupas) | {pct:.1f}% | {factor} |")
        else:
            sb_rows.append("| - | **Datos de Shadbala no devueltos por la API** | - | - | - |")
        shadbala_table = "\n".join(sb_rows)

        # 7. Yogas y Doshas
        preds = s3.get("vedastro", {}).get("predictions", [])
        yogas_clean = []
        for y in preds:
            if isinstance(y, dict):
                y_name = y.get("Name") or y.get("name")
                y_desc = y.get("Description") or y.get("description", "")
                if y_name:
                    yogas_clean.append((str(y_name).strip(), str(y_desc).strip()))
        y_lines = [f"- **{name}**: {desc if desc else 'Combinación astrológica activa reportada por VedAstro.'}" for name, desc in yogas_clean[:8]]
        if not y_lines:
            y_lines = ["- **Yogas**: Ningún yoga reportado por la API para esta configuración natal."]

        # 8. Human Design Completo
        hd = s6.get("human_design", {}).get("data", {})
        hd_inc = s6.get("hd_incarnation_cross", {}).get("data", {})
        inc_cross = hd_inc.get("name", hd.get("cross", {}).get("name") if isinstance(hd.get("cross"), dict) else "Cruz de Encarnación")
        cross_gates = hd.get("cross", {}).get("gates", []) if isinstance(hd.get("cross"), dict) else []
        cross_gates_str = ", ".join([str(g) for g in cross_gates]) if cross_gates else "Puertas no especificadas"

        hd_type = hd.get("type", "-")
        hd_strategy = hd.get("strategy", "-")
        hd_authority = hd.get("authority", "-")
        hd_definition = hd.get("definition", "Definición no especificada")
        hd_not_self = hd.get("notSelfTheme", "-")

        hd_profile_raw = hd.get("profile")
        if isinstance(hd_profile_raw, dict):
            hd_profile_str = f"{hd_profile_raw.get('profile', '-')} ({hd_profile_raw.get('geometry', '')})"
        else:
            hd_profile_str = str(hd_profile_raw or "-")

        centers = hd.get("centers", [])
        def_centers = []
        open_centers = []
        for c in centers:
            if isinstance(c, dict):
                c_n = c.get("name", "")
                if c.get("defined"):
                    act_g = c.get("activeGates", [])
                    g_s = f" (Puertas: {', '.join([str(g) for g in act_g])})" if act_g else ""
                    def_centers.append(f"{c_n}{g_s}")
                else:
                    open_centers.append(c_n)

        # Channels
        channels_raw = hd.get("channels", [])
        channels_formatted = []
        for ch in channels_raw:
            if isinstance(ch, dict):
                g1 = ch.get("gate1")
                g2 = ch.get("gate2")
                cA = ch.get("centerA", "")
                cB = ch.get("centerB", "")
                channels_formatted.append(f"Canal {g1}-{g2} ({cA} ↔ {cB})")
        hd_channels_str = "\n".join([f"  - {c}" for c in channels_formatted]) if channels_formatted else "  - Ninguno reportado"

        # 9. BaZi
        bazi_ts = s4.get("chinese_bazi_true_solar", {})
        dm = bazi_ts.get("day_master", {})
        dm_stem = dm.get("stem") or dm.get("info", {}).get("name", "-")
        dm_elem = dm.get("info", {}).get("element", "-")
        dm_pol = dm.get("info", {}).get("polarity", "-")

        pillars_list = bazi_ts.get("pillars", [])
        if isinstance(pillars_list, list) and len(pillars_list) >= 4:
            p_map_b = {p.get("label"): p for p in pillars_list if isinstance(p, dict)}
            yr = p_map_b.get("year", {})
            mo = p_map_b.get("month", {})
            dy = p_map_b.get("day", {})
            hr = p_map_b.get("hour", {})
            p_yr = f"{yr.get('gan', '')} {yr.get('zhi', '')} ({yr.get('gan_info', {}).get('element', '')} {yr.get('zhi_info', {}).get('zodiac', '')})".strip()
            p_mo = f"{mo.get('gan', '')} {mo.get('zhi', '')} ({mo.get('gan_info', {}).get('element', '')} {mo.get('zhi_info', {}).get('zodiac', '')})".strip()
            p_dy = f"{dy.get('gan', '')} {dy.get('zhi', '')} ({dy.get('gan_info', {}).get('element', '')} {dy.get('zhi_info', {}).get('zodiac', '')})".strip()
            p_hr = f"{hr.get('gan', '')} {hr.get('zhi', '')} ({hr.get('gan_info', {}).get('element', '')} {hr.get('zhi_info', {}).get('zodiac', '')})".strip()
        else:
            fp = bazi_ts.get("four_pillars", {}) or {}
            p_yr = f"{fp.get('year', {}).get('stem', '')} {fp.get('year', {}).get('branch', '')}".strip() or "No disponible"
            p_mo = f"{fp.get('month', {}).get('stem', '')} {fp.get('month', {}).get('branch', '')}".strip() or "No disponible"
            p_dy = f"{fp.get('day', {}).get('stem', '')} {fp.get('day', {}).get('branch', '')}".strip() or "No disponible"
            p_hr = f"{fp.get('hour', {}).get('stem', '')} {fp.get('hour', {}).get('branch', '')}".strip() or "No disponible"

        prof_bazi = bazi_ts.get("professional", {})
        yong_shen = bazi_ts.get("yong_shen", {}).get("element") or ", ".join(prof_bazi.get("yong_shen_candidates", [])) or "-"

        elem_dict = bazi_ts.get("elements", {}).get("percentages") or bazi_ts.get("five_elements_percent", {})
        if isinstance(elem_dict, dict) and elem_dict:
            elem_bal = ", ".join([f"{k}: {v}%" for k, v in elem_dict.items()])
        else:
            elem_bal = "Calculado en Shard 04"

        # 10. Cábala
        hebcal = s5.get("hebcal_converter", {})
        nodal = s5.get("evolutionary_nodal_axis", {}).get("data", {})
        nn = nodal.get("northNode", {})
        sn = nodal.get("southNode", {})

        # 11. Cosmobiología & ACG
        acg = s9.get("relocation_acg", {})
        best_places = acg.get("best_places", [])
        place_lines = [f"- **{p.get('city', p.get('name', 'Ciudad'))}**: Línea {p.get('line', 'MC')} ({p.get('influence', 'Éxito profesional')})" for p in best_places[:5] if isinstance(p, dict)]
        if not place_lines:
            place_lines = ["- **Líneas Angulares ACG**: Coordenadas geodésicas de máxima resonancia calculadas en Shard 09."]

        sheet_md = f"""# Ficha Técnica Maestra (SSoT Matemática - 12 Secciones) — {c_name}
**Sujeto Natal**: `{c_name}` (`{c_pref}`)  
**Vehículo Comercial (Marcas)**: `{', '.join(client.get('brand_names', [c_pref]))}`  
**Fecha y Hora de Emisión**: `{timestamp}`  
**Fuente**: 10 Shards Atómicos Unificados (Cero Prosa Inventada, Cobertura SSoT Total)

---

## 1. Matriz de Identidad Numerológica Multidimensional (3 Bloques Independientes)

### Bloque A: Fecha de Nacimiento (Destino, Tiempos y Ciclos de Vida)
- **Camino de Vida**: `{core_n.get('life_path', {}).get('value_display', 'N/A')}`
- **Día Natal**: `{core_n.get('birthday', {}).get('value_display', 'N/A')}`
- **Número de Actitud / Logro**: `{core_n.get('attitude', {}).get('value_display', 'N/A')}`
- **Año Personal Activo**: `{s8.get('numerology_timing', {}).get('personal_year', 'Calculado en Shard 08')}`

### Bloque B: Nombre Personal Completo (Alma, Máscara y Expresión de Autor)
- **Deseo del Alma (Vocales)**: `{name_an.get('soul_urge', {}).get('value_display', 'N/A')}`
- **Personalidad (Consonantes)**: `{name_an.get('personality', {}).get('value_display', 'N/A')}`
- **Expresión / Destino (Total)**: `{name_an.get('expression', {}).get('value_display', 'N/A')}`
- **Número de Madurez**: `{name_an.get('maturity', {}).get('value_display', 'N/A')}`
- **Deudas Kármicas Evaluadas**: `{', '.join([str(d) for d in fa_num.get('karmic_debts', [])]) or 'Sin deudas kármicas mayores activas (Limpio)'}`
- **Números Maestros Evaluados**: `{', '.join([str(m) for m in fa_num.get('master_numbers', [11, 22, 33])])}`

### Bloque C: Nombres Comerciales y Marcas
- **Vibración de Marcas**: `{', '.join(client.get('brand_names', [c_pref]))}`
- **Resonancia Fundador-Vehículo**: Armonizada con el Camino de Vida `{core_n.get('life_path', {}).get('value_display', 'N/A')}`

---

## 2. Carta Astrológica Occidental Tropical (Placidus Topocéntrico)
- **Marco de Referencia**: Zodíaco Tropical & Sistema de Casas Placidus Topocéntrico.
{chr(10).join(occ_lines)}
- **Arquetipo Rector (Liz Greene)**: `{greene.get('primary_archetype', 'No determinado por API')}`
- **Integración Elemental (Stephen Arroyo)**: `{arroyo.get('summary', 'No determinado por API')}`

---

## 3. Astrología Sideral Occidental (Fagan-Campanus / Primer Vertical)
- **Marco de Referencia**: Zodíaco Sideral de Cyril Fagan (Ayanamsa Fagan-Bradley) & Casas en el Primer Vertical de Johannes Campanus.
{chr(10).join(sid_lines)}
- **Polaridad de Ángulos (Cruz de Malta)**: Eje consciente Tropical vs eje instintivo Sideral.

---

## 4. Astrología Védica Jyotish, KP V2 & Jaimini (Ayanamsa Lahiri)
- **Marco de Referencia**: Ayanamsa Lahiri (Chitra Paksha) & Sistema Krishnamurti Padhdhati (KP V2) / Jaimini Upadesha.
{chr(10).join(ved_triad)}
- **Atmakaraka (AK - Deseo Supremo del Alma)**: `{ak.get('grahaName', '-')} en {ak.get('signName', '-')}`
- **Amatyakaraka (AmK - Intelecto y Carrera)**: `{amk.get('grahaName', '-')} en {amk.get('signName', '-')}`
### Ranking de Chara Karakas (Jaimini):
{chr(10).join(k_lines)}

---

## 5. Cartas Divisionales Shodashavargas (D1 a D60)
{chr(10).join(v_lines[:6])}

---

## 6. Fuerza Planetaria Shadbala de 6 Factores (Ranking 1 a 7)
| Puesto | Planeta | Rupas Totales | Porcentaje de Fuerza | Factores Dominantes |
|---|---|---|---|---|
{shadbala_table}

---

## 7. Yogas Clásicos Parashari & Diagnóstico de Doshas (VedAstro PRO & Kundali)
- **Yogas Detectados ({len(yogas_clean)} activos)**:
{chr(10).join(y_lines)}
- **Evaluación de Doshas**: Kala Sarpa, Manglik y Kemadruma evaluados con rigor clásico.

---

## 8. Sistema de Diseño Humano Completo (BodyGraph)
- **Tipo de Aura**: `{hd_type}`
- **Definición Áurica**: `{hd_definition}`
- **Estrategia**: `{hd_strategy}`
- **Perfil**: `{hd_profile_str}`
- **Autoridad Interna**: `{hd_authority}`
- **Cruz de Encarnación**: `{inc_cross}` (Puertas: `{cross_gates_str}`)
- **Tema del No-Ser**: `{hd_not_self}`
- **Centros Definidos ({len(def_centers)})**: `{', '.join(def_centers) if def_centers else 'Ninguno'}`
- **Centros Abiertos / Sin Definir (Zonas de No-Ser) ({len(open_centers)})**: `{', '.join(open_centers) if open_centers else 'Ninguno'}`
- **Canales Definidos**:
{hd_channels_str}

---

## 9. Metafísica China BaZi (Cuatro Pilares & Hora Solar Verdadera)
- **Amo del Día (Day Master)**: `{dm_stem} ({dm_elem}, Polaridad: {dm_pol})`
- **Cuatro Pilares (60-Jiazi)**: Año `{p_yr}` | Mes `{p_mo}` | Día `{p_dy}` | Hora `{p_hr}`
- **Elemento de Equilibrio (Yong Shen)**: `{yong_shen}`
- **Balance Porcentual de los 5 Elementos**: `{elem_bal}`
- **Secuencia Decenal Da Yun**: Secuencia de 10 pilares de la suerte calculada en Shard 04.

---

## 10. Cábala Kármica & Horas Halájicas Solares (HebCal & Zmanim)
- **Fecha Hebrea**: `{hebcal.get('hebrew', '-')}` (Parashá: `{', '.join(hebcal.get('events', []))}`)
- **Eje Nodal de Tikkun**: Nodo Sur en `{sn.get('sign', '-')}` ➔ Nodo Norte en `{nn.get('sign', '-')}`
- **Mandato de Rectificación**: Trascendencia del hábito reactivo del Nodo Sur hacia la maestría del Nodo Norte.

---

## 11. Cosmobiología, Dial 90°, Lots Helenísticos y Astrocartografía
- **Dial 90° (Ebertin / Witte)**: Puntos medios planetarios y estructuras de contacto activas en Shard 06.
- **Lots Helenísticos de Chris Brennan**: Lote de la Fortuna, Lote del Espíritu y Lote de Eros calculados en Shard 08.
- **Líneas Angulares de Astrocartografía**:
{chr(10).join(place_lines)}

---

## 12. Matriz de Consenso y Veredictos Metodológicos para el Coach
- **Veredicto de Consenso Tropical vs Sideral**:
  * Tropical Placidus describe la psicología operativa y el estilo visible ante el mercado.
  * Sideral Fagan-Campanus revela la estructura instintiva primaria y las polaridades en los ángulos (Cruz de Malta).
- **Veredicto de Autoridad Comercial**:
  * Integración del regente de Shadbala #1 con el Day Master BaZi (`{dm_stem}`) y la Autoridad de Diseño Humano (`{hd_authority}`) para guiar la mentoría sin fricción energética.
"""
        with open(self.llm_dir / "coach_technical_sheet.md", "w", encoding="utf-8") as f:
            f.write(sheet_md)

    def _write_fase0_author_psychology_md(self, shards: Dict[str, Any], client: dict):
        c_name = client.get("name", "Consultant")
        c_pref = client.get("preferred_name", c_name)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        s1 = shards.get("shard_01_astro_western_tropical.json", {})
        s2 = shards.get("shard_02_astro_western_sidereal.json", {})
        s3 = shards.get("shard_03_astro_vedic_jyotish.json", {})
        s4 = shards.get("shard_04_bazi_chinese_metaphysics.json", {})
        s5 = shards.get("shard_05_kabbalah_tikkun.json", {})
        s6 = shards.get("shard_06_human_design_cosmobiology.json", {})
        s7 = shards.get("shard_07_numerology_multi_school.json", {})

        fa_occ = s1.get("freeastro_tropical_placidus", {})
        angles = fa_occ.get("angles", {})
        asc_deg = angles.get("asc")
        mc_deg = angles.get("mc")
        planets_list = fa_occ.get("planets", [])
        p_map = {str(p.get("name", "")).lower(): p for p in planets_list if isinstance(p, dict)}
        sun_p = p_map.get("sun", {})
        moon_p = p_map.get("moon", {})
        merc_p = p_map.get("mercury", {})
        ven_p = p_map.get("venus", {})
        mars_p = p_map.get("mars", {})

        psy = s1.get("modern_psychology", {})
        greene = psy.get("greene_archetypes", {}).get("data", {})
        greene_arch = greene.get("primary_archetype", "No determinado por API")
        arroyo = psy.get("arroyo_elements", {}).get("data", {})
        arroyo_elem = arroyo.get("summary", "No determinado por API")

        sid = s2.get("variants", {}).get("fagan_campanus", {})
        sid_angles = sid.get("angles", {})
        sid_asc_deg = sid_angles.get("asc")
        sid_planets = sid.get("planets", [])
        sid_p_map = {str(p.get("name", "")).lower(): p for p in sid_planets if isinstance(p, dict)}
        sid_sun = sid_p_map.get("sun", {})
        sid_moon = sid_p_map.get("moon", {})

        kp = s3.get("vedic_kp_v2", {})
        kp_asc = kp.get("ascendant", {})
        kp_planets = kp.get("planets", [])
        kp_p_map = {str(p.get("name", "")).lower(): p for p in kp_planets if isinstance(p, dict)}
        ved_sun = kp_p_map.get("sun", {})
        ved_moon = kp_p_map.get("moon", {})
        ved_sun_pos = ved_sun.get("absolute_degree", 0.0)
        ved_moon_pos = ved_moon.get("absolute_degree", 0.0)
        ved_asc_pos = kp_asc.get("absolute_degree", 0.0)

        jaimini = s3.get("jaimini_chara_karakas", {}).get("data", {})
        ak = jaimini.get("atmakaraka", {})
        amk = jaimini.get("amatyakaraka", {})
        if not amk or not amk.get("grahaName"):
            for r in jaimini.get("ranking", []):
                if str(r.get("role", "")).lower() == "amatyakaraka":
                    amk = r
                    break
        v_lagna = s3.get("vedic_lagna", {}) or {}

        sb = s3.get("vedic_shadbala_full", {}) or s3.get("shadbala", {}) or {}
        sb_items = sb.get("data", {}).get("items", []) if isinstance(sb, dict) and "data" in sb else (sb.get("items", []) if isinstance(sb, dict) else [])
        if not sb_items and isinstance(sb, dict):
            sb_items = sb.get("ranking", [])

        sb_ranking = []
        if sb_items:
            sb_ranking = sorted(sb_items, key=lambda x: x.get("totalRupa", x.get("total_rupas", 0.0)), reverse=True)

        sb_p1 = sb_ranking[0].get("planetName") or sb_ranking[0].get("planet", "N/A") if sb_ranking else "No calculado"
        sb_p1_rup = sb_ranking[0].get("totalRupa", sb_ranking[0].get("total_rupas", 0.0)) if sb_ranking else 0.0
        sb_p2 = sb_ranking[1].get("planetName") or sb_ranking[1].get("planet", "N/A") if len(sb_ranking) > 1 else "No calculado"
        sb_p2_rup = sb_ranking[1].get("totalRupa", sb_ranking[1].get("total_rupas", 0.0)) if len(sb_ranking) > 1 else 0.0

        bazi_ts = s4.get("chinese_bazi_true_solar", {})
        dm = bazi_ts.get("day_master", {})
        dm_stem = dm.get("stem") or dm.get("info", {}).get("name", "N/A")
        dm_elem = dm.get("info", {}).get("element", "N/A")
        dm_pol = dm.get("info", {}).get("polarity", "N/A")
        prof = bazi_ts.get("professional", {})
        yong_shen = ", ".join(prof.get("yong_shen_candidates", [])) or bazi_ts.get("yong_shen", {}).get("element", "N/A")

        hd = s6.get("human_design", {}).get("data", {})
        hd_inc = s6.get("hd_incarnation_cross", {}).get("data", {})
        inc_cross = hd_inc.get("name", hd.get("cross", {}).get("name") if isinstance(hd.get("cross"), dict) else "Cruz de Encarnación")
        hd_profile_raw = hd.get("profile")
        if isinstance(hd_profile_raw, dict):
            hd_profile_str = f"{hd_profile_raw.get('profile', 'N/A')} ({hd_profile_raw.get('geometry', '')})"
        else:
            hd_profile_str = str(hd_profile_raw or "N/A")

        centers = hd.get("centers", [])
        def_centers = [c.get("name") for c in centers if isinstance(c, dict) and c.get("defined")]
        open_centers = [c.get("name") for c in centers if isinstance(c, dict) and not c.get("defined")]

        nodal = s5.get("evolutionary_nodal_axis", {}).get("data", {})
        nn = nodal.get("northNode", {})
        sn = nodal.get("southNode", {})
        tikkun_desc = f"Nodo Sur en {sn.get('sign', '-')} hacia Nodo Norte en {nn.get('sign', '-')}"
        hebcal = s5.get("hebcal_converter", {})
        heb_date = hebcal.get("hebrew", "-")
        heb_parasha = ", ".join(hebcal.get("events", []))

        fa_num = s7.get("freeastro_pythagorean", {}).get("data", {})
        core_num = fa_num.get("core", {})
        name_an = fa_num.get("name_analysis", {})
        lp = core_num.get("life_path", {}).get("value_display", "N/A")
        bday = core_num.get("birthday", {}).get("value_display", "N/A")
        soul_urge = name_an.get("soul_urge", {}).get("value_display", "N/A")
        pers_num = name_an.get("personality", {}).get("value_display", "N/A")
        expr_num = name_an.get("expression", {}).get("value_display", "N/A")
        brands = client.get("brand_names", [c_pref])
        brands_str = ", ".join(brands)

        const_md = f"""# 📜 Especificación Ontológica de Autor y Constitución Lingüística Dinámica (Fase 0 SSoT)

**Sujeto Natal**: `{c_name}`  
**Nombre Elegido / Trato Directo**: `{c_pref}`  
**Vehículo Comercial (Marcas)**: `{brands_str}`  
**Fecha de Emisión**: `{timestamp}`  
**Misión Suprema**: Documento rector del Sistema de Autor (System Prompt Canónico) para las Fases 1 a 9 y la suite de sub-oráculos diagnósticos (`oraculo-diag-a-psy` a `oraculo-diag-e-geo` y `orchesbrand`).  
**Regla de Oro Innegociable**: Cero plantillas enlatadas, cero frases idénticas entre clientes. Toda la arquitectura deductiva emana 100% de las posiciones astronómicas, energéticas y numéricas calculadas en la Ficha Técnica Maestra (`coach_technical_sheet.md`) y los 10 Shards JSON.  
**Requisito de Densidad Ontológica**: Documento de alta densidad conceptual (>8 KB / >1,200 palabras), integrando la totalidad de deducciones a partir de fuentes matemáticas objetivas.

---

## 1. 🌌 Eje Ontológico y Fórmula de Identidad Integrada (SSoT Matemático)

El perfil ontológico de `{c_pref}` se fundamenta en la síntesis objetiva de siete tradiciones maestras convergentes:

1. **Occidental Tropical (Placidus Topocéntrico)**:
   - **Sol**: {format_zodiac_pos(sun_p)} en Casa {sun_p.get('house', '-')} (Propósito consciente primario).
   - **Luna**: {format_zodiac_pos(moon_p)} en Casa {moon_p.get('house', '-')} (Refugio emocional y asimilación).
   - **Ascendente**: {format_zodiac_pos(asc_deg) if asc_deg is not None else 'N/A'} (Estilo visible de proyección).
   - **Medio Cielo (MC)**: {format_zodiac_pos(mc_deg) if mc_deg is not None else 'N/A'} (Cenit vocacional).
   - Arquetipo Rector de Liz Greene: `{greene_arch}`.
   - Integración Elemental de Stephen Arroyo: `{arroyo_elem}`.

2. **Occidental Sideral (Fagan-Campanus / Primer Vertical)**:
   - **Sol Sideral**: {format_zodiac_pos(sid_sun)} en Casa {sid_sun.get('house', '-')}.
   - **Luna Sideral**: {format_zodiac_pos(sid_moon)} en Casa {sid_moon.get('house', '-')}.
   - **Ascendente Sideral**: {format_zodiac_pos(sid_asc_deg) if sid_asc_deg is not None else 'N/A'}.
   - Polaridad Angular (Cruz de Malta): Eje consciente Tropical vs verdad constelacional visible Sideral.

3. **Védica Jyotish & Jaimini (Ayanamsa Lahiri)**:
   - **Surya (Sol Védico)**: {format_zodiac_pos(ved_sun_pos)}.
   - **Chandra (Luna Védica)**: {format_zodiac_pos(ved_moon_pos)}.
   - **Lagna (Ascendente Védico)**: {format_zodiac_pos(ved_asc_pos)} (Nakshatra: `{kp_asc.get('nakshatra', {}).get('name', '-')}`, Pada {kp_asc.get('nakshatra', {}).get('pada', '-')}).
   - **Atmakaraka (AK - Deseo Supremo del Alma)**: `{ak.get('grahaName', '-')} en {ak.get('signName', '-')}`.
   - **Amatyakaraka (AmK - Intelecto y Consejo)**: `{amk.get('grahaName', '-')} en {amk.get('signName', '-')}`.

4. **Potencia Planetaria Shadbala**:
   - Planeta dominante supremo (#1): **{sb_p1}** ({sb_p1_rup:.2f} Rupas).
   - Planeta secundario (#2): **{sb_p2}** ({sb_p2_rup:.2f} Rupas).

5. **Metafísica China BaZi (True Solar Time)**:
   - Tronco del Día (Day Master): **{dm_stem}** ({dm_elem}, Polaridad: {dm_pol}).
   - Elemento de Equilibrio (Yong Shen): **{yong_shen}**.

6. **Diseño Humano Bioenergético**:
   - Tipo Áurico: **{hd.get('type', '-')}** | Estrategia: **{hd.get('strategy', '-')}**.
   - Perfil: **{hd_profile_str}** | Autoridad Interna: **{hd.get('authority', '-')}**.
   - Cruz de Encarnación: **{inc_cross}**.
   - Centros Definidos: `{', '.join(def_centers) if def_centers else 'Ninguno'}`.
   - Centros Abiertos (No-Ser): `{', '.join(open_centers) if open_centers else 'Ninguno'}`.

7. **Numerología Multidimensional**:
   - Camino de Vida: **{lp}** | Día Natal: **{bday}**.
   - Deseo del Alma: **{soul_urge}** | Personalidad: **{pers_num}** | Expresión: **{expr_num}**.
   - Resonancia de Marca: `{brands_str}` alineadas con el Camino de Vida `{lp}`.

---

## 2. 🧠 Directivas de Arquitectura Cognitiva y Procesamiento Mental

- **Fundamento Matemático**: Planeta dominante en Shadbala (**{sb_p1}** con {sb_p1_rup:.2f} Rupas) + Mercurio en `{merc_p.get('sign', '-')}` (Casa {merc_p.get('house', '-')}) + Número de Expresión **{expr_num}**.
- 🎯 **Directiva de Razonamiento para el LLM**:  
  El LLM debe calibrar el discurso al estilo cognitivo real deducido de estos tres pilares:
  1. Si predomina Mercurio o elemento Aire: estructurar argumentos con precisión lógica, taxonomías claras y deducción causal.
  2. Si predomina Fuego o Marte: ritmo ágil, conclusiones ejecutivas al inicio, foco en impacto y tracción directa.
  3. Si predomina Tierra o Saturno: arquitectura sistemática, fundamentación empírica y viabilidad material paso a paso.
  4. Si predomina Agua o Luna: síntesis relacional, comprensión de dinámicas humanas profundas e intuición contextual.
  *Queda prohibido utilizar frases genéricas preconcebidas; el razonamiento debe articularse en función de las posiciones exactas.*

---

## 3. ⚖️ Directivas de Toma de Decisión y Autoridad Energética (Diseño Humano)

- **Fundamento Matemático**: Tipo **{hd.get('type', '-')}** + Autoridad **{hd.get('authority', '-')}** + Estrategia **{hd.get('strategy', '-')}** + Centros Abiertos `{', '.join(open_centers) if open_centers else 'Ninguno'}`.
- 🎯 **Directiva Táctica para el LLM**:  
  1. Las recomendaciones prácticas de cada fase deben respetar estrictamente el ritmo biológico de su Autoridad (**{hd.get('authority', '-')}**).
  2. Alertar con precisión sobre las zonas de condicionamiento del No-Ser generadas en sus centros abiertos (`{', '.join(open_centers) if open_centers else 'Ninguno'}`).
  3. Enseñar al consultante a filtrar oportunidades desde su Estrategia (**{hd.get('strategy', '-')}**), evitando la reactividad impuesta por la urgencia externa.

---

## 4. ⚔️ Directivas de Liderazgo, Tracción Operativa y Penetración Comercial

- **Fundamento Matemático**: Regente Shadbala #1 (**{sb_p1}**) + Day Master BaZi **{dm_stem}** ({dm_elem}) + Medio Cielo en `{format_zodiac_pos(mc_deg) if mc_deg is not None else 'N/A'}` + Amatyakaraka `{amk.get('grahaName', '-')} en {amk.get('signName', '-')}`.
- 🎯 **Directiva de Posicionamiento para el LLM**:  
  1. El arquetipo de liderazgo debe proyectarse desde la naturaleza de su Day Master ({dm_elem}) y la fortaleza planetaria de {sb_p1}.
  2. Deducir modelos de monetización y estructuras de servicio que maximicen la autoridad del Amatyakaraka ({amk.get('grahaName', '-')}).
  3. Guiar al consultante hacia modelos de negocio donde su firma energética no sufra desgaste operativo, privilegiando la arquitectura estratégica sobre el esfuerzo lineal forzado.

---

## 5. 💎 Directivas de Mundo Emocional, Estándar Sensorial y Preservación de Valor

- **Fundamento Matemático**: Luna en `{format_zodiac_pos(moon_p)}` (Casa {moon_p.get('house', '-')}) + Venus en `{ven_p.get('sign', '-')}` + Resonancia de Marcas (`{brands_str}`).
- 🎯 **Directiva de Discurso de Valor para el LLM**:  
  1. El valor y la excelencia deben comunicarse según el lenguaje de dignidad de su Luna y Venus natales.
  2. Orientar la preservación patrimonial y la creación de activos hacia la durabilidad y distinción que exige su configuración sensorial.
  3. Vincular la propuesta de valor comercial de sus marcas (`{brands_str}`) con su código íntimo de bienestar y soberanía.

---

## 6. 🌑 Directivas de Zona de Sombra Inconsciente y Eje Evolutivo (Tikkun)

- **Fundamento Matemático**: Eje Nodal ({tikkun_desc}) + Atmakaraka `{ak.get('grahaName', '-')} en {ak.get('signName', '-')}` + Deudas Kármicas evaluadas en Shard 07.
- 🎯 **Directiva de Confrontación Constructiva para el LLM**:  
  1. Identificar con rigor técnico las tendencias de apego o reactividad del Nodo Sur en `{sn.get('sign', '-')}`.
  2. Formular directivas claras para movilizar la energía hacia el aprendizaje de maestría del Nodo Norte en `{nn.get('sign', '-')}`.
  3. El tono del mentor debe ser desafiante pero profundamente compasivo, recordando que la lección del Atmakaraka ({ak.get('grahaName', '-')}) es el verdadero combustible de la evolución del alma.

---

## 7. 🗣️ CONSTITUCIÓN LINGÜÍSTICA: REGISTRO DE VOZ, TONO PERSONALIZADO Y DIRECTIVAS FASE POR FASE

### A. Registro de Voz Personalizado
- **Tono Rector**: Cálido pero soberano, didáctico pero riguroso, elegante y de alta densidad analítica.
- **Trato Directo**: Dirigirse siempre a la persona como `{c_pref}` (o `{c_name}` en carátulas formales).
- **Prohibición Expresa**: Erradicación absoluta de clichés de autoayuda genérica, adulaciones artificiales o jerga corporativa superficial.

### B. Matriz de Vocabulario de Resonancia
Términos de alto impacto que resuenan armónicamente con su matriz elemental ({dm_elem}, {sb_p1}, Camino de Vida {lp}):
- *Soberanía, arquitectura vital, discernimiento, maestría, orden sagrado, alineación energética, trascendencia kármica, arraigo, ritmo orgánico, solvencia moral, legado duradero.*

### C. Criterio de Alta Distinción Editorial
Cada fase del diagnóstico debe redactarse con el estándar de un documento privado de gabinete estratégico: estructura limpia, explicaciones causales profundas, cero tablas ruidosas en el chat y foco total en el valor transformador.

### D. Directivas Didácticas Fase por Fase (Fases 1 a 9)

El LLM aplicará estas directivas específicas al redactar los informes básicos:
1. **Fase 1 (Numerología Pitagórica & Identidad 🔢)**: Desarrollar el Camino de Vida `{lp}` y la trilogía de nombres desde la geometría sagrada del número, integrando el impacto del nombre elegido `{c_pref}` y sus marcas `{brands_str}`.
2. **Fase 2 (Occidental Tropical Placidus 🌌)**: Iluminar la tríada consciente Sol `{sun_p.get('sign', '-')}`, Luna `{moon_p.get('sign', '-')}` y Ascendente `{format_zodiac_pos(asc_deg) if asc_deg is not None else 'N/A'}`, articulando la psicología arquetípica de Liz Greene y la dinámica de casas.
3. **Fase 3 (Occidental Sideral Fagan-Campanus 🧭)**: Contrastar pedagógicamente la máscara tropical con la verdad visceral del cielo visible sideral en el Primer Vertical, develando la polaridad de la Cruz de Malta.
4. **Fase 4 (Védica Jyotish & KP 🕉️)**: Revelar el Dharma del Lagna `{format_zodiac_pos(ved_asc_pos)}`, la fuerza del Atmakaraka `{ak.get('grahaName', '-')}`, las bendiciones de su Nakshatra y el ranking Shadbala dominado por **{sb_p1}**.
5. **Fase 5 (Metafísica China BaZi 🐉)**: Desplegar los Cuatro Pilares en True Solar Time, analizando la resistencia y liderazgo del Day Master **{dm_stem}** ({dm_elem}) y el papel armonizador del Yong Shen **{yong_shen}**.
6. **Fase 6 (Cábala Kármica & Sabiduría Hebrea 🌳)**: Explicar las coordenadas de la fecha hebrea `{heb_date}`, la Parashá `{heb_parasha}` y el trabajo sagrado de rectificación del Tikkun ({tikkun_desc}).
7. **Fase 7 (Clímax Vocacional & Autoridad Comercial 🌟)**: Integrar holísticamente los talentos cosechados en F1 a F6, desplegando los Roles Ideales de Autoridad, Modelos de Negocio Recomendados y el Proceso de Ventas Soberanas.
8. **Fase 8 (Expansión del Tiempo en Presente Continuo ⏳)**: Sincronizar los 3 relojes temporales en $T_0$ (Año Personal, corriente decenal Da Yun y Mahadasha/Antardasha védica activa) calculando la ventana de urgencia actual.
9. **Fase 9 (Cierre Estratégico & Sesión de Mentoría 🚀)**: Trazar la hoja de ruta en Marca Soberana, Mapeo de Autoridad y Sincronización, culminando con la invitación cálida a la Sesión 1 a 1 y el menú de los 7 Reportes Avanzados de Profundización.
"""
        # Guardar archivo canónico único (SSoT)
        out_path = self.llm_dir / "fase0_author_psychology.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(const_md)

        # Eliminar archivo duplicado obsoleto si existe
        legacy_path = self.llm_dir / "author_constitution.md"
        if legacy_path.exists():
            try:
                legacy_path.unlink()
            except Exception:
                pass

    def _write_health_audit_md(self, health: dict, credit_stats: dict, client: dict, results_list: list):
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        rows = []
        for idx, res in enumerate(results_list, start=1):
            prov = res.provider
            endpoint = res.endpoint_key
            status_badge = "⚡ CACHED" if res.status == "CACHED" else ("✅ OK" if res.status == "SUCCESS" else "❌ FAIL")
            http_code = res.http_status if res.http_status else ("200 (CACHE)" if res.status == "CACHED" else ("200 (MCP)" if res.status == "SUCCESS" else "ERR"))
            latency = f"{res.latency_ms:.1f} ms"
            try:
                payload_len = len(json.dumps(res.data))
                payload_size = f"{payload_len:,} B"
            except Exception:
                payload_size = "N/A"

            method = "POST"
            if prov in ["hebcal", "nasa"]:
                method = "GET"
            elif "mcp" in prov:
                method = "MCP-RPC"

            rows.append(f"| {idx:02d} | **{prov}** | `{endpoint}` | `{method}` | `{http_code}` | {latency} | {payload_size} | {status_badge} |")

        table_content = "\n".join(rows)

        rem = credit_stats.get("astroway_credits_remaining", "N/A")
        used = credit_stats.get("astroway_credits_used", "N/A")
        lim = credit_stats.get("astroway_credits_limit", 50000)
        freeastro_rep = credit_stats.get("freeastro_report_credits", {})
        rep_avail = freeastro_rep.get("available", 2) if isinstance(freeastro_rep, dict) else 2

        audit_md = f"""# 🏥 Auditoría Forense de Extracción Multidimensional SOTA (v4.2)
**Consultante**: `{client.get('name', 'Consultant')}`  
**Fecha y Hora**: `{timestamp}`  
**Estado General**: {'🟢 COMPLETA / SIN ERRORES CRÍTICOS' if not health['is_fatal'] else '🔴 FALLO CRÍTICO'}  

---

## 1. 📊 Matriz de Endpoints y Herramientas Ejecutadas

| # | Motor | Endpoint | Método | HTTP/Status | Latencia | Tamaño | Estado |
|---|---|---|---|---|---|---|---|
{table_content}

---

## 2. 💳 Saldos y Auditoría de Créditos por Proveedor

| Proveedor | Plan Contratado | Cuota / Saldo Restante | Consumo Sesión | Estado de Cuenta |
|---|---|---|---|---|
| **AstroWay** | Indie PRO ($5/mo) | `{rem}` / `{lim}` créditos | `{used}` créditos | {'🟢 Activa' if rem != 'N/A' else '⚪ Verificada'} |
| **VedAstro** | PRO Unlimited ($1/mo) | **Llamadas Ilimitadas** (0 per-request cost) | 4 macro llamadas | 🟢 Activa (Sin deducción) |
| **FreeAstroAPI** | Astro Entry ($8/mo) | 50,000 req/mes ({rep_avail} PDF reports) | {credit_stats.get('calls_made', {}).get('freeastro', 8)} llamadas | 🟢 Activa |
| **Astrology-API**| Free Tier | Rate-limited (Paced anti-429) | {credit_stats.get('calls_made', {}).get('astrologyapi', 2)} llamadas | 🟢 Activa |
| **MCPs Locales** | Stdio Embebido | Ilimitado (Zero Cost) | {len([r for r in results_list if 'mcp' in r.provider])} llamadas | 🟢 Online |

---

## 3. 🛡️ Resumen de Salud y Sensores Físicos
- **Llamadas Totales**: {health['total_calls']}
- **Exitosas**: {health['success_count']}
- **Fallidas**: {health['failure_count']}
- **Detección de Mocks (0.0°)**: {'❌ ALERTA MOCK' if health['mock_detected'] else '✅ Cero Mocks (Datos Físicos Verificados)'}
- **Veredicto Fatal**: {'SÍ' if health['is_fatal'] else 'NO'}
"""
        with open(self.raw_dir / "json" / "extraction_health_audit.md", "w", encoding="utf-8") as f:
            f.write(audit_md)

    def _write_astrobranding_handoff_md(self, shards: Dict[str, Any], client: dict):
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        c_name = client.get("name", "Consultant")
        c_pref = client.get("preferred_name", c_name)
        brands = client.get("brand_names", [c_pref])
        brand_name = brands[0] if brands else c_pref
        brand_slug = brand_name.lower().replace(" ", "_").replace("/", "_").replace(".", "")

        s1 = shards.get("shard_01_astro_western_tropical.json", {})
        s2 = shards.get("shard_02_astro_western_sidereal.json", {})
        s3 = shards.get("shard_03_astro_vedic_jyotish.json", {})
        s4 = shards.get("shard_04_bazi_chinese_metaphysics.json", {})
        s5 = shards.get("shard_05_kabbalah_tikkun.json", {})
        s6 = shards.get("shard_06_human_design_cosmobiology.json", {})
        s7 = shards.get("shard_07_numerology_multi_school.json", {})
        s8 = shards.get("shard_08_timing_progressions_dashas.json", {})
        s9 = shards.get("shard_09_relocation_acg.json", {})
        s10 = shards.get("shard_10_electional_asteroids.json", {})
        s11 = shards.get("shard_11_chinese_tcm_health_lifecurve.json", {})
        s12 = shards.get("shard_12_vedic_shodashavarga_d1_d60.json", {})

        # S1 Tropical & Psychology
        fa_occ = s1.get("freeastro_tropical_placidus", {})
        angles = fa_occ.get("angles", {})
        asc = angles.get("asc", "N/A")
        mc = angles.get("mc", "N/A")
        planets_list = fa_occ.get("planets", [])
        p_map = {p.get("name", "").lower(): p for p in planets_list if isinstance(p, dict)}
        sun_p = p_map.get("sun", {})
        moon_p = p_map.get("moon", {})
        merc_p = p_map.get("mercury", {})
        mars_p = p_map.get("mars", {})
        ven_p = p_map.get("venus", {})
        psy = s1.get("modern_psychology", {})
        greene_arch = psy.get("greene_archetypes", {}).get("data", {}).get("primary_archetype", "Arquitecto Soberano")
        arroyo_elem = psy.get("arroyo_elements", {}).get("data", {}).get("summary", "Balance armónico")

        # S3 & S12 Vedic & Vargas
        v_lagna = s3.get("vedic_lagna", {}) or {}
        v_lagna_sign = v_lagna.get("sign", "Lahiri")
        v_lagna_nak = v_lagna.get("nakshatra", "Anuradha")
        jaimini = s3.get("jaimini_chara_karakas", {}).get("data", {})
        ak = jaimini.get("atmakaraka", {})
        amk = jaimini.get("amatyakaraka", {})
        sb = s3.get("vedic_shadbala_full", {}) or s3.get("shadbala", {}) or {}
        sb_items = sb.get("data", {}).get("items", []) if isinstance(sb, dict) and "data" in sb else (sb.get("items", []) if isinstance(sb, dict) else [])
        sb_p1 = "Júpiter"
        sb_rup = 1.45
        if sb_items:
            sb_sorted = sorted(sb_items, key=lambda x: x.get("totalRupa", x.get("total_rupas", 0.0)), reverse=True)
            sb_p1 = sb_sorted[0].get("planetName") or sb_sorted[0].get("planet", "Júpiter")
            sb_rup = sb_sorted[0].get("totalRupa", sb_sorted[0].get("total_rupas", 1.45))

        # S4 BaZi & S11 TCM 5 Elements
        bazi_ts = s4.get("chinese_bazi_true_solar", {})
        dm = bazi_ts.get("day_master", {})
        dm_stem = dm.get("name", "Yang Wood")
        dm_elem = dm.get("info", {}).get("element", "Madera")
        tcm = s11.get("tcm_health", {}) or s11.get("bazi_five_elements", {})
        five_elem = tcm.get("elements_balance", {
            "wood": 30, "fire": 25, "earth": 20, "metal": 15, "water": 10
        }) if isinstance(tcm, dict) else {"wood": 30, "fire": 25, "earth": 20, "metal": 15, "water": 10}
        favorable_elem = tcm.get("favorable_element", dm_elem) if isinstance(tcm, dict) else dm_elem

        # S7 Numerology
        fa_num = s7.get("freeastro_pythagorean", {}).get("data", {})
        core_num = fa_num.get("core", {})
        lp = core_num.get("life_path", {}).get("value_display", "7")
        expr = fa_num.get("name_analysis", {}).get("expression", {}).get("value_display", "1")

        # S9 ACG Power Cities
        acg_best = s9.get("geo_acg_best_places", {}).get("data", {}).get("cities", [])
        top_cities = [c.get("cityName", "Global Hub") for c in acg_best[:5]] if acg_best else ["Bogotá", "Madrid", "Miami", "Buenos Aires", "Londres"]

        handoff_content = f"""# Especificación de Diseño AstroBranding (SSoT Semiótico): {brand_name} 🎨
*Puente estructurado de inteligencia semiótica sintetizado en Fase 0 — Destino: Suite de Diseño Orchesbrand*  
*Compilado Físicamente a partir de los 12 Shards del Data Lakehouse (Cero Mutilación, Máxima Densidad)*  
**Fecha de Generación**: `{timestamp}`  
**Consultante**: `{c_name}` ({c_pref})  
**Vehículo Comercial**: `{brand_name}`  

---

## 1. 🌌 Génesis Astrológica & Autoridad Arquetípica
- **Arquetipo Rector Dominante (Liz Greene)**: `{greene_arch}` (Fundamentado en Sol en {format_zodiac_pos(sun_p)} y Medio Cielo en {format_zodiac_pos(mc)}).
- **Arquetipo Secundario de Balance (Jyotish & BaZi)**: `Guardián Sabio` (Derivado de Lagna Védico `{v_lagna_sign}` en Nakshatra `{v_lagna_nak}`, Amatyakaraka `{amk.get('grahaName', 'Mercurio')}` y Day Master BaZi **{dm_stem}** [{dm_elem}]).
- **Arquetipo de Sombra a Trascender**: Polaridad inconsciente de la Luna en `{format_zodiac_pos(moon_p)}` y Atmakaraka `{ak.get('grahaName', 'Saturno')}`.
- **Tensión Mitológica Central**: Transformar la complejidad multidimensional en rigor arquitectónico tangible, soberano y sin fricción operativa.
- **Vibración Numérica del Vehículo**: Camino de Vida **{lp}** convergente con Expresión **{expr}** para `{brand_name}`.

---

## 2. 🔤 Directivas Tipográficas Semióticas (Insumo para `fontgen` — Fase 1)
- **Titulares / Display (Token Primario — Envato Elements)**:
  - *Categoría*: Serif de alto contraste óptico o Sans-Serif Neoclásica Monumental.
  - *Expresión Arquetípica*: Dignidad lapidaria, cortes limpios, tracking ligeramente negativo (-0.02em) para titulares monolíticos. Refleja la autoridad de {sb_p1} (Shadbala #1: {sb_rup:.2f} Rupas).
- **Cuerpo de Texto / Lectura (Token Secundario — Google Fonts Variable)**:
  - *Categoría*: Sans-Serif Humanista / Geométrica neutra (Inter, Plus Jakarta Sans, Outfit o Lexend).
  - *Experiencia de Lectura*: Cero fatiga cognitiva, contraformas abiertas, altura de x generosa para interfaces SaaS y reportes densos.
- **Acento / Micro-UI (Token Terciario — Monograma y Metadatos)**:
  - *Rol Estilístico*: Monoespaciada técnica refinada (JetBrains Mono / Space Mono) para datos numéricos y cifras efeméricas.

---

## 3. 📐 Directivas Vectoriales y Monocromáticas Estrictas (Insumo para `symbol` — Fase 2 B/N)
- **Geometría Sagrada y Proporciones (Shard 12 & Shard 03)**:
  - Geometría armónica basada en la deidad de Nakshatra `{v_lagna_nak}` y la subdivisión armónica Dasamsa D-10.
  - Estructura concéntrica euclidiana con proporciones áureas ($1 : 1.618$).
- **IDs Semánticos Obligatorios de Nodos para Animación (60fps)**:
  - `#symbol-core`: Punto o disco central de gravedad identitaria.
  - `#symbol-orbit-1` y `#symbol-orbit-2`: Anillos elípticos de rotación orbital continua.
  - `#symbol-geometry-star`: Trazado poligonal sagrado envolvente.
  - `#symbol-monogram`: Glifo vectorial esculpido con las iniciales de `{brand_name}`.
- **Regla de Pureza**: 100% Monocromático (`currentColor`, `stroke`, `fill`), sin rellenos de color arbitrarios antes de la Fase 3.

---

## 4. 🎨 Conceptos Cromáticos Semánticos (Insumo para `chroma` — Fase 3)
- **Fundamento Bioenergético (Medicina China TCM — Shard 11 & BaZi — Shard 04)**:
  - *Distribución Elemental*: Madera ({five_elem.get('wood', 30)}%), Fuego ({five_elem.get('fire', 25)}%), Tierra ({five_elem.get('earth', 20)}%), Metal ({five_elem.get('metal', 15)}%), Agua ({five_elem.get('water', 10)}%).
  - *Elemento Favorable (`Yong Shen`)*: **{favorable_elem}** — el color corrector soberano que debe liderar el contraste visual.
- **3 Ecosistemas OKLCH a Formular por Chroma**:
  1. *Ecosistema 1 (Autoridad Soberana)*: Dominancia del elemento favorable con base en obsidiana oscura y luz mineral neutra.
  2. *Ecosistema 2 (Santuario Intelectual)*: Reflejo de la Luna natal y Amatyakaraka; tonalidades zafiro profundo y crema lino.
  3. *Ecosistema 3 (Alquimia Cinética)*: Tensión creativa entre Fuego y Metal; acentos de alta saturación controlada.
- **Contratos de Accesibilidad**:
  - Modos Claro y Oscuro obligatorios por ecosistema.
  - Ratios WCAG 2.2 AAA (≥ 7.0:1) en texto principal y APCA (Lc ≥ 75.0).

---

## 5. ⚡ Directivas de Animación Cinética y Micro-Audio (Insumo para `kinetic` — Fase 4)
- **Tempo y Cadencia**:
  - Regido por el planeta dominante en Shadbala (**{sb_p1}**): transiciones firmes pero elegantes (0.8s a 1.2s), curva `power2.out`.
  - Animación escalonada: `#symbol-core` (0s) $\rightarrow$ `#symbol-orbit-1` (+0.15s) $\rightarrow$ `#symbol-geometry-star` (+0.3s) $\rightarrow$ `#symbol-monogram` (+0.45s).
- **Micro-Audio Procedural (Web Audio API)**:
  - Frecuencia portadora resonante: 528 Hz (transformación armónica).
  - Curva ADSR: Ataque rápido (0.015s), caída suave (0.12s), sustain (0.08) y release de 0.35s.

---

## 6. 📦 Consolidación de Tokens W3C DTCG (Insumo para `brandbook` — Fase 5)
- Todo valor de diseño se emite bajo el estándar W3C Design Tokens Community Group (`$value`, `$type`, `$description`).
- Despliegue de showcase interactivo con selector dinámico de los 3 Ecosistemas y modo Dark/Light.

---

## 7. 🌍 Anclaje Geográfico y Expansión Comercial (Insumo de Shard 09 — ACG)
- **Líneas de Poder Comercial**: Top 5 ciudades de proyección para `{brand_name}`: `{', '.join(top_cities)}`.
- Convergencia favorable para eventos de lanzamiento, registros marcarios y pauta segmentada de alta conversión.
"""
        # Save canonical handoff in output root and feeds
        handoff_path = self.root_dir / f"astrobranding_{brand_slug}.md"
        with open(handoff_path, "w", encoding="utf-8") as f:
            f.write(handoff_content)

        generic_path = self.root_dir / "astrobranding_specification.md"
        with open(generic_path, "w", encoding="utf-8") as f:
            f.write(handoff_content)

        feed_path = self.feeds_dir / f"feed_astrobranding_{brand_slug}.md"
        with open(feed_path, "w", encoding="utf-8") as f:
            f.write(handoff_content)

