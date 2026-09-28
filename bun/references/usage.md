# Bun — Developer & Agent Usage Manual on Zerops

This manual provides production-tested specifications, base OS selection rules, the Bundling Bifurcation Law, native database querying with `Bun.sql`, and code recipes for developing with the **Zerops Managed Bun Runtime** (`type: bun@1.3.9` / `bun@latest`).

---

## 1. Runtime Architecture & Base OS Selection in `zerops.yaml`

Within the Zerops Managed Bun Runtime, the underlying container environment is configurable in `zerops.yaml`:

```
+-------------------------------------------------------------------------+
| Zerops Managed Bun Runtime (type: bun@1.3.9 / bun@latest)               |
+------------------------------------+------------------------------------+
| Option A: os: alpine (Default)     | Option B: os: ubuntu               |
| - musl libc (~5MB base)            | - glibc 2.39 (~100MB base)         |
| - Ultra-lean RAM (~25-40MB)        | - Full glibc C++ toolchain (GCC 14)|
| - Pure JS/TS web APIs (Elysia/Hono)| - Native C++ addons (sharp, canvas)|
| - Bundling: bun build -> ~150KB    | - Skip bundling: deployFiles: [./] |
+------------------------------------+------------------------------------+
```

### The Bundling Bifurcation Law
1. **Type A: Pure JavaScript/TypeScript Applications**
   * Dependencies: `elysia`, `hono`, `drizzle-orm`, `zod`, `@sinclair/typebox`, `pg`, `kysely`.
   * Strategy: Compile with `bun build src/index.ts --outfile dist/index.js --target bun` and deploy only `./dist` (`deployFiles: [dist]`).
   * Output: A standalone ~150KB file with all dependencies inlined, zero `node_modules` at runtime, sub-millisecond cold boot.
2. **Type B: Native C/C++ Addons**
   * Dependencies: `sharp`, `canvas`, `bcrypt` (npm), `mysql2`, `better-sqlite3`.
   * Strategy: **SKIP BUNDLING**. Inlining native C++ bindings silently corrupts the binary. Deploy the full repository (`deployFiles: [./]`) on `os: ubuntu` and launch with `start: bun src/index.ts`.

---

## 2. Built-in Database Clients (`Bun.sql` & `bun:sqlite`)

### A. Native PostgreSQL Client (`Bun.sql`)
```typescript
import { SQL } from 'bun';

// Automatic connection pooling and parameterization
export const sql = new SQL({
  url: process.env.DATABASE_URL || `postgresql://${process.env.DB_USER}:${process.env.DB_PASS}@${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.DB_NAME}`,
  max: 20,
  idleTimeout: 30
});

export async function getUserById(id: string) {
  const users = await sql`
    SELECT id, email, full_name, created_at
    FROM users
    WHERE id = ${id}
  `;
  return users[0] || null;
}
```

### B. High-Speed SQLite Client (`bun:sqlite`)
```typescript
import { Database } from 'bun:sqlite';

export const db = new Database('./data.db', { create: true });
db.exec('PRAGMA journal_mode = WAL;');

db.run(`
  CREATE TABLE IF NOT EXISTS cache (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    expires_at INTEGER NOT NULL
  ) STRICT;
`);

const setCacheStmt = db.prepare('INSERT OR REPLACE INTO cache VALUES (?, ?, ?)');
export function setCache(key: string, value: string, ttlSeconds: number) {
  setCacheStmt.run(key, value, Date.now() + ttlSeconds * 1000);
}
```

---

## 3. Native HTTP Server (`Bun.serve`) & Security Hashing

### High-Performance Native Server
```typescript
const PORT = parseInt(process.env.PORT || '3000', 10);

Bun.serve({
  port: PORT,
  hostname: '0.0.0.0', // Mandatory for Zerops L7 routing
  development: process.env.NODE_ENV !== 'production',

  async fetch(req) {
    const url = new URL(req.url);

    if (url.pathname === '/healthz') {
      return Response.json({ status: 'healthy', runtime: 'bun-native' });
    }

    if (url.pathname === '/api/hash' && req.method === 'POST') {
      const { password } = await req.json();
      const hash = await Bun.password.hash(password, { algorithm: 'argon2id', memoryCost: 65536, timeCost: 3 });
      return Response.json({ hash });
    }

    return new Response('Not Found', { status: 404 });
  }
});

