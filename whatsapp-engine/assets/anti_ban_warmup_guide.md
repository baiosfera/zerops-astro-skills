# Universal WhatsApp Anti-Ban & Number Warmup Protocol (v2.0)

---

## 1. Gradual Warmup Schedule (Multi-Tier Volume Ramp)

| Period | Daily Volume Budget | Interaction Type |
|---|---|---|
| **Days 1 to 3** | 0 automated messages | Manual mobile usage, personal conversations, join 2-3 active groups, receive incoming calls. |
| **Days 4 to 7** | 20 – 40 messages / day | Strictly inbound responses to customer-initiated conversations or high-intent leads. |
| **Days 8 to 14** | 80 – 120 messages / day | Randomized dispatch delays (2s – 5s) and realistic `composing` typing state simulation. |
| **Maturity (>14 Days)** | 150 – 350 conversations / day | Regular production traffic with AI conversational agents and CRM automations. |

---

## 2. Technical Anti-Ban Invariants
1. **Presence Simulation**: Always emit `composing` (typing state) for 1.5s – 3s before sending text messages.
2. **Native Voice Notes**: Send voice messages using standard Opus audio (`audio/ogg; codecs=opus`) while simulating `recording` state.
3. **Automated Opt-Out Handlers**: Immediately pause automation and unsubscribe phone numbers if the user sends opt-out keywords (`STOP`, `UNSUBSCRIBE`, `CANCEL`, `QUIT`, `BAJA`, `SALIR`, `NO MAS`).
4. **Sliding Window Rate Limiting**: Limit outbound message bursts using Valkey token buckets (maximum 15 messages/minute per instance).
5. **Session Monitoring**: Track socket disconnection frequency. If 2 consecutive disconnections occur, cycle instance state cleanly.
