# NASA JPL Horizons & Open APIs Technical Usage Manual

Comprehensive developer and agent reference manual for the NASA Jet Propulsion Laboratory (JPL) Horizons REST system (`https://ssd.jpl.nasa.gov/api/horizons.api`), JPL SBDB CAD API (`https://ssd-api.jpl.nasa.gov/cad.api`), and the NASA Open APIs portal (`https://api.nasa.gov/`).

---

## 1. NASA JPL Horizons Common Parameter Standards

### Key Query Parameters:
- `format=json`: Returns JSON envelope containing the formatted output string under `.result`.
- `COMMAND`: Body ID string (enclosed in single quotes).
  - **Planets & Major Centers**: Sun: `'10'`, Moon: `'301'`, Mercury: `'199'`, Venus: `'299'`, Mars: `'499'`, Jupiter: `'599'`, Saturn: `'699'`, Uranus: `'799'`, Neptune: `'899'`, Pluto: `'999'` (or `'134340%3B'`).
  - **Small Bodies (Mandatory `%3B` Rule)**: Asteroids, centaurs, and TNOs require a trailing semicolon `%3B` to avoid collision with planet barycenters:
    * `COMMAND='1'` $\rightarrow$ Mercury Barycenter.
    * `COMMAND='1%3B'` $\rightarrow$ 1 Ceres.
- `CENTER`: Coordinate origin:
  - `'500@399'`: Geocentric (Earth center).
  - `'coord@399'`: Topocentric on Earth surface (with `SITE_COORD='<LNG>,<LAT>,<ELEV>'` and `COORD_TYPE='GEODETIC'`).
  - `'500@0'`: Solar System Barycenter (SSB).
  - `'500@10'`: Heliocentric (Sun center).
  - `'500@301'`: Selenocentric (Moon center).
- `START_TIME` & `STOP_TIME`: ISO dates (`'<YYYY>-<MM>-<DD>'` or `'<YYYY>-<MM>-<DD> <HH>:<mm>'`).
- `STEP_SIZE`: Increment step (e.g. `'1d'`, `'1h'`, `'10m'`).
- `QUANTITIES`: Desired output columns:
  - `1`: Astrometric RA & DEC (ICRF).
  - `2`: Apparent RA & DEC (corrected for light-time and aberration).
  - `9`: Visual magnitude (`APmag`) and surface brightness (`S-brt`).
  - `31`: **Observer Ecliptic Longitude & Latitude (`ObsEcLon`, `ObsEcLat`)** — Direct zodiacal coordinates.
  - `43`: Phase angle and bisector (`phi`, `PAB-LON`, `PAB-LAT`).
- `CSV_FORMAT='YES'`: Formats tabulated ephemeris rows as comma-separated values between `$$SOE` and `$$EOE` markers.

---

## 2. Module 1: Geocentric Observer Table Ephemeris

Retrieves apparent Right Ascension, Declination, Ecliptic Longitude/Latitude, and Visual Magnitude.

### Geocentric Mars Observer Ephemeris:
```bash
timeout 10s curl -s "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='499'&EPHEM_TYPE='OBSERVER'&CENTER='500@399'&START_TIME='<START_DATE>'&STOP_TIME='<STOP_DATE>'&STEP_SIZE='1d'&QUANTITIES='1,2,9,31,43'&CSV_FORMAT='YES'" | jq -r '.result' | awk '/\$\$SOE/{flag=1;next}/\$\$EOE/{flag=0}flag'
```

### Key Output Columns:
- `R.A._(ICRF)` & `DEC_(ICRF)`: Astrometric right ascension and declination.
- `R.A._(a-apparent)` & `DEC_(a-apparent)`: Apparent equatorial coordinates.
- `ObsEcLon` & `ObsEcLat`: Apparent ecliptic longitude and latitude (Zodiac position).
- `APmag`: Apparent visual magnitude.

---

## 3. Module 2: Cartesian State Vectors (DE440/DE441)

Generates 3D barycentric or heliocentric Cartesian position and velocity vectors ($X, Y, Z, V_x, V_y, V_z$) in the ICRF frame.

### Barycentric Earth-Moon State Vectors:
```bash
timeout 10s curl -s "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='399'&EPHEM_TYPE='VECTORS'&CENTER='500@0'&START_TIME='<START_DATE>'&STOP_TIME='<STOP_DATE>'&STEP_SIZE='1d'&OUT_UNITS='AU-D'&VEC_TABLE='3'&CSV_FORMAT='YES'" | jq -r '.result' | awk '/\$\$SOE/{flag=1;next}/\$\$EOE/{flag=0}flag'
```

---

## 4. Module 3: Osculating Keplerian Orbital Elements

Extracts instantaneous osculating Keplerian orbital elements relative to the Sun.

### Chiron (2060) Orbital Elements:
```bash
timeout 10s curl -s "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='2060%3B'&EPHEM_TYPE='ELEMENTS'&CENTER='500@10'&START_TIME='<START_DATE>'&STOP_TIME='<STOP_DATE>'&STEP_SIZE='1d'&CSV_FORMAT='YES'" | jq -r '.result' | awk '/\$\$SOE/{flag=1;next}/\$\$EOE/{flag=0}flag'
```

### Returned Elements:
- `EC`: Eccentricity ($e$).
- `QR`: Perihelion distance ($q$, AU).
- `IN`: Inclination ($i$, degrees).
- `OM`: Longitude of Ascending Node ($\Omega$, degrees).
- `W`: Argument of Perihelion ($\omega$, degrees).
- `Tp`: Time of perihelion passage (Julian Date).
- `N`: Mean motion ($n$, deg/day).
- `MA`: Mean anomaly ($M$, degrees).
- `A`: Semi-major axis ($a$, AU).

