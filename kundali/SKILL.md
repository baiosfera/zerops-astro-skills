---
name: kundali
description: "Trigger: kundali, kundali mcp, shodashavarga d1-d60, shadbala 6 factors, vimshottari 5 levels, kundali milan 36 gunas, pramaan bphs, muhurat. Motor MCP de calculo Jyotish de precision."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# `kundali` — Vedic Jyotish & Shodashavarga MCP Engine (v1.2)

## Activation Contract
High-precision Vedic Jyotish computations: Shodashavarga divisional charts (D1–D60), 6-factor Shadbala strength, 5-level Vimshottari Dashas, and classical scriptural citations (BPHS/Jaimini) across 10 native MCP tools.

## Core Architecture & Invariants
- **MCP Server Connection**: Operates via Model Context Protocol (`https://mcp.kundalimcp.com/mcp`). Authentication uses Bearer tokens prioritizing `$KUNDALI_MCP_KEY` with fallback to `$kundali_mcpKey`. Historical timezones resolve via `chrono-tz` IANA database.
- **Local Naive Datetime**: Pass `birth_datetime` as local naive clock time (`YYYY-MM-DDTHH:mm:ss`) without 'Z' or timezone offsets.
- **Structured Inputs**: Pass `groom: {birth_datetime, latitude, longitude}` and `bride: {...}` in `kundali_milan`, and `chart_ref: {...}` in `pramaan`.
- **Auspicious Timing**: Use `muhurat` with 24 `event_type` options and optional `scan_end` ($\le$ 31 days).
- **Process Hygiene**: Timeouts $\le$ 10s (`timeout 10s`), max 2 retries on 500/timeout, terminate background tasks via `manage_task action="kill"`.

## Decision Gates & References

| Module | Native Tool | Key Arguments | Reference |
|---|---|---|---|
| Natal & Shodashavarga | `kundali` | `birth_datetime`, `latitude`, `longitude`, `vargas` | [`usage.md`](file:///var/www/zerops-astro-skills/kundali/references/usage.md) |
| Marriage Matching | `kundali_milan` | `groom`, `bride`, `school`, `locale` | [`usage.md`](file:///var/www/zerops-astro-skills/kundali/references/usage.md) |
| Auspicious Timing | `muhurat` | `datetime`, `latitude`, `longitude`, `event_type` | [`usage.md`](file:///var/www/zerops-astro-skills/kundali/references/usage.md) |
| Life Timeline | `lifemap` | `birth_datetime`, `latitude`, `longitude` | [`usage.md`](file:///var/www/zerops-astro-skills/kundali/references/usage.md) |
| Vedic Calendar | `panchang` | `datetime`, `latitude`, `longitude`, `locale` | [`usage.md`](file:///var/www/zerops-astro-skills/kundali/references/usage.md) |
| Observances | `festivals` | `start_date`, `end_date`, `latitude`, `longitude` | [`usage.md`](file:///var/www/zerops-astro-skills/kundali/references/usage.md) |
| Scriptural Proofs | `pramaan` | `chart_ref`, `claim_id`, `school`, `locale` | [`usage.md`](file:///var/www/zerops-astro-skills/kundali/references/usage.md) |
| Infrastructure | Incus LXC / MCP | `KUNDALI_MCP_KEY`, remote MCP, JSON-RPC 2.0 | [`infra.md`](file:///var/www/zerops-astro-skills/kundali/references/infra.md) |

## Output Contract
Parse JSON responses directly with `jq`. Verify `facts.planets` and `facts.active_dasha` before passing to downstream diagnostic modules.
