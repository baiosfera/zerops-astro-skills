# Video Worker — Infrastructure, Zerops Lifecycle & Zero-Cost Manual (v2.0)

El servicio `videoworker` se rige por el principio de **efimeridad soberana**: no consume presupuesto de infraestructura cuando no hay tareas de renderizado pendientes.

---

## 1. Topología del Servicio en Zerops

- **Hostname:** `videoworker`
- **Base OS / Runtime:** `ubuntu/nodejs@22` (con FFmpeg, Playwright/Chromium y fuentes tipográficas instaladas)
- **Modo CPU:** `SHARED` (frugalidad extrema)
- **Memoria:** 512 MB base con auto-escalado
- **Variables de Entorno Inyectadas:** `$NATS_URL`, `$VALKEY_URL`, `$STORAGE_API_URL`, `$STORAGE_BUCKET_NAME`

---

## 2. Protocolo de Ciclo de Vida Efímero (Costo Cero)

### Fase 1: Aprovisionamiento On-Demand
Cuando se requiera generar o actualizar un lote de videos promocionales:

```bash
# Opción A: Mediante el importador de Zerops
zcli service import recipes/steps/08-video-worker.yaml

# Opción B: Mediante script de orquestación
./scripts/deploy-step.sh 8
```

El servicio `videoworker` arranca en segundos, detecta automáticamente las credenciales inyectadas por Zerops y se suscribe a la cola de trabajos.

### Fase 2: Ejecución y Validación de Entrega
1. El cliente (API, script de branding o ZCP) encola los trabajos de renderizado con los metadatos correspondientes (plantilla, textos, fuentes, audios y proporciones).
2. `videoworker` procesa cada trabajo de forma secuencial con control determinista.
3. Los archivos generados (`.mp4`) se publican directamente en el bucket de S3/Object Storage o se transfieren al directorio público de la aplicación web (`/apps/web/public/videos/`).
4. Se ejecuta una verificación física de descarga y reproducción (`HTTP 200`, códec H.264, audio AAC).

### Fase 3: Purga (Retorno a Costo Cero)
Una vez confirmada la integridad y persistencia de los videos entregables:

```bash
# Destruir el contenedor del worker en Zerops
zcli service delete videoworker
```

El clúster regresa a su topología base sin costos recurrentes por capacidad ociosa. Cuando se requiera un nuevo lote de videos en el futuro, el servicio se vuelve a importar en un único comando.
