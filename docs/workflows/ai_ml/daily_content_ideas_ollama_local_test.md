# Daily Content Ideas (Ollama — local test)

- **Workflow file:** `AI_ML/daily_content_ideas_ollama_local_test.json`
- **Status:** `ready`
- **Tested date:** 2026-10-20 (n8n 2.43.7, Windows, Ollama)
- **n8n compatibility:** 2.x (run-tested on 2.43.7); expected to work on 1.50+
- **Variant of:** [`daily_content_ideas_ollama.json`](daily_content_ideas_ollama.md) — same agent logic, but **zero external services** (no Supabase, no Google Sheets, no Slack)
- **Source:** Original work (local-test variant of an original variant)

## Purpose

A fully self-contained version of [Daily Content Ideas (Ollama)](daily_content_ideas_ollama.md) that you can import and run with **nothing but n8n and Ollama** — no API keys, no database, no spreadsheets.

The workflow:

1. Accepts a webhook POST with a `topic` (and optional `sessionId`)
2. Chunks the request payload and stores embeddings in n8n's built-in **In-Memory Vector Store** (persists across runs in the same n8n process)
3. Runs a **RAG agent** (`llama3.1`) that can query the vector store via the `recent_content_ideas` tool to avoid duplicating previously generated ideas
4. Appends the result as JSON to a local log file

Good for: validating the RAG pattern end-to-end, air-gapped environments, cost-sensitive deployments, or anyone who wants a zero-keyword content-ideas pipeline.

## What's swapped vs. the Supabase version

| Component | `daily_content_ideas_ollama.json` | This variant |
|---|---|---|
| Vector store | Supabase pgvector (768 dims) | In-Memory Vector Store (n8n built-in) |
| Idea logging | Google Sheets append | Write Binary File → `content_ideas_log.json` |
| Slack notification | Posts ideas / error alerts | Removed |
| Chat model | `llama3.1` via Ollama | same |
| Embeddings | `nomic-embed-text` via Ollama | same |
| Credentials needed | Supabase + Sheets + Slack | **Ollama only** |

## Requirements

