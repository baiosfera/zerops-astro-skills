# Protocolo de Ciclo de Vida Efímero (Costo Cero)

El servicio `videoworker` se rige por el principio de **efimeridad soberana**: no consume presupuesto de infraestructura cuando no hay tareas de renderizado pendientes.

## 1. Fase de Aprovisionamiento (On-Demand)

Cuando se requiera generar o actualizar un lote de videos promocionales:

```bash
# Opción A: Mediante el orquestador de pasos
./scripts/deploy-step.sh 8

# Opción B: Mediante zcli
zcli service import recipes/steps/08-video-worker.yaml
```

El servicio `videoworker` (`ubuntu/nodejs@22`) arranca en segundos, detecta automáticamente las credenciales de `$NATS_URL` y `$VALKEY_URL` inyectadas por Zerops y se suscribe a la cola de trabajos.

## 2. Fase de Ejecución y Entrega

1. El cliente (API, script de branding o ZCP) encola los trabajos de renderizado con los metadatos correspondientes (plantilla, textos, fuentes, audios y proporciones).
2. `videoworker` procesa cada trabajo de forma secuencial con control determinista.
3. Los archivos generados (`.mp4`) se publican directamente en el bucket de S3/Object Storage o se transfieren al directorio público de la aplicación web (`/apps/web/public/videos/`).
4. Se ejecuta una verificación física de descarga y reproducción (`HTTP 200`, códec H.264, audio AAC).

## 3. Fase de Purga (Retorno a Costo Cero)

Una vez confirmada la integridad de los entregables:

```bash
# Eliminar el contenedor del worker en Zerops
zcli service delete videoworker
```

El clúster regresa a su topología base sin costos recurrentes por capacidad ociosa. Cuando se requiera un nuevo lote de videos en el futuro, el Hito 8 se vuelve a importar en un único comando.
