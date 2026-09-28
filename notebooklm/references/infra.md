# Gemini Notebook / NotebookLM Infrastructure & Authentication Architecture

Este manual documenta los fundamentos de infraestructura, transporte de red, persistencia de credenciales y arnés operativo bajo **Fractal CoHaLo** para Gemini Notebook.

---

## 1. Arquitectura de Autenticación & Ciclo de Vida de Cookies

Google NotebookLM no ofrece una API pública con tokens Bearer convencionales. La autenticación se realiza simulando una sesión de Google Workspace / Google Account válida a través de un pool de hasta 16 cookies HTTP.

### A. La Jerarquía de Cookies y el Desafío de Frescura
- **Cookies de Identidad de Larga Duración:** `SID`, `HSID`, `SSID`, `APISID`, `SAPISID`, `__Secure-1PSID`, `__Secure-3PSID`. Estas cookies identifican la cuenta (`baiosfera.com@gmail.com`) y son válidas por meses.
- **Tokens de Frescura y Rotación Rápida:** `__Secure-1PSIDTS` y `__Secure-3PSIDTS`. 
  - **Tiempo de vida:** 12 a 24 horas.
  - **Invariante:** Google exige `__Secure-1PSIDTS` en todas las llamadas `batchexecute`. Si decae, las llamadas retornan error de autenticación (código 3 / `INVALID_ARGUMENT` o HTTP 401).
  - **Rotación:** No puede renovarse mediante llamadas HTTP directas (`RotateCookies`). Requiere ejecución de JavaScript en un contexto de navegador legítimo (Chromium).

### B. Modos de Transporte RPC (`NOTEBOOKLM_RPC_TRANSPORT`)
El cliente soporta dos modos de transporte en `notebooklm_tools/core/client.py`:
1. `NOTEBOOKLM_RPC_TRANSPORT=http` (Default): Envía peticiones HTTP POST con `httpx` hacia `https://notebooklm.google.com/_/LabsTailwindUi/data/batchexecute`.
2. `NOTEBOOKLM_RPC_TRANSPORT=cdp`: Se conecta vía Chrome DevTools Protocol (CDP) a una instancia de Chromium headless abierta y ejecuta las llamadas inyectando `window.fetch()` directamente dentro del contexto web de Google. Esto garantiza que `__Secure-1PSIDTS` y los tokens CSRF se refresquen en segundo plano sin intervención manual.

### C. Entorno de Login Efímero noVNC (`nlm-vnc-login`)
Para renovar credenciales de forma visual e interactiva sin sobrecargar el servidor:
- Se inicia bajo demanda mediante el comando `nlm-vnc-login`.
- Despliega un entorno X11 virtual (`Xvfb`), gestor mínimo (`fluxbox`), `x11vnc`, `websockify` en el puerto **6080** y abre Chromium.
- **Consumo:** 0 MB de RAM en reposo (los procesos se detienen automáticamente al cerrar la sesión).
- Acceso: `http://<HOST>:6080/vnc.html`.

### D. Persistencia SSoT en Google Drive
Las credenciales de sesión se sincronizan y resguardan en:
`/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/mcp/.nlm-auth/`
- `nlm-cookies.json`: Snapshot de las cookies de sesión exportadas.
- Al aprovisionar un contenedor virgen con `unisetup.sh`, las credenciales se restauran automáticamente en `~/.notebooklm/` o el almacén de perfil de `nlm`.

---

## 2. Telemetría y Modelo de Cuotas de Cómputo (Septiembre 2026)

Gemini Notebook opera con un modelo de asignación de cómputo supervisado por dos ventanas temporales concurrentes:

| Ventana | Constante Interna | Duración / Alcance | Propósito |
|---|---|---|---|
| **Rolling** | `USAGE_WINDOW_ROLLING = 1` | ~5 horas | Control de saturación y ráfagas de inferencia o generación Studio. |
| **Semanal** | `USAGE_WINDOW_WEEKLY = 2` | 7 días (168 horas) | Límite agregado de cómputo para Gemini Pro / Ultra. |

### Monitoreo de Cuotas:
```bash
# Verificación vía CLI
nlm usage --json
```
Retorno estructurado:
```json
{
  "windows": [
    {
      "window": "rolling",
      "percent_used": 0.0,
      "percent_remaining": 100.0,
      "resets_at": "2026-09-21T19:37:24+00:00"
    },
    {
      "window": "weekly",
      "percent_used": 0.0,
      "percent_remaining": 100.0,
      "resets_at": "2026-09-28T14:37:24+00:00"
    }
  ],
  "tier": "NOTEBOOKLM_TIER_PRO_CONSUMER_USER"
}
```
O mediante el tool FastMCP `usage_get`.

