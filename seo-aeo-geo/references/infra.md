# SEO, AEO & CDN Infrastructure Manual in Zerops (v1.0)

> **Documento Normativo SSoT:** Especificación de infraestructura para entrega ultrarrápida, cabeceras HTTP de compresión, Edge Caching en Zerops CDN global y purgado programático.

---

## 1. Zerops Global CDN & Edge Caching

- **Infraestructura**: CDN Anycast distribuida en 6 regiones globales con baja latencia perimetral.
- **TTL de Caché en CDN**: TTL fijo de **30 días** en el edge de Zerops.
- **Control del Navegador**: Se define mediante la cabecera HTTP `Cache-Control`.
- **Purgado Programático de CDN**:
  ```bash
  # Purgar todo el dominio
  zsc cdn purge <dominio.com>

  # Purgar una ruta específica
  zsc cdn purge <dominio.com> /blog/*
  ```

---

## 2. Cabeceras HTTP de Alto Rendimiento

### Configuración Recomendada para Páginas SSR y Activos Estáticos:
```http
Cache-Control: public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800
X-Robots-Tag: max-snippet:-1, max-image-preview:large, max-video-preview:-1
Content-Type: text/html; charset=utf-8
Vary: Accept-Encoding
```

### Compresión L7 en Zerops:
El balanceador L7 de Zerops negocia automáticamente **Brotli (`br`)** y **Gzip (`gzip`)** para todos los contenidos de texto (`text/html`, `application/json`, `application/ld+json`, `text/plain`).

---

## 3. Arnés de Ejecución y Proceso (Fractal CoHaLo)

- **Timeouts**: Comandos con `timeout 10s`.
- **Espera Síncrona**: `WaitMsBeforeAsync: 10000`.
- **Sensores Físicos**: Validación de Rich Results con Google Rich Results API y validación de `llms.txt` HTTP 200.
- **Circuit Breaker**: Máximo 2 reintentos antes de escalación.
