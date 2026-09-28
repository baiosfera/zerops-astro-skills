# NASA JPL Horizons & Open APIs Canonical Reference Pointer

NASA JPL Horizons & Open APIs are now maintained as a sovereign first-class Dual-RAG System Skill in the workspace.

## Primary Documentation Links

- **Main Router**: [.agents/skills/nasa/SKILL.md](file:///var/www/.agents/skills/nasa/SKILL.md)
- **Comprehensive Usage Manual (8 Modules)**: [.agents/skills/nasa/references/usage.md](file:///var/www/.agents/skills/nasa/references/usage.md)
- **Infrastructure, Horizons Parameters & CoHaLo Guide**: [.agents/skills/nasa/references/infra.md](file:///var/www/.agents/skills/nasa/references/infra.md)

## Integrated Domains Summary

1. **Observer Table Planetary Ephemeris**: `EPHEM_TYPE='OBSERVER'`, `CENTER='500@399'`.
2. **Cartesian State Vectors (DE440/DE441)**: `EPHEM_TYPE='VECTORS'`, `CENTER='500@0'`.
3. **Osculating Keplerian Orbital Elements**: `EPHEM_TYPE='ELEMENTS'`, `CENTER='500@10'`.
4. **Asteroids, Centaurs & Minor Bodies**: Ceres ('1'), Vesta ('4'), Chiron ('2060'), Sedna ('90377').
5. **Close-Approach Tables**: `EPHEM_TYPE='APPROACH'`.
6. **NASA NeoWs Asteroid Feed**: `https://api.nasa.gov/neo/rest/v1/feed`.
7. **NASA DONKI Space Weather**: `/DONKI/FLR`, `/DONKI/CME`, `/DONKI/GST`.
8. **Physical Constants (OBJ_DATA)**: `OBJ_DATA='YES'`.