---

## 5. Module 4: Asteroids, Centaurs & Transneptunians (TNOs)

Track minor planets using their permanent IAU numbers with the mandatory `%3B` suffix:

### Minor Bodies Catalog:
| Category | Body Name | IAU Number | Horizons Command |
|---|---|---|---|
| **Classical Asteroids** | 1 Ceres | 1 | `COMMAND='1%3B'` |
| | 2 Pallas | 2 | `COMMAND='2%3B'` |
| | 3 Juno | 3 | `COMMAND='3%3B'` |
| | 4 Vesta | 4 | `COMMAND='4%3B'` |
| | 433 Eros | 433 | `COMMAND='433%3B'` |
| | 99942 Apophis | 99942 | `COMMAND='99942%3B'` |
| **Centaurs** | 2060 Chiron | 2060 | `COMMAND='2060%3B'` |
| | 5145 Pholus | 5145 | `COMMAND='5145%3B'` |
| | 7066 Nessus | 7066 | `COMMAND='7066%3B'` |
| | 10199 Chariklo | 10199 | `COMMAND='10199%3B'` |
| | 8405 Asbolus | 8405 | `COMMAND='8405%3B'` |
| | 10370 Hylonome | 10370 | `COMMAND='10370%3B'` |
| **TNOs & Plutinos** | 136199 Eris | 136199 | `COMMAND='136199%3B'` |
| | 136108 Haumea | 136108 | `COMMAND='136108%3B'` |
| | 136472 Makemake | 136472 | `COMMAND='136472%3B'` |
| | 90377 Sedna | 90377 | `COMMAND='90377%3B'` |
| | 50000 Quaoar | 50000 | `COMMAND='50000%3B'` |
| | 90482 Orcus | 90482 | `COMMAND='90482%3B'` |
| | 20000 Varuna | 20000 | `COMMAND='20000%3B'` |
| | 28978 Ixion | 28978 | `COMMAND='28978%3B'` |
| | 225088 Gonggong | 225088 | `COMMAND='225088%3B'` |
| | 120347 Salacia | 120347 | `COMMAND='120347%3B'` |

### Example cURL (Chariklo 10199):
```bash
timeout 10s curl -s "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='10199%3B'&EPHEM_TYPE='OBSERVER'&CENTER='500@399'&START_TIME='<START_DATE>'&STOP_TIME='<STOP_DATE>'&STEP_SIZE='1d'&QUANTITIES='1,2,9,31'&CSV_FORMAT='YES'" | jq -r '.result' | awk '/\$\$SOE/{flag=1;next}/\$\$EOE/{flag=0}flag'
```

---

## 6. Module 5: JPL SBDB Close-Approach Data API (CAD API v1.5)

Searches multi-body close encounters across all asteroids and cometas in native structured JSON:

### Multi-Object Close Encounters Query:
```bash
# Query close approaches within 10 Lunar Distances (10LD) for Centaurs and TNOs
timeout 10s curl -s "https://ssd-api.jpl.nasa.gov/cad.api?dist-max=10LD&date-min=<START_DATE>&date-max=<STOP_DATE>&class=CEN,TNO&sort=dist&fullname=true" | jq '{count, data: .data[:5]}'
```

### Key Query Parameters:
- `date-min` & `date-max`: Date range (`<YYYY>-<MM>-<DD>` or `now`).
- `dist-max`: Maximum encounter distance (e.g. `0.05` AU or `10LD`).
- `body`: Target body (`Earth`, `Moon`, `Mars`, `Juptr`, `ALL`).
- `class`: Orbit class (`CEN`, `TNO`, `ATE`, `APO`, `AMO`, `MBA`, `TJN`).
- `pha=true`: Filter Potentially Hazardous Asteroids.
- `fullname=true`: Include formal asteroid name.

---

## 7. Module 6: NASA NeoWs (Near Earth Object Web Service)

Queries NASA's near-Earth asteroid feed and lookup service:

### Daily Asteroid Feed:
```bash
timeout 10s curl -s "https://api.nasa.gov/neo/rest/v1/feed?start_date=<START_DATE>&end_date=<STOP_DATE>&api_key=${NASA_API_KEY:-DEMO_KEY}" | jq '.near_earth_objects'
```

### Asteroid SPK Lookup:
```bash
timeout 10s curl -s "https://api.nasa.gov/neo/rest/v1/neo/<SPK_ID>?api_key=${NASA_API_KEY:-DEMO_KEY}" | jq '{name, estimated_diameter, close_approach_data: .close_approach_data[:3]}'
```

---

## 8. Module 7: NASA DONKI Space Weather (Flares & CMEs)

Monitors space weather, geomagnetic storms, and solar flares:

### Solar Flares (FLR):
```bash
timeout 10s curl -s "https://api.nasa.gov/DONKI/FLR?startDate=<START_DATE>&endDate=<STOP_DATE>&api_key=${NASA_API_KEY:-DEMO_KEY}" | jq '.[] | {flrID, beginTime, peakTime, classType}'
```

### Geomagnetic Storms (GST):
```bash
timeout 10s curl -s "https://api.nasa.gov/DONKI/GST?startDate=<START_DATE>&endDate=<STOP_DATE>&api_key=${NASA_API_KEY:-DEMO_KEY}" | jq '.[] | {gstID, startTime, allKpIndex}'
```

---

## 9. Module 8: Physical Astronomical Constants (OBJ_DATA)

Extracts physical constants, rotational periods, and GM values without generating ephemeris tables:

```bash
timeout 10s curl -s "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='599'&OBJ_DATA='YES'&MAKE_EPHEM='NO'" | jq -r '.result'
```