console.log(`Bun server running on 0.0.0.0:${PORT}`);
```

---

## 4. Production Patterns & Verified Code Recipes

### Pattern 1: Elysia Framework Microservice
```typescript
import { Elysia, t } from 'elysia';

const app = new Elysia()
  .get('/healthz', () => ({ status: 'healthy', framework: 'elysia' }))
  .post('/api/users', ({ body }) => {
    return { success: true, user: body };
  }, {
    body: t.Object({
      email: t.String({ format: 'email' }),
      name: t.String({ minLength: 2 })
    })
  })
  .listen({
    port: parseInt(process.env.PORT || '3000', 10),
    hostname: '0.0.0.0'
  });

console.log(`Elysia listening on ${app.server?.hostname}:${app.server?.port}`);
```

### Pattern 2: Hono Framework Standalone Bundle (~150KB)
```typescript
import { Hono } from 'hono';

const app = new Hono();

app.get('/healthz', (c) => c.json({ status: 'healthy', framework: 'hono' }));
app.get('/api/info', (c) => c.json({ runtime: 'bun', version: Bun.version }));

export default {
  port: parseInt(process.env.PORT || '3000', 10),
  fetch: app.fetch
};
```

### Pattern 3: C++ Native Addon Service with `sharp` (`os: ubuntu`)
```typescript
import sharp from 'sharp';

const PORT = parseInt(process.env.PORT || '3000', 10);

Bun.serve({
  port: PORT,
  hostname: '0.0.0.0',
  async fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === '/render/banner') {
      const banner = await sharp({
        create: {
          width: 800,
          height: 200,
          channels: 4,
          background: { r: 99, g: 102, b: 241, alpha: 1 }
        }
      }).png().toBuffer();

      return new Response(banner, {
        headers: { 'Content-Type': 'image/png' }
      });
    }
    return Response.json({ status: 'healthy', base: 'ubuntu@24' });
  }
});
```

### Pattern 4: Atomic Database Migrations with `zsc execOnce`
In `zerops.yaml`:
```yaml
run:
  initCommands:
    - zsc execOnce ${appVersionId} --retryUntilSuccessful -- bun dist/migrate.js
```

Migration runner (`migrate.ts`):
```typescript
import { sql } from './db.js';

async function runMigrations() {
  console.log('Running atomic migration via zsc execOnce on Bun...');
  await sql`
    CREATE TABLE IF NOT EXISTS migrations (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
  `;
  console.log('Migrations completed successfully');
}

runMigrations().catch((err) => {
  console.error('Migration failed:', err);
  process.exit(1);
});
```

### Pattern 5: Interactive SSH Development Setup with `noop`
```yaml
zerops:
  - setup: dev
    build:
      base: bun@1.3.9
      envVariables:
        BUN_INSTALL: ./.bun
      buildCommands:
        - bun install
      deployFiles:
        - ./
      cache:
        - node_modules
        - .bun/install/cache
    run:
      base: bun@1.3.9
      ports:
        - port: 3000
          httpSupport: true
      start: zsc noop --silent
```

---

## 5. Anti-Patterns & Gotchas in Zerops

| Anti-Pattern | Why it Fails | Correct Solution |
|---|---|---|
| Bundling C++ native addons (`sharp`, `mysql2`) | Inlining native `.node` bindings corrupts binary or fails at runtime | Skip bundling: `deployFiles: [./]`, `start: bun src/index.ts` on `os: ubuntu`. |
| Omitting `BUN_INSTALL: ./.bun` | Bun caches packages to `~/.bun` which is outside `/build/source/` and lost | Redirect `BUN_INSTALL: ./.bun` and cache `.bun/install/cache`. |
| Using `npx` in build/runtime | `npx` may not resolve dependencies correctly under Bun | Always use `bunx`. |
| Binding server to `127.0.0.1` | Zerops L7 load balancer cannot route traffic $\to$ 502 error | Always bind HTTP servers to `0.0.0.0`. |
| Hardcoding `verticalAutoscaling` | Overrides Zerops' native dynamic elastic scaling | Omit `verticalAutoscaling` and allow Zerops to auto-scale. |
