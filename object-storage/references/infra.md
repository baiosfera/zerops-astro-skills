# Zerops Object Storage Infrastructure Specification (MinIO S3)

Technical reference for platform provisioning, security policies, environment variable injection, and lifecycle management of Object Storage in Zerops.

---

## 1. Zerops Object Storage Specification

Zerops Object Storage is a high-performance, S3-compatible managed service powered by MinIO. It runs isolated on the project's private overlay network and exposes an HTTPS S3 gateway.

### A. Manifest Declaration (`import.yaml`)
```yaml
services:
  - hostname: objectstorage
    type: object-storage             # or "objectstorage"
    objectStorageSize: 10             # Storage quota in GB (1 to 100)
    objectStoragePolicy: private      # Security policy: private | public-read
    priority: 10                      # High priority: provisions before runtimes
```

### B. Predefined Security Policies (`objectStoragePolicy`)
- **`private`** (Default): No anonymous access. All requests require valid S3v4 signature headers. Recommended for user data, confidential contracts, raw data lakehouse dumps, and database backups.
- **`public-read`**: Anonymous clients can issue `GET` and `HEAD` requests without authentication. Recommended for publicly distributed static media, brandbook showcases, public product images, and font files.

---

## 2. Environment Variables Wiring

When an Object Storage service is provisioned with hostname `objectstorage`, Zerops automatically generates the following connection variables across the project:

| Platform Variable | Description |
|---|---|
| `${objectstorage_apiUrl}` | Full HTTPS S3 endpoint URL (`https://...`), ready for SDK `endpoint` option. |
| `${objectstorage_apiHost}` | Host-only endpoint without scheme (requires manual `https://` prefix). |
| `${objectstorage_accessKeyId}` | Unique S3 access key ID. |
| `${objectstorage_secretAccessKey}` | Cryptographic S3 secret access key. |
| `${objectstorage_bucketName}` | Immutable auto-generated bucket name (hostname + random unique suffix). |
| `${objectstorage_quotaGBytes}` | Configured bucket quota in GB. |

### Canonical `zerops.yaml` Service Injection
```yaml
run:
  envVariables:
    S3_ENDPOINT: ${objectstorage_apiUrl}
    S3_ACCESS_KEY: ${objectstorage_accessKeyId}
    S3_SECRET_KEY: ${objectstorage_secretAccessKey}
    S3_BUCKET: ${objectstorage_bucketName}
    S3_REGION: "us-east-1"
    AWS_USE_PATH_STYLE_ENDPOINT: "true"
```

---

## 3. Co-Existence Matrix: Local Storage vs. Object Storage

| Dimension | `local-storage` (`local-storage:single@1`) | `object-storage` (`object-storage`) |
|---|---|---|
| **Underlying Tech** | Dedicated Incus LXC persistent POSIX disk volume | Distributed S3 MinIO cluster |
| **Mount Mechanism** | `run.volume: {hostname, mountPath}` in `zerops.yaml` | S3 API via HTTP/HTTPS network calls |
| **Kernel Locks** | Native POSIX advisory locks (`flock`, `fcntl`) | None (S3 object immutability) |
| **Primary Use Cases** | SQLite WAL databases, search indexes, socket files | User uploads, PDF reports, brandbook assets, dumps |
| **Deploy Lifecycle** | Preserved across container restarts & redeploys | Preserved indefinitely across all deploys |
| **Container Placement** | Co-located on the same physical host machine | Network-accessible from any container in the project |
