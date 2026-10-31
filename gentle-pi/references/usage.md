# `gentle-pi` — Usage, CLI Patterns & Bounded Execution Manual

This manual details the interactive and headless operational modes of the **Pi Coding Agent** (`pidev`) and **Gentle Shell** within Zerops.

---

## 1. Core Mental Model: The Sovereign Code Builder

In our multi-agent mesh:
- **Hermes (Chief of Staff)**: Receives natural language from Telegram or SSH, formulates technical specifications via PydanticAI, and dispatches implementation tasks.
- **Pi (`pidev`)**: The sole surgical code editor for Astro 5 SSR, TypeScript, and Tailwind CSS.
- **Goose**: The independent QA/Reviewer that runs `bun test` and checks diffs before git commit.
- **Paperclip**: The governance watchdog enforcing daily token spend caps and heartbeat schedules.

Pi operates in two modes:
1. **Interactive Split-Rail Mode**: Used during manual developer sessions via SSH terminal.
2. **Headless Agentic Mode**: Used for autonomous task execution triggered via NATS RPC or local queue.

---

## 2. Interactive Mode (`pi` / `gentle-shell`)

### Launching the Interactive Shell
Connect to the `pidev` container over SSH:
```bash
ssh pidev "cd /var/www && pi"
```

### Key Interactive Features
- **Split-Rail TUI**: Left rail displays conversation context and reasoning; right rail displays live unified diffs (`pi-tui`).
- **QuickJS Sandboxed Eval**: Evaluates small snippets and AST transformations safely before touching the file system.
- **Direct Terminal Hot-Reload**: Changes made to Astro components in `/var/www/webdev` hot-reload instantly on the Zerops preview subdomain.

### Keyboard Shortcuts in Split-Rail
| Key | Action |
|---|---|
| `Tab` | Switch focus between Prompt rail and Diff preview rail |
| `Ctrl+O` | Accept unified diff and write to disk |
| `Ctrl+R` | Reject diff and return to prompt |
| `Ctrl+T` | Run test suite in background (`bun test`) |
| `Ctrl+C` | Cancel active generation |

---

## 3. Headless Mode (`pi -p` / JSON RPC)

Hermes triggers Pi tasks headlessly without opening an interactive TUI session.

### Direct Prompt Invocation (`pi -p`)
```bash
# Execute a single-turn coding task headlessly
pi -p "Update src/components/Hero.astro with new brandbook tokens from /mnt/localstorage/pidev/brandbook_state.json"
```

### JSON RPC Protocol (`--mode json`)
Pi can stream structured events over stdin/stdout for seamless NATS integration:
```bash
pi --mode json < task_input.json
```

**Task Input Schema (`task_input.json`)**:
```json
{
  "taskId": "task-2026-10-31-001",
  "instruction": "Refactor ProductCard.astro to use Tailwind 4 container queries",
  "targetFiles": ["src/components/ProductCard.astro"],
  "contextFiles": ["src/styles/theme.css", "/mnt/localstorage/pidev/brandbook_state.json"],
  "testCommand": "bun test src/components/ProductCard.test.ts"
}
```

**Streamed Response Schema**:
```json
{
  "event": "diff_generated",
  "file": "src/components/ProductCard.astro",
  "unifiedDiff": "--- a/src/components/ProductCard.astro\n+++ b/src/components/ProductCard.astro\n@@ -5,2 +5,2 @@...",
  "testResult": {
    "command": "bun test",
    "exitCode": 0,
    "output": "1 test passed"
  },
  "status": "completed"
}
```

---

## 4. ODD (Outcome-Driven Development) & RDD (Receipt-Driven Development)

1. **Receipt Generation**: Every file edit produces an immutable cryptographic receipt containing:
   - Git SHA pre-edit.
   - Unified diff.
   - Test execution output and exit code.
   - Timestamps and token consumption metrics.
2. **Review Authority**: The receipt is published to NATS topic `receipts.coding.<taskId>` where Hermes or Goose audits compliance.
3. **Delivery Gate**: If tests fail (exit code $\neq 0$), Pi rolls back changes immediately to the pre-edit Git SHA.
