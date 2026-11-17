# CrewAI Engine: Infrastructure & Mesh Topology

## 1. Network Topology & Ports

```mermaid
flowchart LR
    A["Hermes Daemon (Python 3.12)"] -->|"HTTP :8080 (BIFROST_MASTER_VK)"| B["Maxim AI Bifrost (Go 1.22)"]
    B -->|"CEL Default Priority 2 (true, fallbacks: [])"| C["FreeLLMAPI (:3001)"]
    C -->|"Keyed + Keyless (kilo, ovh) Pools"| D["Cerebras / Groq / Ollama / OpenRouter / Kilo / OVH"]
    B -->|"Explicit Pro Only (x-force-deepseek / x-routing-tier: pro)"| E["DeepSeek Official API"]
    A -->|"POSIX NVMe Mount"| F["/mnt/localstorage/skills"]
    A -->|"CREWAI_STORAGE_DIR + Knowledge (ONNX)"| G["/mnt/localstorage/hermes/crewai"]
```

## 2. Invariant Specifications

- **Container Runtime**: Hermes + embedded `crewai_engine` run in `ubuntu/python@3.12` LXC on Zerops.
- **Persistent Volume**: Mounted at `/mnt/localstorage` (`CREWAI_STORAGE_DIR=/mnt/localstorage/hermes/crewai`).
- **Inference Gateway**: Bifrost (`http://bifrost:8080/v1`) routes strictly to FreeLLMAPI (`fallbacks: []` unless `x-allow-paid-fallback: true` or `x-force-deepseek: true`).
- **Embedder Invariant ($0 Local ONNX)**: CrewAI's built-in `{"provider": "onnx"}` embedder (`KnowledgeLoader.build_embedder_config()`) embeds playbooks locally without needing `OPENAI_API_KEY` or Bifrost embedding routes.
- **Path Resolution Invariant**: All file paths passed to `TextFileKnowledgeSource` MUST be explicit `pathlib.Path` instances to avoid CrewAI's `knowledge/` string-prefix bug.
