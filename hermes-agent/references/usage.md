# Hermes-Agent Usage & Runtime Architecture Guide

This guide establishes the production operational standard for **Nous Research Hermes-Agent** (CalVer 2026.8+), covering the core agent loop, tool calling protocols, Telegram Bot Gateway integration, and anti-flood communication pipelines.

---

## 1. Core Agent Loop & ChatML Tool Protocol

Hermes models (Hermes 2, Hermes 3, Hermes-Agent) use a specialized ChatML prompt template designed for precise structured output and zero-shot tool execution.

### System Prompt Tool Injection Schema

Tools are defined inside an XML `<tools>` block within the system prompt:

```markdown
<|im_start|>system
You are Hermes, a state-of-the-art autonomous AI agent. You have access to the following tools:
<tools>
{
  "name": "zerops_deploy",
  "description": "Trigger a build and deployment for a Zerops runtime service",
  "parameters": {
    "type": "object",
    "properties": {
      "service": {"type": "string", "description": "Hostname of the target service"},
      "branch": {"type": "string", "description": "Git branch to deploy from (default: main)"}
    },
    "required": ["service"]
  }
}
</tools>
When you need to call a tool, you MUST respond ONLY with the tool call in this exact format:
<tool_call>
{"name": "zerops_deploy", "arguments": {"service": "directus"}}
</tool_call>
<|im_end|>
```

### Agent Execution Loop Pipeline

1. **User Turn**: Ingestion from Telegram, CLI, or API webhook.
2. **Context Assembly**: System prompt + tool schema injection + conversation history + system state.
3. **Model Generation**: Output generation via Hermes LLM (vLLM, Ollama, OpenRouter, or OpenAI-compatible endpoint).
4. **Parsing**: Regex or parser extraction of `<tool_call>...</tool_call>` chunks.
5. **Execution**: Dynamic dispatch to registered tool handlers.
6. **Tool Ingestion**: Output fed back as `<|im_start|>tool
<tool_response>{"result": ...}</tool_response><|im_end|>`.
7. **Synthesis**: Final assistant response generated and sent to the user.

---

## 2. Telegram Bot Gateway Architecture

The Telegram Gateway provides a direct, mobile-first interface for system administrators and developers.

```
┌─────────────────┐       HTTPS Webhook        ┌──────────────────────────────┐
│  Telegram Bot   │ ─────────────────────────> │  FastAPI / PTB Gateway Host  │
│  API (v22.8)    │ <───────────────────────── │  (/webhook/telegram)         │
└─────────────────┘      MarkdownV2 / Media    └──────────────┬───────────────┘
                                                              │
                                                              ▼
                                               ┌──────────────────────────────┐
                                               │ RBAC & Whitelist Filter      │
                                               └──────────────┬───────────────┘
                                                              │
                                                              ▼
                                               ┌──────────────────────────────┐
                                               │ Hermes Agent Core Loop       │
                                               └──────────────────────────────┘
```

### Key Gateway Requirements

- **Telegram Bot API**: Uses `python-telegram-bot[webhooks]==22.8` or `aiogram==3.15.0`.
- **Ingestion Mode**:
  - *Production*: Webhook mode bound to Zerops internal or public port (e.g., `:8443` or `:8000`).
  - *Development / Local*: Long polling (`run_polling(drop_pending_updates=True)`).
- **Security Whitelist**: Mandatory rejection of all user IDs not present in `TELEGRAM_ALLOWED_USERS`.
- **Anti-Flood Rate Limiting**: Telegram limits bot messages to ~30 messages/second globally and 1 message/second per chat. Streaming edits must be strictly batched (every 300–800ms, minimum delta 20 characters).

---

## 3. Production Implementation Patterns

### Pattern 1: Telegram Webhook Server with FastAPI & PTB

```python
import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL")
ALLOWED_USERS = {int(uid.strip()) for uid in os.getenv("TELEGRAM_ALLOWED_USERS", "").split(",") if uid.strip()}

ptb_app = Application.builder().token(TOKEN).build()

async def auth_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user = update.effective_user
    if not user or user.id not in ALLOWED_USERS:
        if update.effective_message:
            await update.effective_message.reply_text("⛔ Unauthorized access rejected.")
        return False
    return True

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await auth_filter(update, context):
        return
    await update.message.reply_text("👋 Hermes-Agent online. Send instructions or commands.")

ptb_app.add_handler(CommandHandler("start", handle_start))

@asynccontextmanager
async def lifespan(app: FastAPI):
    await ptb_app.initialize()
    if WEBHOOK_URL:
        await ptb_app.bot.set_webhook(url=f"{WEBHOOK_URL}/telegram", drop_pending_updates=True)
    await ptb_app.start()
    yield
    await ptb_app.stop()
    await ptb_app.shutdown()

api = FastAPI(lifespan=lifespan)

@api.post("/telegram")
async def telegram_webhook(request: Request):
    payload = await request.json()
    update = Update.de_json(payload, ptb_app.bot)
    await ptb_app.process_update(update)
    return Response(status_code=200)

@api.get("/healthz")
async def health_check():
    return {"status": "healthy", "service": "hermes-telegram-gateway"}

if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=8000, reload=False)
```

