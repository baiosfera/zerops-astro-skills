# Rust 1.85+ — Developer & Architecture Usage Manual on Zerops

This manual provides production-tested specifications, Axum 0.8+ HTTP architectures, Tokio async runtimes, SQLx connection pools with `rustls`, and compilation recipes for **Rust** on Zerops Incus LXC runtimes.

---

## 1. Production Axum 0.8+ HTTP Router with State

```rust
use axum::{
    extract::State,
    http::StatusCode,
    response::IntoResponse,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::net::TcpListener;
use tower_http::trace::TraceLayer;

#[derive(Clone)]
pub struct AppState {
    pub db_pool: sqlx::PgPool,
}

#[derive(Serialize, Deserialize)]
pub struct UserPayload {
    pub username: String,
    pub email: String,
}

#[derive(Serialize)]
pub struct UserResponse {
    pub id: i64,
    pub username: String,
    pub email: String,
}

pub fn create_router(state: Arc<AppState>) -> Router {
    Router::new()
        .route("/healthz", get(healthz_handler))
        .route("/api/users", post(create_user_handler))
        .layer(TraceLayer::new_for_http())
        .with_state(state)
}

async fn healthz_handler() -> impl IntoResponse {
    (StatusCode::OK, "healthy")
}

async fn create_user_handler(
    State(state): State<Arc<AppState>>,
    Json(payload): Json<UserPayload>,
) -> Result<(StatusCode, Json<UserResponse>), StatusCode> {
    let row = sqlx::query!(
        "INSERT INTO users (username, email) VALUES ($1, $2) RETURNING id",
        payload.username,
        payload.email
    )
    .fetch_one(&state.db_pool)
    .await
    .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    Ok((
        StatusCode::CREATED,
        Json(UserResponse {
            id: row.id,
            username: payload.username,
            email: payload.email,
        }),
    ))
}
```

---

## 2. SQLx 0.8+ Async Connection Pool with `rustls`

Configure `Cargo.toml` to avoid OpenSSL linking failures:
```toml
[dependencies]
sqlx = { version = "0.8", default-features = false, features = [
    "runtime-tokio-rustls",
    "postgres",
    "macros",
    "chrono",
    "uuid"
] }
tokio = { version = "1.40", features = ["full"] }
```

Initialization in `src/main.rs`:
```rust
use sqlx::postgres::PgPoolOptions;
use std::{env, time::Duration};

pub async fn init_db_pool() -> Result<sqlx::PgPool, sqlx::Error> {
    let database_url = env::var("DATABASE_URL").unwrap_or_else(|_| {
        format!(
            "postgres://{}:{}@{}:{}/{}",
            env::var("DB_USER").unwrap_or_else(|_| "zerops".into()),
            env::var("DB_PASS").unwrap_or_default(),
            env::var("DB_HOST").unwrap_or_else(|_| "db".into()),
            env::var("DB_PORT").unwrap_or_else(|_| "5432".into()),
            env::var("DB_NAME").unwrap_or_else(|_| "db".into()),
        )
    });

    PgPoolOptions::new()
        .max_connections(25)
        .min_connections(5)
        .acquire_timeout(Duration::from_secs(5))
        .idle_timeout(Duration::from_secs(600))
        .connect(&database_url)
        .await
}
```

---

## 3. Dedicated Migration Binary (`src/bin/migrate.rs`)

For atomic migrations executed via `zsc execOnce` on Zerops:

```rust
use sqlx::migrate::Migrator;
use std::path::Path;

static MIGRATOR: Migrator = sqlx::migrate!("./migrations");

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let pool = rust_app::init_db_pool().await?;
    println!("Running database migrations...");
    MIGRATOR.run(&pool).await?;
    println!("Database migrations completed successfully.");
    Ok(())
}
```

---

## 4. Graceful Shutdown Signal Handling (Tokio + Axum)

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let pool = init_db_pool().await?;
    let state = Arc::new(AppState { db_pool: pool });
    let app = create_router(state);

    let port = std::env::var("PORT").unwrap_or_else(|_| "8080".into());
    let listener = TcpListener::bind(format!("0.0.0.0:{}", port)).await?;
    println!("Server listening on port {}", port);

    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;

    Ok(())
}

async fn shutdown_signal() {
    tokio::signal::ctrl_c()
        .await
        .expect("Failed to install CTRL+C signal handler");
    println!("Shutdown signal received, draining connections...");
}
```

---

## 5. Anti-Patterns & Gotchas in Zerops

| Anti-Pattern | Why it Fails | Correct Solution |
|---|---|---|
| Using `native-tls` crates (`reqwest`, `hyper-tls`) | Build container has no `pkg-config`/`libssl-dev` $\to$ compilation error | Use `rustls-tls` or install build tools in `prepareCommands`. |
| Running migrations in `buildCommands` | Fails because managed databases are not reachable during build | Run migrations in `run.initCommands` using `zsc execOnce`. |
| Omitting `CARGO_HOME: ./.cargo` in build | Crates download to root `$HOME`, evading the cache $\to$ slow builds | Set `CARGO_HOME: ./.cargo` and cache `.cargo/registry` and `target`. |
| Omitting `--locked` in `cargo build --release` | Cargo may resolve different dependency versions between environments | Always build with `cargo build --release --locked`. |
| Deploying source directory to production | Bloats runtime disk footprint with hundreds of MBs of debug artifacts | Deploy only binaries via `deployFiles: [ ./target/release/<binary> ]`. |