- **Ollama** installed and running — [ollama.com](https://ollama.com)
- Both models pulled locally: `ollama pull llama3.1` and `ollama pull nomic-embed-text`
- n8n must reach Ollama's HTTP API (default `http://localhost:11434`)

## Required credentials

| Credential | n8n credential type | Used by |
|---|---|---|
| Ollama | `ollamaApi` | Chat Model, Embeddings, Vector Store Query |

No other credentials needed.

## Node inventory

| Node name | Type | Purpose |
|---|---|---|
| Sticky Note | `n8n-nodes-base.stickyNote` | Setup instructions on canvas |
| Webhook Trigger | `n8n-nodes-base.webhook` | Receives POST at `/daily-content-ideas-ollama-local` |
| Text Splitter | `@n8n/n8n-nodes-langchain.textSplitterCharacterTextSplitter` | Chunks request payload (400 chars, 40 overlap) |
| Document Loader | `@n8n/n8n-nodes-langchain.documentDefaultDataLoader` | Feeds chunked documents to the vector store |
| Embeddings | `@n8n/n8n-nodes-langchain.embeddingsOllama` | `nomic-embed-text` — 768-dim vectors |
| Vector Store Insert | `@n8n/n8n-nodes-langchain.vectorStoreInMemory` | Stores idea context for deduplication |
| Vector Store Query | `@n8n/n8n-nodes-langchain.vectorStoreInMemory` | `recent_content_ideas` tool for the agent |
| Window Memory | `@n8n/n8n-nodes-langchain.memoryBufferWindow` | Short-term agent memory (keyed by `sessionId`) |
| Chat Model | `@n8n/n8n-nodes-langchain.lmChatOllama` | `llama3.1` generation |
| RAG Agent | `@n8n/n8n-nodes-langchain.agent` | Orchestrates generation + deduplication |
| Convert Agent Output to JSON File | `n8n-nodes-base.convertToFile` | Agent output → JSON |
| Save to File | `n8n-nodes-base.writeBinaryFile` | Appends to `content_ideas_log.json` |

## Setup steps

### Step 1 — Install Ollama and pull models

```bash
# Install Ollama — https://ollama.com/download
ollama pull llama3.1
ollama pull nomic-embed-text

# Verify both are available:
ollama list
```

### Step 2 — Confirm Ollama is reachable

```bash
curl http://localhost:11434/api/tags
```

Create an **Ollama API credential** in n8n (type `ollamaApi`) with Base URL `http://127.0.0.1:11434`.

> ⚠️ Use `127.0.0.1`, not `localhost`. n8n's fetch (undici) does not fall back from IPv6 `::1`, so `localhost` can fail with `ECONNREFUSED ::1:11434` on dual-stack machines.

### Step 3 — Import and configure in n8n

1. **Import** `AI_ML/daily_content_ideas_ollama_local_test.json` via **Import from File**.
2. Attach your Ollama credential to the **Chat Model**, **Embeddings**, and **Vector Store Query** nodes.
3. Adjust the **Save to File** path if needed (n8n 2.x only writes to paths allowed by `N8N_RESTRICT_FILE_ACCESS_TO` — see troubleshooting).
4. **Publish/activate** the workflow, then test with a POST.

### Step 4 — Test

```bash
curl -X POST http://your-n8n-instance/webhook/daily-content-ideas-ollama-local \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "sustainable gardening for beginners",
    "sessionId": "test-session-1"
  }'
```

Expected: an HTTP 200 `{ "message": "Workflow was started" }`, and shortly after, a JSON object with a numbered list of 10 content ideas appended to the log file.

## Verified test run (2026-10-20)

Run on n8n 2.43.7 (Windows) with Ollama on the same host (Tesla T4, 15 GB VRAM; `llama3.1` fully on GPU):

| Run | Result | Wall time | Notes |
|---|---|---|---|
| First (cold models) | ✅ success | ~5 min | First-ever `llama3.1` load (~43 s), 16 chunks embedded, agent looped the dedup tool several times |
| Warm re-run (topology fix applied) | ✅ success | **23 s** | Agent ran exactly once: 2 chat-model calls, 1 vector query, insert chain green |

Both runs ended with a valid JSON object appended to the output file containing 10 unique, on-topic content ideas.

## Design note — do not chain Insert → Agent

The vector insert node emits **one item per chunk**. If you connect `Vector Store Insert → RAG Agent` (main output), the agent runs once *per chunk* — in the first test run above that meant 16 agent invocations (~4.5 min) and 16 duplicate log entries.

This workflow therefore branches the Webhook Trigger into two parallel paths (n8n `executionOrder: v1` runs them in connection order):

1. `Webhook Trigger → Vector Store Insert` (terminal branch — inserts, then stops)
2. `Webhook Trigger → RAG Agent → Convert → Save to File`

The agent references the original payload with `$('Webhook Trigger').first()`, so it runs exactly once per webhook call.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ECONNREFUSED ::1:11434` | `localhost` resolving to IPv6 | Use `http://127.0.0.1:11434` in the credential |
| `Access to the file is not allowed` / file write fails | n8n 2.x blocks writes outside `~/.n8n-files` | Start n8n with `N8N_RESTRICT_FILE_ACCESS_TO` pointing at the output folder |
| Agent output appended N times | Insert chain chained into the agent | Branch them separately (see design note above) |
| Webhook returns 404 | Workflow not published, or using the test URL for production traffic | Publish the workflow; use the production `/webhook/...` path |
| First run very slow | Cold model load (several GB into VRAM/RAM) | Expected once; subsequent runs are much faster |
| Ollama `404: model not found` | Model not pulled | `ollama pull llama3.1` and `ollama pull nomic-embed-text` |

## Alternative models

Any Ollama-compatible chat model works — update the `model` field in the Chat Model node:

| Model | Size | Notes |
|---|---|---|
| `llama3.1` | 4.7 GB | Default — good balance of quality and speed |
| `mistral` | 4.1 GB | Fast, good for structured output |
| `qwen2.5` | 4.7 GB | Strong multilingual performance |
| `phi3` | 2.2 GB | Lightweight, good for low-resource setups |

## Privacy and cost

- **Zero API costs** — inference runs on your hardware.
- All data stays local: the vector store is in-process memory and ideas are appended to a local file.
- The in-memory vector store only survives while the n8n process is running (and is per-workflow). For durable deduplication, use the [Supabase variant](daily_content_ideas_ollama.md).

## Safety notes

- `ai-generated-output` — review generated ideas before publishing.
- The log file is appended, never trimmed — rotate or archive it if the workflow runs frequently.
