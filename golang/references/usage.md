# Golang — Developer & Agent Usage Manual on Zerops

This manual provides production-tested specifications, base OS selection rules, database pooling patterns, and code recipes for developing with the **Zerops Managed Go Runtime** (`type: go@...` / `golang@latest`).

---

## 1. Base OS Selection Strategy in `zerops.yaml`

Within the Zerops Managed Go Runtime, the underlying OS base is configurable in `zerops.yaml`:

```
+-------------------------------------------------------------------------+
| Zerops Managed Go Runtime (type: go@1.22 / golang@latest)               |
+------------------------------------+------------------------------------+
| Option A: os: alpine (Default)     | Option B: os: ubuntu               |
| - musl libc (~5MB base)            | - glibc 2.39 (~100MB base)         |
| - Pure Go: CGO_ENABLED=0           | - CGO-enabled: CGO_ENABLED=1       |
| - Netgo pure Go DNS resolver       | - Dynamic C libraries (libvips)    |
| - Ultra-low RAM (~10-20MB)         | - Full Ubuntu toolchain            |
| - Ideal for 95% of web APIs        | - Needed for C CGO bindings        |
+------------------------------------+------------------------------------+
```

### When to Select `os: alpine` (Default)
* Standard REST/gRPC microservices.
* Pure Go database drivers (`jackc/pgx/v5`, `go-redis/v9`, `nats-io/nats.go`).
* Web frameworks (`chi`, `fiber`, `gin`, `echo`, standard `net/http`).
* Full static compilation: `CGO_ENABLED="0"`.

### When to Select `os: ubuntu`
* Binding native C/C++ libraries via CGO (`libvips-dev`, `libsqlite3-dev`, `librdkafka-dev`).
* Applications requiring glibc-specific system libraries.
* Toolchain requires Ubuntu `apt-get` packages in `prepareCommands`.

---

## 2. Environment Variables & Secret Ingestion

Zerops automatically generates and injects environment variables for managed services. Reference them in `zerops.yaml` using the `${hostname_key}` syntax:

```yaml
run:
  envVariables:
    PORT: "8080"
    DB_HOST: ${db_hostname}
    DB_PORT: ${db_port}
    DB_USER: ${db_user}
    DB_PASS: ${db_password}
    DB_NAME: db
    CACHE_HOST: ${cache_hostname}
    CACHE_PORT: ${cache_port}
```

---

## 3. Production Patterns & Verified Code Recipes

### Pattern 1: High-Concurrency REST API with Chi & Graceful Shutdown
```go
package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	r := chi.NewRouter()
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Timeout(60 * time.Second))

	r.Get("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, `{"status":"healthy","runtime":"go-zerops-native"}`)
	})

	server := &http.Server{
		Addr:         ":" + port,
		Handler:      r,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  120 * time.Second,
	}

	// Graceful shutdown listener
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)

	go func() {
		log.Printf("Zerops Go server listening on port %s", port)
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server error: %v", err)
		}
	}()

	<-stop
	log.Println("Shutting down server gracefully...")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}
	log.Println("Server exiting")
}
```

### Pattern 2: Resilient PostgreSQL Pooling with `jackc/pgx/v5`
```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

func InitDB(ctx context.Context) (*pgxpool.Pool, error) {
	connStr := fmt.Sprintf(
		"postgres://%s:%s@%s:%s/%s?sslmode=disable",
		os.Getenv("DB_USER"),
		os.Getenv("DB_PASS"),
		os.Getenv("DB_HOST"),
		os.Getenv("DB_PORT"),
		os.Getenv("DB_NAME"),
	)

	config, err := pgxpool.ParseConfig(connStr)
	if err != nil {
		return nil, fmt.Errorf("failed to parse db config: %w", err)
	}

	// Elastic scaling pool parameters for Zerops
	config.MaxConns = 25
	config.MinConns = 5
	config.MaxConnLifetime = 1 * time.Hour
	config.MaxConnIdleTime = 15 * time.Minute
	config.HealthCheckPeriod = 1 * time.Minute

	pool, err := pgxpool.NewWithConfig(ctx, config)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to postgres: %w", err)
	}

	if err := pool.Ping(ctx); err != nil {
		return nil, fmt.Errorf("db ping failed: %w", err)
	}

	log.Println("Successfully connected to Zerops PostgreSQL cluster")
	return pool, nil
}
```

### Pattern 3: Atomic Migrations Binary for `zsc execOnce`
```go
// cmd/migrate/main.go
package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/jackc/pgx/v5"
)

func main() {
	connStr := fmt.Sprintf(
		"postgres://%s:%s@%s:%s/%s?sslmode=disable",
		os.Getenv("DB_USER"),
		os.Getenv("DB_PASS"),
		os.Getenv("DB_HOST"),
		os.Getenv("DB_PORT"),
		os.Getenv("DB_NAME"),
	)

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	conn, err := pgx.Connect(ctx, connStr)
	if err != nil {
		log.Fatalf("Migration connection error: %v", err)
	}
	defer conn.Close(ctx)

	query := `
	CREATE TABLE IF NOT EXISTS schema_migrations (
		version INT PRIMARY KEY,
		applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
	);
	`
	if _, err := conn.Exec(ctx, query); err != nil {
		log.Fatalf("Failed to execute schema migration: %v", err)
	}

	log.Println("Database migration executed successfully via zsc execOnce")
}
```

### Pattern 4: CGO Image Processing with `libvips` (`os: ubuntu`)
```go
package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	// Requires build.os: ubuntu and run.os: ubuntu in zerops.yaml
	// #cgo pkg-config: vips
	// #include <vips/vips.h>
	"C"
)

func main() {
	if C.vips_init(C.CString("zerops-vips")) != 0 {
		log.Fatal("Unable to initialize libvips")
	}
	defer C.vips_shutdown()

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "OK - Go CGO libvips running on Zerops Ubuntu base")
	})

	log.Fatal(http.ListenAndServe(":"+port, nil))
}
```

### Pattern 5: Interactive SSH Development Setup with `noop`
In `zerops.yaml`, authoring a `dev` setup allows interactive SSH development without rebuild triggers:

```yaml
zerops:
  - setup: dev
    build:
      base: go@1.22
      buildCommands:
        - go mod download
      deployFiles:
        - ./
      cache: true
    run:
      base: go@1.22
      ports:
        - port: 8080
          httpSupport: true
      start: zsc noop --silent
```

---

## 4. Anti-Patterns & Gotchas in Zerops

| Anti-Pattern | Why it Fails | Correct Solution |
|---|---|---|
| Compiling CGO on `os: alpine` | Dynamic linking against musl causes `502 Bad Gateway` on launch | Set `os: ubuntu` in `build` and `run` when CGO is enabled. |
| Deploying source code in `prod` (`deployFiles: ./`) | Bloats runtime container and increases memory footprint | Deploy compiled binaries only: `deployFiles: [./app, ./migrate]`. |
| Running migrations in `buildCommands` | Schema migrations run against the build container, not the live database | Execute migrations in `run.initCommands` using `zsc execOnce`. |
| Omitting `cache: true` in `build` | Every build downloads all modules over the network, slowing deploys | Add `cache: true` to snapshot the global `GOMODCACHE`. |
| Hardcoding `verticalAutoscaling` | Overrides Zerops' native dynamic elastic scaling | Omit `verticalAutoscaling` and allow Zerops to auto-scale. |
