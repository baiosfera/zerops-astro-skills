---
name: kundali
description: "Trigger: kundali, kundali mcp, shodashavarga d1-d60, shadbala 6 factors, vimshottari 5 levels, kundali milan 36 gunas, pramaan bphs, muhurat. Motor MCP de calculo Jyotish de precision."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---
# Kundali Jyotish & Shodashavarga MCP Engine

Agentic-AI Vedic Jyotish computation suite exposing high-precision Shodashavarga divisional charts (D1–D60), 6-factor Shadbala strength, 5-level Vimshottari Dashas, and classical scriptural citations across 10 native MCP tools.

## Core Architecture

Kundali operates via a dedicated Model Context Protocol server (`https://mcp.kundalimcp.com/mcp` and local schemas). Authentication uses Bearer tokens prioritizing `$KUNDALI_MCP_KEY` with fallback to `$kundali_mcpKey` (`Authorization: Bearer ${KUNDALI_MCP_KEY:-$kundali_mcpKey}`). Historical timezones are accurately resolved using the full `chrono-tz` IANA database.

- **Primary Reference**: [references/usage.md](file:///var/www/.agents/skills/kundali/references/usage.md) — Comprehensive tool invocations for all 10 native tools across 9 functional modules.
- **Infrastructure Guide**: [references/infra.md](file:///var/www/.agents/skills/kundali/references/infra.md) — Remote/local MCP connection, authentication cascade, JSON-RPC 2.0 error codes, and CoHaLo process hygiene.

## Available Engines & Modules

1. **Vedic Natal (`kundali`)**: Lagna, Bhavas, Grahas, Yogas, and boundary checks (`boundary_sensitive`).
2. **16 Shodashavargas (D1–D60)**: Divisional charts (`vargas: ["D1".."D60"]`).
3. **6-Factor Shadbala**: Sthana, Dig, Kala, Chesta, Naisargika, and Drik Bala.
4. **5-Level Vimshottari Dashas**: Maha through Prana dashas with `dasha_branch` drilldown.
5. **Ashtakoota Milan (`kundali_milan`)**: 36 Gunas scoring with structured `groom` and `bride` objects.
6. **Life Timeline (`lifemap`)**: Multi-year forecast and transit ingress scans.
7. **Panchanga (`panchang`)**: Tithi, Vara, Nakshatra, Yoga, Karana, and inauspicious windows.
8. **Observances (`festivals`)**: Tithi and solar recurrence scans ($\le$ 400 days).
9. **Auspicious Timing & Proofs (`muhurat`, `pramaan`)**: 24 electional activities and BPHS/Jaimini proof trees.
10. **AI Chat & System (`chat`, `submit_feedback`, `get_version`)**: Grounded Vedic chat, CIL feedback, and engine status.

## Critical Workflows

1. **Local Naive Datetime Input**: Pass `birth_datetime` as local naive clock time (`YYYY-MM-DDTHH:mm:ss`) without 'Z' or timezone offsets.
2. **Structured Objects**: Pass `groom: {birth_datetime, latitude, longitude}` and `bride: {...}` in `kundali_milan`, and `chart_ref: {...}` in `pramaan`.
3. **Auspicious Electional Timing**: Use `muhurat` specifying one of 24 `event_type` options and optional `scan_end` ($\le$ 31 days).
4. **Process Hygiene (CoHaLo)**: Maximum 10s execution timeouts (`timeout 10s`), `WaitMsBeforeAsync: 10000`, Zero Orphaned Tasks (`manage_task action="kill"`).
5. **Circuit Breakers**: Max 2 retries on 500/timeout before escalation; verify `headline` and `facts`.

## Quick Reference Table

| Module | Native Tool | Key Arguments |
|---|---|---|
| Full Chart | `kundali` | `birth_datetime`, `latitude`, `longitude`, `school`, `locale` |
| Divisional Charts | `kundali` | `include: "vargas"`, `vargas: ["D9","D10"]` |
| Marriage Matching | `kundali_milan` | `groom`, `bride`, `school`, `locale` |
| Auspicious Timing | `muhurat` | `datetime`, `latitude`, `longitude`, `event_type` |
| Life Timeline | `lifemap` | `birth_datetime`, `latitude`, `longitude` |
| Vedic Calendar | `panchang` | `datetime`, `latitude`, `longitude`, `locale` |
| Observances | `festivals` | `start_date`, `end_date`, `latitude`, `longitude` |
| Scriptural Proofs | `pramaan` | `chart_ref`, `claim_id`, `school`, `locale` |
| Vedic AI Chat | `chat` | `message`, `locale`, `birth_datetime` |
| Engine Status | `get_version` | `{}` |

## Output Contract

Parse JSON responses directly with `jq` or JSON parsers. Always verify `facts.planets` and `facts.active_dasha`. Report calculation results directly to downstream diagnostic or branding modules.
