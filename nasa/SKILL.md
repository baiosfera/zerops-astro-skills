---
name: nasa
description: "Trigger: nasa, nasa jpl horizons, ephemerides de440 de441, asteroids tracking, cad close approach, neows near earth objects, donki space weather. Motor REST de efemerides cientificas y datos de la NASA."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---
# NASA JPL Horizons & Open APIs Engine

High-precision NASA Jet Propulsion Laboratory (JPL) Horizons ephemeris calculation engine, SBDB CAD API, and NASA Open APIs suite for planetary bodies, asteroids, centaurs, TNOs, orbital state vectors, and space weather.

## Core Architecture

NASA astronomical services operate via REST endpoints: JPL Horizons (`https://ssd.jpl.nasa.gov/api/horizons.api`) for DE440/DE441 physical ephemerides, JPL SBDB CAD API (`https://ssd-api.jpl.nasa.gov/cad.api`) for multi-body close approaches, and NASA Open APIs (`https://api.nasa.gov/`) prioritizing `$NASA_API_KEY` with fallback to `$nasa_apiKey` and `DEMO_KEY`.

- **Primary Reference**: [references/usage.md](file:///var/www/.agents/skills/nasa/references/usage.md) — Comprehensive REST cURL templates, body IDs (`COMMAND`), coordinate centers (`CENTER`), and quantity parsing across all 9 modules.
- **Infrastructure Guide**: [references/infra.md](file:///var/www/.agents/skills/nasa/references/infra.md) — JPL Horizons parameters, rate limits (1,000 req/hr vs 30 req/hr), parsing markers, error taxonomy, and CoHaLo process hygiene.

## Available Engines & Modules

1. **Observer Table Planetary Ephemeris**: Geocentric (`500@399`) and topocentric apparent RA/Dec, ecliptic longitude/latitude (`QUANTITIES='31'`), and visual magnitude (`EPHEM_TYPE='OBSERVER'`).
2. **Cartesian State Vectors (DE440/DE441)**: ICRF barycentric and heliocentric 3D position and velocity vectors ($X, Y, Z, V_x, V_y, V_z$) (`EPHEM_TYPE='VECTORS'`).
3. **Osculating Keplerian Elements**: Semi-major axis, eccentricity, inclination, node, perihelion, and mean anomaly (`EPHEM_TYPE='ELEMENTS'`).
4. **Asteroids, Centaurs & TNOs**: Minor body tracking using the mandatory `%3B` semicolon rule (1 Ceres, 4 Vesta, 2060 Chiron, 5145 Pholus, 7066 Nessus, 10199 Chariklo, 90377 Sedna, 136199 Eris, 50000 Quaoar).
5. **SBDB Close-Approach Data API (CAD API)**: Multi-body close encounter search filtering by lunar distance (`dist-max=10LD`), date, and orbit class (`CEN`, `TNO`) (`/cad.api`).
6. **Object Close-Approach Tables**: Nominal dates, miss distance ($CA\_Dist$), and relative velocity ($V\_rel$) for a single object (`EPHEM_TYPE='APPROACH'`).
7. **NASA NeoWs**: Daily asteroid feed, miss distances, and Potentially Hazardous Asteroid (PHA) assessments (`/neo/rest/v1/feed`).
8. **NASA DONKI Space Weather**: Coronal Mass Ejections (CME), Solar Flares (FLR), and Geomagnetic Storms (GST).
9. **Physical Astronomical Constants**: Radius, mass, $GM$, density, albedo, and rotational period (`OBJ_DATA='YES'`, `MAKE_EPHEM='NO'`).

## Critical Workflows

1. **Semicolon Rule for Small Bodies**: Small body number IDs in Horizons require `%3B` (e.g. `COMMAND='1%3B'` for Ceres). Omitting `%3B` selects planet barycenters (e.g. `COMMAND='1'` selects Mercury Barycenter).
2. **CSV Marker Parsing**: Ephemeris tables reside between `$$SOE` and `$$EOE` markers; parse with `awk '/\$\$SOE/{flag=1;next}/\$\$EOE/{flag=0}flag'`.
3. **Process Hygiene (CoHaLo)**: Maximum 10s execution timeouts (`timeout 10s`), `WaitMsBeforeAsync: 10000`, Zero Orphaned Tasks (`manage_task action="kill"`).
4. **Circuit Breakers**: Max 2 retries on 500/timeout before escalation; verify HTTP 200 and `$$SOE` presence.

## Quick Reference Table

| Module | Route / Base URL | Key Query Parameters |
|---|---|---|
| Observer Ephemeris | `GET ssd.jpl.nasa.gov/api/horizons.api` | `COMMAND='499'`, `QUANTITIES='1,2,9,31'` |
| Minor Bodies | `GET ssd.jpl.nasa.gov/api/horizons.api` | `COMMAND='<ID>%3B'`, `EPHEM_TYPE='OBSERVER'` |
| State Vectors | `GET ssd.jpl.nasa.gov/api/horizons.api` | `COMMAND='10'`, `EPHEM_TYPE='VECTORS'`, `CENTER='500@0'` |
| Keplerian Elements | `GET ssd.jpl.nasa.gov/api/horizons.api` | `COMMAND='2060%3B'`, `EPHEM_TYPE='ELEMENTS'` |
| CAD Close Approach | `GET ssd-api.jpl.nasa.gov/cad.api` | `dist-max=10LD`, `class=CEN,TNO` |
| Asteroid Feed | `GET api.nasa.gov/neo/rest/v1/feed` | `start_date`, `end_date`, `api_key` |
| Space Weather | `GET api.nasa.gov/DONKI/FLR` | `startDate`, `endDate`, `api_key` |
| Physical Data | `GET ssd.jpl.nasa.gov/api/horizons.api` | `COMMAND='599'`, `OBJ_DATA='YES'` |

## Output Contract

Parse JSON envelopes with `jq`. Extract tabulated CSV from `.result` using `$$SOE`/`$$EOE` markers. Forward ephemeris data directly to downstream diagnostic, relocation, or planetary timing modules.
