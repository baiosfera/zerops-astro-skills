# CoHaLo Reference Manual: Harness Engineering, Guides & Sensors

## 1. Concepto Fundamental
La capa de **Harness Engineering** dota al agente de manos mecánicas y sentidos de verificación. Un arnés robusto encapsula la ejecución del agente mediante **Guías de Entrada (Feedforward)** que previenen errores antes de ejecutar acciones en la infraestructura, y **Sensores de Salida (Feedback)** que atestiguan el éxito o capturan fallos estructurados.

---

## 2. Feedforward Guides (Guías de Entrada)

Las guías de entrada son validadores programáticos deterministas que bloquean la ejecución si los parámetros no satisfacen los contratos de plataforma:

1. **Validador de Plataforma `zcp-validate`**:
   - `zcp-validate hostname <name>`: Valida hostnames alfanuméricos estrictos en minúsculas (a-z0-9), máximo 25 caracteres, sin guiones ni caracteres especiales.
   - `zcp-validate os <ubuntu|alpine>`: Valida la selección explícita del SO base.
   - `zcp-validate resolution <EXISTS|CREATE|SHARED>`: Valida dependencias de infraestructura.
   - `zcp-validate db-variant <name:single|name:ha>`: Valida variantes inmutables de bases de datos administradas.
   - `zcp-validate scaling <docker|native> <minCpu> <maxCpu> <minRam> <maxRam>`: Valida que Docker VM use recursos fijos (`min == max`) y los runtimes nativos usen autoscaling elástico (`min < max`).
   - `zcp-validate yaml <import.yaml>`: Valida manifiestos completos de Zerops.
2. **Registro de Servicios y Esquemas REST (`rest_registry.json`)**:
   - Valida endpoints, headers requeridos y payloads antes de invocar APIs externas.
3. **Plantillas Fractales de Skills (`docu/references/templates.md`)**:
   - Asegura que todo nuevo artefacto compile sus propios arneses de ejecución.
4. **Structured Outputs & Tipado Estricto**:
   - Uso de esquemas Pydantic / Zod y validación estricta para garantizar outputs predecibles sin parsing frágil por regex.

---

## 3. Feedback Sensors (Sensores de Salida)

Los sensores de salida proporcionan verificación objetiva y sin ambigüedades:

1. **Atestación HTTP (`zerops_verify`)**:
   - Comprobación de status code `200 OK` en endpoints desplegados.
2. **Sensores de Procesos y Tests**:
   - Códigos de salida (`exit code 0`).
   - Linters estáticos y suites de pruebas unitarias/E2E ejecutadas en el contenedor destino vía SSH.
3. **Diagnóstico Estructurado**:
   - En caso de fallo, el sensor recopila logs y trazas de error sin conjeturas para alimentar el bucle de auto-corrección.

---

## 4. Process Hygiene & Filesystem Shield (FS Shield)

1. **Timeouts Estrictos en Comandos**:
   - Todo comando exploratorio, de búsqueda o llamadas a terminal DEBE ejecutarse con límites de tiempo (`timeout 5s ...`, `timeout 10s ...`, `timeout 15s ...`).
2. **Sincronización Máxima de Espera (`WaitMsBeforeAsync: 10000`)**:
   - Al invocar herramientas de terminal, configurar siempre `10000 ms` para prevenir que procesos síncronos queden detached en background innecesariamente.
3. **Invariante de Cero Tareas Huérfanas (Zero Orphaned Tasks)**:
   - Al concluir cualquier acción, listar y terminar inmediatamente tareas rezagadas con `manage_task action="kill"`.
4. **Protección del Filesystem (FS Shield)**:
   - Operaciones de borrado requieren rutas absolutas explícitas de archivo, limitando el uso de comodines destructivos en raíces de `/mnt/`.
5. **Servidores de Desarrollo Persistentes**:
   - Watchers y procesos continuos se lanzan exclusivamente mediante `zerops_dev_server`.

---

## 5. Arneses de Tool Calling & Optimización de Ejecución

1. **Pre-Computación Reflexiva (Tool Reflection):**
   - Declarar internamente el motivo de la llamada, qué datos se esperan y cómo aportan a la solución antes de invocar herramientas.
2. **Paralelismo Inteligente:**
   - Ejecutar tool calls independientes en un solo lote paralelo.
   - Ejecutar tool calls dependientes en secuencia estricta.
3. **Poda de Herramientas (Catalog Pruning):**
   - Exponer únicamente el subconjunto de herramientas pertinentes para la tarea activa para evitar la degradación por sobrecarga de catálogo.
