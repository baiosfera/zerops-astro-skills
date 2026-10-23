---
name: nasa
description: "Trigger: nasa, nasa jpl horizons, ephemerides de440 de441, asteroids tracking, cad close approach, neows near earth objects, donki space weather. Motor REST de efemerides cientificas y datos de la NASA."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# `nasa` — NASA JPL Horizons & Open APIs Engine (v1.2)

## Activation Contract
High-precision NASA Jet Propulsion Laboratory (JPL) Horizons ephemerides (DE440/DE441), SBDB CAD close approaches, NeoWs asteroid tracking, and DONKI space weather across REST endpoints.

## Core Architecture & Invariants
- **Horizons REST API**: `https://ssd.jpl.nasa.gov/api/horizons.api` for physical ephemerides, vectors, and osculating elements. Authentication uses `$NASA_API_KEY` with fallback to `DEMO_KEY` for `api.nasa.gov`.
- **Semicolon Rule for Small Bodies**: Small body number IDs in Horizons require `%3B` (e.g. `COMMAND='1%3B'` for Ceres). Omitting `%3B` selects planet barycenters (e.g. `COMMAND='1'` selects Mercury Barycenter).
- **Marker Parsing**: Ephemeris tables reside between `$$SOE` and `$$EOE` markers; parse with `awk '/\$\$SOE/{flag=1;next}/\$\$EOE/{flag=0}flag'`.
- **Process Hygiene**: Timeouts $\le$ 10s (`timeout 10s`), max 2 retries on 500/timeout, terminate background tasks via `manage_task action="kill"`.

## Decision Gates & References

| Module | Route / Base URL | Key Arguments | Reference |
|---|---|---|---|
| Observer Ephemeris | `GET ssd.jpl.nasa.gov/api/horizons.api` | `COMMAND='499'`, `QUANTITIES='1,2,9,31'` | [`usage.md`](file:///var/www/zerops-astro-skills/nasa/references/usage.md) |
| Minor Bodies & Centaurs | `GET ssd.jpl.nasa.gov/api/horizons.api` | `COMMAND='<ID>%3B'`, `EPHEM_TYPE='OBSERVER'` | [`usage.md`](file:///var/www/zerops-astro-skills/nasa/references/usage.md) |
| State Vectors (DE440) | `GET ssd.jpl.nasa.gov/api/horizons.api` | `COMMAND='10'`, `EPHEM_TYPE='VECTORS'`, `CENTER='500@0'` | [`usage.md`](file:///var/www/zerops-astro-skills/nasa/references/usage.md) |
| Keplerian Elements | `GET ssd.jpl.nasa.gov/api/horizons.api` | `COMMAND='2060%3B'`, `EPHEM_TYPE='ELEMENTS'` | [`usage.md`](file:///var/www/zerops-astro-skills/nasa/references/usage.md) |
| CAD Close Approach | `GET ssd-api.jpl.nasa.gov/cad.api` | `dist-max=10LD`, `class=CEN,TNO` | [`usage.md`](file:///var/www/zerops-astro-skills/nasa/references/usage.md) |
| NeoWs Asteroid Feed | `GET api.nasa.gov/neo/rest/v1/feed` | `start_date`, `end_date`, `api_key` | [`usage.md`](file:///var/www/zerops-astro-skills/nasa/references/usage.md) |
| Space Weather (DONKI) | `GET api.nasa.gov/DONKI/FLR` | `startDate`, `endDate`, `api_key` | [`usage.md`](file:///var/www/zerops-astro-skills/nasa/references/usage.md) |
| Infrastructure | Rate limits, parsing, error catalog | `NASA_API_KEY`, 1000 req/hr quota | [`infra.md`](file:///var/www/zerops-astro-skills/nasa/references/infra.md) |

## Output Contract
Parse JSON envelopes with `jq`. Extract tabulated CSV from `.result` using `$$SOE`/`$$EOE` markers and pass to downstream timing or relocation modules.