### B. Contrato de Suscripción Google One AI Premium (`NOTEBOOKLM_TIER_PRO_CONSUMER_USER`)
La infraestructura opera formalmente bajo el plan de suscripción **Google One AI Premium (5TB)**, lo que otorga el nivel máximo de capacidad en Gemini Notebook:
- **Identificador de Tier Oficial:** `NOTEBOOKLM_TIER_PRO_CONSUMER_USER`.
- **Capacidad de Fuentes:** Hasta **300 fuentes** por cuaderno (frente al límite de 50 en el tier gratuito).
- **Límite por Fuente:** Hasta **500,000 palabras** o 200MB por fuente indexada.
- **Cuadernos por Cuenta:** Hasta **50 cuadernos** activos concurrentes.
- **Deep Research Avanzado:** Soporte completo de investigación profunda autónoma (`research_start(mode='deep', source='web'|'drive')`).
- **Cero Saldo de APIs Externas Pagas:** Las consultas RAG, la generación multivariada de Studio (audio, infografías, quizzes, presentaciones, reportes) y las sesiones socráticas con `nlm-tutor` se ejecutan **sin gastar saldo** de APIs de pago por token (OpenAI, Anthropic Claude, Groq o Cerebras).
- **Asignación de Cómputo:** Las cuotas de consumo se administran de manera nativa mediante las ventanas de saturación `rolling` (~5 horas) y `weekly` (7 días), garantizando alta disponibilidad sin costos imprevistos de facturación externa por token consumido.
- **Almacenamiento Cloud Nativo:** Todos los artefactos pesados (MP3, MP4, PDF, PNG) se alojan en Google Cloud Studio sin ocupar espacio en disco local, con descargas confinadas estrictamente a `NOTEBOOKLM_DOWNLOAD_DIR`.

---

## 3. Arnés Operativo CoHaLo (Bounded Execution & Hygiene)

Toda interacción con la CLI `nlm` o el servidor FastMCP en entornos Zerops debe respetar los arneses de contención:

1. **Timeouts Acotados:**
   - Comandos estándar de consulta y lectura: `timeout 10s nlm notebook list`.
   - Subidas de medios o procesamiento de audio: `--wait --wait-timeout 600`.
   - Polling de Studio: intervalos de 15 a 20 segundos con techo máximo de 900 segundos.
2. **Higiene de Subprocesos:**
   - Todo comando de larga duración ejecutado en segundo plano se gestiona con `WaitMsBeforeAsync: 10000`.
   - Procesos huérfanos o colgados deben ser abortados inmediatamente mediante `manage_task action="kill"`.
3. **Sensores Físicos de Atestación:**
   - Toda operación automatizada debe validar su código de salida determinista (`exit code 0`).
   - Los fallos RPC de Google deben ser inspeccionados en la respuesta JSON estructurada (`res.returncode == 0` con verificación de `status`).

---

## 4. Arquitectura de Sincronización Bidireccional de Notas y Sesiones REPL (`nlm-tutor`)

El subsistema `nlm-tutor` implementa un puente interactivo local-remoto que sincroniza de forma bidireccional el estado del estudiante entre la terminal y los servidores de Google NotebookLM mediante RPC `batchexecute`:

```
┌─────────────────────────────────┐               ┌─────────────────────────────────┐
│     Terminal Local (REPL)       │               │      Google NotebookLM Cloud     │
│   (nlm-tutor session / schedule)│               │      (Google One 5TB Storage)   │
├─────────────────────────────────┤               ├─────────────────────────────────┤
│ 1. Turno socrático del usuario  │ ──RPC chat──> │ • chat.send_message (historial) │
│ 2. Detección silenciosa de duda │ ──RPC note──> │ • 00_CUADERNO_DE_LAGUNAS (nota) │
│ 3. schedule (Ebbinghaus math)   │ <──RPC read── │ • Lectura de notas sin LLM      │
└─────────────────────────────────┘               └─────────────────────────────────┘
```

### A. Mecanismo de Sincronización de Turnos (`chat.send_message`)
- Cada turno del usuario en la sesión interactiva en terminal se envía hacia el hilo activo del cuaderno mediante el servicio RPC `notebooklm_tools.services.chat`.
- Esto garantiza que el historial pedagógico completo se conserve en la nube y sea accesible en cualquier momento desde la interfaz web oficial de NotebookLM.

### B. Persistencia Silenciosa de Lagunas en SSoT (`00_CUADERNO_DE_LAGUNAS`)
- Durante el diálogo socrático, las lagunas conceptuales identificadas por la rúbrica de evaluación se extraen algorítmicamente y se inyectan en tiempo real en la nota nativa del cuaderno `00_CUADERNO_DE_LAGUNAS` mediante `notebooklm_tools.services.notes.update_note`.
- **Cero Pérdida ante Desconexión:** Si la sesión de terminal o la conexión SSH se interrumpe, la nota permanece resguardada en la infraestructura de Google.
- **Acceso Algorítmico Desacoplado:** El subcomando `nlm-tutor schedule` lee directamente esta nota nativa mediante `notes.get_notes` para calcular las fechas exactas de repaso espaciado de Ebbinghaus, requiriendo **cero llamadas a modelos LLM** para planificar la memoria a largo plazo.

