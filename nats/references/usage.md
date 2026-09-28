# NATS Server 2.12 — Developer & Architecture Usage Manual on Zerops

This manual provides production-tested specifications, Core NATS Request-Reply RPC patterns, JetStream 2.12 durability, Key-Value and Object Store implementations, and polyglot client recipes for **NATS Server 2.12** on Zerops.

---

## 1. Core NATS Messaging Primitives

### A. Sub-Millisecond Request-Reply RPC (<0.3ms P99)
NATS implements request-reply natively at the protocol level using ephemeral inbox subjects (`_INBOX.>`):

```typescript
import { connect, JSONCodec } from 'nats';

const nc = await connect({
  servers: `${process.env.NATS_HOST}:${process.env.NATS_PORT}`,
  user: process.env.NATS_USER,
  pass: process.env.NATS_PASS
});

const jc = JSONCodec();

// RPC Server
const sub = nc.subscribe('orders.calculate_total', { queue: 'calc_workers' });
(async () => {
  for await (const msg of sub) {
    const data = jc.decode(msg.data) as { items: number[]; tax: number };
    const total = data.items.reduce((acc, curr) => acc + curr, 0) * (1 + data.tax);
    msg.respond(jc.encode({ total, calculatedAt: Date.now() }));
  }
})();

// RPC Client with Mandatory Timeout
try {
  const response = await nc.request(
    'orders.calculate_total',
    jc.encode({ items: [100, 250, 50], tax: 0.21 }),
    { timeout: 2000 }
  );
  console.log('Calculation Result:', jc.decode(response.data));
} catch (err) {
  console.error('RPC Request Timeout or Failure:', err);
}
```

### B. Queue Groups Load Balancing
Queue groups distribute incoming messages across active worker containers without an external load balancer:
```typescript
// Load balanced across all running app containers
const sub = nc.subscribe('payments.process', { queue: 'payment_processors' });
```

---

## 2. JetStream 2.12 Persistence & Pull Consumers

### A. Stream Provisioning & Deduplication (`Nats-Msg-Id`)
```typescript
import { connect, JSONCodec, headers } from 'nats';

const nc = await connect({ servers: process.env.NATS_URL });
const js = nc.jetstream();
const jsm = await nc.jetstreamManager();

// Provision Stream
await jsm.streams.add({
  name: 'ORDERS',
  subjects: ['orders.>'],
  storage: 'file', // Persistent storage
  num_replicas: 1 // In :ha clusters, use 3
});

// Idempotent Publishing with Nats-Msg-Id Header
const h = headers();
h.set('Nats-Msg-Id', 'order_evt_unique_109283'); // Native deduplication key

await js.publish('orders.created', jc.encode({ orderId: '109283', amount: 99.5 }), { headers: h });
```

### B. Durable Pull Consumer with Poison Pill Defense (`msg.term()`)
```typescript
const consumer = await js.consumers.get('ORDERS', 'order_processor');
const messages = await consumer.fetch({ max_messages: 50, expires: 5000 });

for await (const msg of messages) {
  try {
    // Process business logic
    console.log('Processing order message:', msg.seq);
    msg.ack();
  } catch (error) {
    if (msg.info.deliveryCount >= 5) {
      console.error(`Poison pill detected on message ${msg.seq}, terminating.`);
      msg.term(); // Terminate delivery to prevent infinite loops
    } else {
      msg.nak(1000); // Negative acknowledge with 1s backoff
    }
  }
}
```

---

## 3. Key-Value (KV) Store & Object Store

### A. Key-Value Store with TTL
```typescript
const js = nc.jetstream();
const kv = await js.views.kv('app_config', { ttl: 3600000 }); // 1 hour TTL

// Put and Get
await kv.put('features.dark_mode', JSON.stringify({ enabled: true }));
const entry = await kv.get('features.dark_mode');
console.log('Value:', entry?.string());

// Watch for changes in real-time
const watch = await kv.watch();
(async () => {
  for await (const e of watch) {
    console.log(`Key ${e.key} updated:`, e.string());
  }
})();
```

### B. Object Store (Binary Assets)
```typescript
const os = await js.views.os('invoice_documents');
await os.putBlob({ name: 'invoice_109283.pdf' }, new Uint8Array([0x25, 0x50, 0x44, 0x46]));
const file = await os.getBlob('invoice_109283.pdf');
```

---

## 4. Production Patterns & Verified Polyglot Recipes

### Pattern 1: Python `nats-py` FastAPI Integration
```python
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
import nats

nc = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global nc
    nc = await nats.connect(
        servers=[f"{os.getenv('NATS_HOST', 'queue')}:{os.getenv('NATS_PORT', '4222')}"],
        user=os.getenv("NATS_USER", "zerops"),
        password=os.getenv("NATS_PASS")
    )
    yield
    await nc.drain()

app = FastAPI(lifespan=lifespan)

@app.post("/events/publish")
async def publish_event(payload: dict):
    await nc.publish("events.incoming", str(payload).encode())
    return {"status": "published"}
```

### Pattern 2: Go `nats.go` High-Throughput Worker
```go
package main

import (
	"log"
	"os"
	"github.com/nats-io/nats.go"
)

func main() {
	nc, err := nats.Connect(os.Getenv("NATS_URL"))
	if err != nil {
		log.Fatalf("Failed to connect to NATS: %v", err)
	}
	defer nc.Drain()

	sub, err := nc.QueueSubscribe("tasks.render", "render_pool", func(msg *nats.Msg) {
		log.Printf("Received task: %s", string(msg.Data))
		msg.Respond([]byte("Render completed"))
	})
	if err != nil {
		log.Fatal(err)
	}
	defer sub.Unsubscribe()

	select {}
}
```

---

## 5. Anti-Patterns & Gotchas in Zerops

| Anti-Pattern | Why it Fails | Correct Solution |
|---|---|---|
| Hand-rolling URLs with embedded auth | Produces double-auth and `Authorization Violation` error | Pass `servers`, `user`, `pass` separately or use `${queue_connectionString}`. |
| Omitting timeouts on `nc.request()` | Network drops cause client thread to hang indefinitely | Always supply an explicit timeout option (e.g. `{ timeout: 2000 }`). |
| Missing `msg.term()` on poison pills | Unprocessable messages retry infinitely, exhausting CPU | Terminate message with `msg.term()` when `deliveryCount >= 5`. |
| Hardcoding `verticalAutoscaling` | Overrides native dynamic autoscaling on Incus LXC | Omit `verticalAutoscaling` and allow Zerops to auto-scale. |
| Using internal TLS on port 4222 | Internal communication is plaintext over encrypted VXLAN | Connect via plaintext on port 4222; TLS is only used on external ingress. |
