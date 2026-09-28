# Automation Engine: Topología & Infraestructura Zerops (v1.0)

> **SSoT Reference Document:** `.agents/skills/automation-engine/references/infra.md`  
> **Ámbito:** Despliegue de NATS Server 2.12 en Zerops Incus LXC, puertos de comunicación, integración con Valkey 7.2 y Directus 11+.

---

## 1. Topología del Bus de Eventos en Zerops Incus LXC

El clúster de automatización corre íntegramente sobre la red privada de Zerops con un consumo inferior a 250MB de RAM total:

```mermaid
graph TD
    subgraph Zerops_Incus_Network["Red Privada del Proyecto Zerops"]
        NatsServer["Servicio NATS Server 2.12 (Incus LXC)<br/>• JetStream Storage: File / Storage Volume<br/>• Puertos: 4222 (Cliente), 8222 (Monitoring)"]
        
        Directus["Servicio Directus 11+ (Headless CRM/CMS)<br/>• Flows In-Process Engine<br/>• Puerto: 8055"]
        
        Valkey["Servicio Valkey 7.2<br/>• Backend de Colas BullMQ & DLQ<br/>• Puerto: 6379"]
        
        Workers["Servicio Background Workers (Node 24)<br/>• Consumidores Pull NATS & Workers BullMQ<br/>• Puerto: 3006"]
    end

    Directus -->|POST CloudEvents 1.0| NatsServer
    NatsServer -->|Pull Consumer (<1ms)| Workers
    Workers -->|Encolado de Tareas Pesadas| Valkey
```

---

## 2. Required Environment Variables

```ini
# ============================================================================
# NATS JETSTREAM 2.12
# ============================================================================
NATS_URL="nats://nats:4222"
NATS_CLUSTER_ID="gentle-cluster"
NATS_MONITORING_URL="http://nats:8222"

# ============================================================================
# VALKEY 7.2 & BULLMQ
# ============================================================================
VALKEY_HOST="valkey"
VALKEY_PORT="6379"
VALKEY_CONNECTION_STRING="redis://valkey:6379"

# ============================================================================
# DIRECTUS 11+ FLOWS
# ============================================================================
DIRECTUS_URL="http://directus:8055"
DIRECTUS_SERVER_TOKEN="directus_admin_token_2026"
```
