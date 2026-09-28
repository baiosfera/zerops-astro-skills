# Valkey 7.2 — Developer & Architecture Usage Manual on Zerops

This manual provides production-tested specifications, Cache-Aside patterns, sliding-window rate limiting via atomic Lua scripts, BullMQ job queues, and polyglot client recipes for **Valkey 7.2** on Zerops.

---

## 1. Core Valkey Patterns & RESP3 Protocol

### A. Resilient Cache-Aside Pattern (TypeScript with `ioredis`)
```typescript
import Redis from 'ioredis';

export const cache = new Redis(process.env.REDIS_URL || 'redis://:password@cache:6379', {
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  retryStrategy(times) {
    return Math.min(times * 100, 3000);
  }
});

export async function getOrSetCache<T>(
  key: string,
  ttlSeconds: number,
  fetchFn: () => Promise<T>
): Promise<T> {
  const cached = await cache.get(key);
  if (cached) {
    return JSON.parse(cached) as T;
  }
  const freshData = await fetchFn();
  await cache.set(key, JSON.stringify(freshData), 'EX', ttlSeconds);
  return freshData;
}
```

### B. Atomic Sliding-Window Rate Limiter (Lua Script)
```typescript
const RATE_LIMIT_LUA = `
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

local clearBefore = now - window
redis.call('ZREMRANGEBYSCORE', key, 0, clearBefore)
local currentRequests = redis.call('ZCARD', key)

if currentRequests < limit then
  redis.call('ZADD', key, now, now)
  redis.call('EXPIRE', key, math.ceil(window / 1000))
  return 1
else
  return 0
end
`;

export async function checkRateLimit(ip: string, limit: number, windowMs: number): Promise<boolean> {
  const key = `ratelimit:${ip}`;
  const allowed = await cache.eval(RATE_LIMIT_LUA, 1, key, Date.now(), windowMs, limit);
  return allowed === 1;
}
```

---

## 2. BullMQ Job Queue Engine (Node.js & Bun)

When building background queues with BullMQ over Valkey 7.2:

```typescript
import { Queue, Worker, Job } from 'bullmq';

const connection = {
  host: process.env.REDIS_HOST || 'cache',
  port: parseInt(process.env.REDIS_PORT || '6379', 10),
  password: process.env.REDIS_PASSWORD
};

// Queue Definition
export const emailQueue = new Queue('emails', {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 1000
    },
    removeOnComplete: 1000,
    removeOnFail: 5000
  }
});

// Enqueue Job
export async function queueEmail(to: string, template: string) {
  await emailQueue.add('send_welcome', { to, template }, { priority: 1 });
}

// Worker Definition
export const emailWorker = new Worker(
  'emails',
  async (job: Job) => {
    console.log(`Processing email job ${job.id} for ${job.data.to}...`);
    // Business logic
    return { sent: true, at: Date.now() };
  },
  { connection, concurrency: 10 }
);
```

---

## 3. Production Patterns & Verified Polyglot Recipes

### Pattern 1: Python `redis-py` Connection Pool
```python
import os
import redis.asyncio as aioredis

valkey_pool = aioredis.ConnectionPool.from_url(
    os.getenv("REDIS_URL", "redis://:password@cache:6379"),
    max_connections=20,
    decode_responses=True
)

async def get_valkey():
    return aioredis.Redis(connection_pool=valkey_pool)
```

### Pattern 2: Go `go-redis/v9` Connection
```go
package cache

import (
	"context"
	"os"
	"github.com/redis/go-redis/v9"
)

var RDB *redis.Client

func InitValkey() {
	opt, err := redis.ParseURL(os.Getenv("REDIS_URL"))
	if err != nil {
		panic(err)
	}
	opt.PoolSize = 25
	RDB = redis.NewClient(opt)
}
```

### Pattern 3: Session Management in Express / Fastify
```typescript
import session from 'express-session';
import RedisStore from 'connect-redis';

export const sessionMiddleware = session({
  store: new RedisStore({ client: cache, prefix: 'sess:' }),
  secret: process.env.SESSION_SECRET || 'super-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 86400000 // 1 day
  }
});
```

---

## 4. Anti-Patterns & Gotchas in Zerops

| Anti-Pattern | Why it Fails | Correct Solution |
|---|---|---|
| Attempting unauthenticated connection | Valkey in Zerops enforces authentication $\to$ `NOAUTH` error | Supply `${cache_password}` or connect via `${cache_connectionString}`. |
| Provisioning `valkey@8` | Version 8 fails platform import on Zerops | Always target `valkey:single@7.2` or `valkey:ha@7.2`. |
| Using Valkey for general pub/sub messaging | High-volume message broadcasting causes memory spikes | Use `nats@2.12` for microservice events and pub/sub. |
| Hardcoding `verticalAutoscaling` | Overrides native dynamic autoscaling configured by `profile:` | Use `profile:` (`hobby`, `staging`, `production`) and allow Zerops to auto-scale. |
| Modifying the internal `zps` user | Breaks Zerops platform telemetry and monitoring | Never alter or drop internal system users. |