### Pattern 2: Tool Registry & Strict Pydantic Dispatcher

```python
import json
import inspect
from typing import Callable, Dict, Any
from pydantic import BaseModel

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: list[dict] = []

    def register(self, name: str, description: str, schema_model: type[BaseModel]):
        def decorator(func: Callable):
            self._tools[name] = (func, schema_model)
            json_schema = schema_model.model_json_schema()
            self._schemas.append({
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": json_schema.get("properties", {}),
                    "required": json_schema.get("required", [])
                }
            })
            return func
        return decorator

    def get_schemas(self) -> list[dict]:
        return self._schemas

    async def execute(self, name: str, raw_arguments: str | dict) -> dict:
        if name not in self._tools:
            return {"error": f"Tool '{name}' is not registered."}
        func, model = self._tools[name]
        try:
            args_dict = json.loads(raw_arguments) if isinstance(raw_arguments, str) else raw_arguments
            validated = model.model_validate(args_dict)
            if inspect.iscoroutinefunction(func):
                result = await func(**validated.model_dump())
            else:
                result = func(**validated.model_dump())
            return {"success": True, "result": result}
        except Exception as err:
            return {"success": False, "error": str(err)}
```

### Pattern 3: Anti-Flood Streaming Message Drafter

Telegram rejects rapid message edits. This drafter buffers tokens, updates only on meaningful changes (delta > 25 chars or elapsed > 600ms), and formats with `MarkdownV2` upon completion.

```python
import time
import asyncio
from telegram import Message
from telegram.helpers import escape_markdown
from telegram.error import BadRequest, RetryAfter

class TelegramStreamDrafter:
    def __init__(self, message: Message, min_interval: float = 0.6, min_chars: int = 25):
        self.message = message
        self.min_interval = min_interval
        self.min_chars = min_chars
        self.buffer = ""
        self.last_sent = ""
        self.last_edit_time = 0.0

    async def append(self, token: str):
        self.buffer += token
        now = time.time()
        if (now - self.last_edit_time >= self.min_interval) and (len(self.buffer) - len(self.last_sent) >= self.min_chars):
            await self._flush_draft(now)

    async def _flush_draft(self, timestamp: float):
        try:
            # Send plain draft text to prevent Markdown parse failures mid-stream
            await self.message.edit_text(self.buffer + " ▌")
            self.last_sent = self.buffer
            self.last_edit_time = timestamp
        except RetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except BadRequest:
            pass  # Ignored when content is identical

    async def finalize(self):
        try:
            # Finalize using clean Markdown formatting
            formatted = escape_markdown(self.buffer, version=2)
            await self.message.edit_text(self.buffer, parse_mode=None)
        except Exception:
            await self.message.edit_text(self.buffer)
```

### Pattern 4: Inline Approval Callback Flow for High-Risk Deployments

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackQueryHandler

async def prompt_deploy_confirmation(update: Update, service: str, caller_id: int):
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm Deploy", callback_data=f"deploy:confirm:{service}:{caller_id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"deploy:cancel:{service}:{caller_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"⚠️ *High-Impact Operation Requested*

Service: `{service}`
Action: Build & Deploy

Please confirm authorization:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_callback_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":")
    action, decision, service, caller_id = parts[0], parts[1], parts[2], int(parts[3])

    if query.from_user.id != caller_id:
        await query.message.reply_text("⛔ You are not authorized to decide on this action.")
        return

    if decision == "confirm":
        await query.edit_message_text(f"🚀 Deploy approved for `{service}`. Dispatching task to AGY...")
        # Dispatch to bridge
    else:
        await query.edit_message_text(f"🛑 Deploy cancelled for `{service}`.")
```

---

## 4. Error Catalog & Remediation Matrix

| Error Scenario | Root Cause | Immediate Remediation |
|---|---|---|
| **Telegram `RetryAfter: Flood control exceeded`** | Bot edited or sent messages faster than 1/sec per chat. | Back off for the duration returned by `e.retry_after`; tune `min_interval` to `0.8s` in `TelegramStreamDrafter`. |
| **Markdown Parsing Error (`Can't parse entities`)** | Unescaped special characters (`_`, `*`, `[`, `]`, `(`, `)`, `~`, `` ` ``, `>`, `#`, `+`, `-`, `=`, `|`, `{`, `}`, `.`, `!`). | Stream drafts with `parse_mode=None`; use `escape_markdown(text, version=2)` only on final render or wrap code in raw code blocks. |
| **Invalid `<tool_call>` JSON syntax** | Model emitted truncated or malformed JSON arguments. | Catch JSONDecodeError; return `<tool_response>{"error": "Malformed JSON arguments. Correct the JSON structure and retry."}</tool_response>`. |
| **Non-existent tool hallucination** | Model invented a tool name not in the `<tools>` schema. | Return `<tool_response>{"error": "Tool '{name}' does not exist. Available tools: {list}"}</tool_response>` so the model re-evaluates. |
| **Context Window Overflow** | Unbounded conversation history or oversized tool output. | Implement sliding-window truncation, summarize past turns, and cap tool output to 2000 tokens before re-injecting into the prompt. |
