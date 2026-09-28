# NATS JetStream Domain Event Streaming (v2.0)

## 1. Domain Event Hierarchy
Event subjects follow the sovereign dot notation:
- `order.created`: Emitted when checkout begins.
- `order.payment.settled`: Emitted when webhook cryptographically validates payment.
- `order.payment.failed`: Emitted when payment is rejected.
- `order.shipped`: Emitted when courier tracking guide is minted.
- `stock.depleted`: Emitted when a SKU reaches 0 available units.

---

## 2. JetStream Stream Declaration
```typescript
import { connect, JSONCodec } from "nats";

export async function setupJetStream(natsUrl: string) {
  const nc = await connect({ servers: natsUrl });
  const jsm = await nc.jetstreamManager();

  // Create stream ORDERS
  await jsm.streams.add({
    name: "ORDERS",
    subjects: ["order.*"],
    retention: "limits",
    max_age: 7 * 24 * 3600 * 1e9, // 7 days in nanoseconds
    storage: "file",
  });

  return nc;
}
```
