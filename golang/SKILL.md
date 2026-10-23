---
name: golang
description: "Trigger: golang, go, zerops go, go runtime, os alpine, os ubuntu, gomodcache, zsc execOnce. Native Go runtime architecture, base selection, GOMODCACHE caching, and deployment pipelines on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# Golang — Zerops Native Go Runtime Engine (v1.1)

## Activation Contract
Activate whenever architecting, building, compiling, caching, or deploying Go microservices (`runtime: alpine/go@1.22` or `ubuntu/go@1.22`) and high-performance compiled binaries on Zerops.

## Hard Rules & Positive Guidance
- **Runtime Base Selection**:
  - `alpine/go@1.22`: Standard for Go web services; produces minimal, static musl binaries.
  - `ubuntu/go@1.22`: Required when compiling with CGO or linking against glibc-dependent shared libraries.
- **Build Pipeline & Caching**: Cache `go/pkg/mod` and `~/.cache/go-build` in `zerops.yaml` to reduce compile times from minutes to seconds.
- **Static Binary Output**: In production runtimes, copy only the compiled binary and necessary configuration assets into the deploy artifact.
- **Port Binding**: Bind HTTP/gRPC servers to `0.0.0.0` on port `8080` (or `${PORT}`).
- **Container Execution**: Run Go tests inside the container via SSH (`ssh {hostname} "cd /var/www && go test ./..."`).

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Static Binary Compilation | CGO_ENABLED=0 go build -ldflags="-s -w" | [`references/usage.md#compilation`](file:///var/www/.agents/skills/golang/references/usage.md) |
| Caching Optimization | go/pkg/mod and build cache in zerops.yaml | [`references/infra.md#caching`](file:///var/www/.agents/skills/golang/references/infra.md) |
| Alpine vs Ubuntu Base | musl static vs glibc CGO compilation | [`references/infra.md#base-images`](file:///var/www/.agents/skills/golang/references/infra.md) |

## Critical Workflows
1. Declare Go runtime in `zerops.yaml` with build and run stages.
2. Compile binary during `build` and output to artifact directory.
3. Validate service with physical health sensor (`curl -s http://<service>:8080/health`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/golang/references/usage.md) — Go compilation flags, web server patterns, CGO handling, and test suites.
- [`references/infra.md`](file:///var/www/.agents/skills/golang/references/infra.md) — Multi-stage deployment manifests, GOMODCACHE caching, and base image trade-offs.
