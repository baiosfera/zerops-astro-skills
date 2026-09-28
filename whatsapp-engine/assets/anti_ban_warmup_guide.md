# Protocolo Anti-Bloqueo (Anti-Ban) para Números WhatsApp en Colombia (+57)

---

## 1. Fase de Calentamiento Gradual (Warm-up)

| Período | Volumen Diario Recomendado | Tipo de Interacción |
|---|---|---|
| **Días 1 a 3** | 0 automatizados | Uso manual en celular, chats con amigos/familiares, unirse a 2-3 grupos reales, recibir llamadas. |
| **Días 4 a 7** | 20 – 40 mensajes/día | Solo respuestas a clientes que escriban primero (inbound) o clientes altamente calificados. |
| **Días 8 a 14** | 80 – 120 mensajes/día | Mensajes con delays aleatorios (2s a 5s) y simulación de escritura `composing`. |
| **Madurez (>14 Días)** | 150 – 250 conversaciones/día | Operación regular con Typebot o agentes de IA. |

---

## 2. Invariantes Técnicos Anti-Ban
1. **Simulación de Presencia:** Emitir siempre `composing` durante 1.5s - 3s antes de enviar un mensaje de texto.
2. **Notas de Voz Nativas:** Usar siempre `sendWhatsAppAudio` con `audio/ogg; codecs=opus` simulando `recording`.
3. **Manejo de Opt-Out:** Pausar inmediatamente si el usuario escribe `SALIR`, `CANCELAR` o `NO MAS`.
