# Node.js — Developer & Agent Usage Manual on Zerops

This manual provides production-tested specifications, base OS selection rules, native TypeScript execution, database pooling patterns, and code recipes for developing with the **Zerops Managed Node.js Runtime** (`type: nodejs@22` / `nodejs@24`).

---

## 1. Base OS Selection Strategy in `zerops.yaml`

Within the Zerops Managed Node.js Runtime, the underlying OS base is configurable in `zerops.yaml`:

```
+-------------------------------------------------------------------------+
| Zerops Managed Node.js Runtime (type: nodejs@22 / nodejs@24)            |
+------------------------------------+------------------------------------+
| Option A: os: alpine (Default)     | Option B: os: ubuntu               |
| - musl libc (~5MB base)            | - glibc 2.39 (~100MB base)         |
| - Ultra-lean RAM (~35-50MB)        | - Full glibc C++ toolchain (GCC 14)|
| - Pure JS/TS web APIs              | - Native C++ addons (sharp, canvas)|
| - Ideal for Fastify, Express, Nest | - Mandatory for node-gyp builds    |
+------------------------------------+------------------------------------+
```

### When to Select `os: alpine` (Default)
* Standard REST/GraphQL/gRPC web services (`Fastify`, `Express`, `NestJS`, `Hono`, `Astro`, `Remix`).
* Pure JavaScript/TypeScript database clients (`pg`, `postgres`, `drizzle-orm`, `@prisma/client` with pure JS engine).
* Web applications without compiled C++ binary addons.

### When to Select `os: ubuntu`
* Image and document manipulation using native C/C++ libraries (`sharp`, `libvips-dev`, `canvas`, `pdfkit`).
* Native crypto or security addons (`bcrypt` native, `sodium-native`).
* Native SQLite bindings requiring external C headers (`better-sqlite3`).

---

## 2. Native TypeScript Execution (Type Stripping)

Node.js 22+ and 24 LTS execute TypeScript files directly without a pre-compilation step via the V8 type-stripping engine:

```bash
# Direct TypeScript execution in development or lightweight runtimes
node --experimental-strip-types src/index.ts

# In tsconfig.json:
{
  "compilerOptions": {
    "target": "ES2024",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "strict": true
  }
}
```

---

## 3. Native Database (`node:sqlite`) & Testing (`node:test`)

### A. Built-in Synchronous SQLite (`node:sqlite`)
```typescript
import { DatabaseSync } from 'node:sqlite';

export const db = new DatabaseSync('./data.db');

db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    created_at INTEGER NOT NULL
  ) STRICT;
`);

const insertUser = db.prepare('INSERT INTO users (email, created_at) VALUES (?, ?)');
export function createUser(email: string) {
  const result = insertUser.run(email, Date.now());
  return { id: result.lastInsertRowid, email };
}
```

### B. Built-in Testing Engine (`node:test`)
```typescript
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

describe('User API Validation', () => {
  it('should validate email structure', () => {
    assert.equal(1 + 1, 2);
  });
});
```

---

## 4. Production Patterns & Verified Code Recipes

### Pattern 1: High-Performance Fastify Service
```typescript
import Fastify from 'fastify';

const fastify = Fastify({
  logger: true,
  trustProxy: true // Mandatory for Zerops L7 SSL termination
});

const PORT = parseInt(process.env.PORT || '3000', 10);

fastify.get('/healthz', async (_req, reply) => {
  return reply.code(200).send({ status: 'healthy', runtime: 'nodejs-zerops-native' });
});

fastify.get('/api/data', async (_req, reply) => {
  return reply.code(200).send({ message: 'Hello from Zerops Node.js Runtime' });
});

try {
  await fastify.listen({ port: PORT, host: '0.0.0.0' });
  console.log(`Fastify server listening on port ${PORT}`);
} catch (err) {
  fastify.log.error(err);
  process.exit(1);
}
```

### Pattern 2: Resilient PostgreSQL Pooling with `pg`
```typescript
import { Pool } from 'pg';

export const pool = new Pool({
  host: process.env.DB_HOST || 'db',
  port: parseInt(process.env.DB_PORT || '5432', 10),
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME || 'db',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
  ssl: false
});

pool.on('error', (err) => {
  console.error('Unexpected error on idle PostgreSQL client', err);
});
```

### Pattern 3: C++ Native Addon Service with `sharp` (`os: ubuntu`)
```typescript
import express, { Request, Response } from 'express';
import sharp from 'sharp';

const app = express();
app.set('trust proxy', true);
const PORT = process.env.PORT || 3000;

app.get('/render/avatar', async (_req: Request, res: Response) => {
  const avatarBuffer = await sharp({
    create: {
      width: 200,
      height: 200,
      channels: 4,
      background: { r: 16, g: 185, b: 129, alpha: 1 }
    }
  }).png().toBuffer();

  res.setHeader('Content-Type', 'image/png');
  res.send(avatarBuffer);
});

app.get('/healthz', (_req: Request, res: Response) => {
  res.status(200).json({ status: 'healthy', base: 'ubuntu@24', addon: 'sharp' });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Sharp worker listening on 0.0.0.0:${PORT}`);
});
```

### Pattern 4: Atomic Database Migrations Binary with Prisma / Drizzle
In `zerops.yaml`:
```yaml
run:
  initCommands:
    - zsc execOnce ${appVersionId} --retryUntilSuccessful -- node dist/migrate.js
```

Migration runner (`src/migrate.ts`):
```typescript
import { pool } from './db.js';

async function migrate() {
  console.log('Starting atomic schema migration via zsc execOnce...');
  const client = await pool.connect();
  try {
    await client.query(`
      CREATE TABLE IF NOT EXISTS schema_version (
        version INT PRIMARY KEY,
        applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
      );
    `);
    console.log('Schema migration completed successfully');
  } finally {
    client.release();
    await pool.end();
  }
}

migrate().catch((err) => {
  console.error('Migration failed:', err);
  process.exit(1);
});
```

### Pattern 5: Interactive SSH Development Setup with `noop`
```yaml
zerops:
  - setup: dev
    build:
      base: nodejs@22
      buildCommands:
        - npm install
      deployFiles:
        - ./
      cache:
        - node_modules
    run:
      base: nodejs@22
      ports:
        - port: 3000
          httpSupport: true
      start: zsc noop --silent
```

---

## 5. Anti-Patterns & Gotchas in Zerops

| Anti-Pattern | Why it Fails | Correct Solution |
|---|---|---|
| Compiling `sharp` / `better-sqlite3` on `os: alpine` | Fails dynamic linking or requires slow source compile | Set `os: ubuntu` and install `build-essential libvips-dev` in prepareCommands. |
| Binding server to `127.0.0.1` or `localhost` | L7 load balancer cannot route traffic to container $\to$ 502 error | Always bind HTTP servers to `0.0.0.0`. |
| Deploying `devDependencies` to production | Bloats runtime container RAM and increases cold boot duration | Always execute `npm prune --omit=dev` before packaging. |
| Omitting `npm_config_cache: .npm-cache` | npm cache is discarded on build container exit, slowing builds | Set `npm_config_cache: .npm-cache` in `build.envVariables` + `cache: [.npm-cache]`. |
| Hardcoding `verticalAutoscaling` | Overrides Zerops' native dynamic elastic scaling | Omit `verticalAutoscaling` and allow Zerops to auto-scale. |
