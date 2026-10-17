# Daily Content Ideas (Ollama — self-hosted)

- **Workflow file:** `AI_ML/daily_content_ideas_ollama.json`
- **Status:** `needs-configuration`
- **Tested date:** Not recorded
- **n8n compatibility:** 1.x
- **Variant of:** [`daily_content_ideas.json`](daily_content_ideas.md) — same logic, fully self-hosted models
- **Source:** Original work (variant of upstream-adapted template)

## Purpose

Identical to [Daily Content Ideas](daily_content_ideas.md) but with **zero external AI API calls**. Uses:

- **[Ollama](https://ollama.com)** (`llama3.1`) as the chat model instead of GPT-4o
- **Ollama** (`nomic-embed-text`) for embeddings instead of Cohere

Everything runs on your own hardware. The only external services are Supabase (for the vector store), Google Sheets (for logging), and Slack (for output) — all three can be self-hosted or replaced too.

Good for: air-gapped environments, cost-sensitive deployments, privacy-first setups, or anyone who wants to avoid API keys entirely.

## Model swap summary

| Component | Cloud variant | This variant |
|---|---|---|
| Chat model | `lmChatOpenAi` — `gpt-4o` | `lmChatOllama` — `llama3.1` |
| Embeddings | `embeddingsCohere` — `embed-english-v3.0` (1024 dims) | `embeddingsOllama` — `nomic-embed-text` (768 dims) |
| Vector table | `embedding vector(1024)` | `embedding vector(768)` |
| Credentials needed | OpenAI + Cohere + Supabase + Sheets + Slack | Supabase + Sheets + Slack only |

## Requirements

- **Ollama** installed and running — [ollama.com](https://ollama.com)
- Both models pulled locally (see setup step 1)
- n8n must be able to reach Ollama's HTTP API (default `http://localhost:11434`)
- Supabase with pgvector (see SQL below — note the different vector dimension vs the cloud variant)

## Required credentials

| Credential | n8n credential type | Used by |
|---|---|---|
| Supabase | `supabaseApi` | Vector store (insert + query) |
| Google Sheets OAuth2 | `googleSheetsOAuth2Api` | Log append |
| Slack API | `slackApi` | Posts ideas + error alerts |

No OpenAI or Cohere credentials needed.

## Node inventory

| Node name | Type | Purpose |
|---|---|---|
| Webhook Trigger | `n8n-nodes-base.webhook` | Receives POST at `/daily-content-ideas-ollama` |
| Text Splitter | `@n8n/n8n-nodes-langchain.textSplitterCharacterTextSplitter` | Chunks topic context |
| Embeddings | `@n8n/n8n-nodes-langchain.embeddingsOllama` | `nomic-embed-text` — 768-dim vectors |
| Supabase Insert | `@n8n/n8n-nodes-langchain.vectorStoreSupabase` | Stores embedding in `daily_content_ideas_ollama` |
| Supabase Query | `@n8n/n8n-nodes-langchain.vectorStoreSupabase` | Retrieves recent ideas for deduplication |
| Vector Tool | `@n8n/n8n-nodes-langchain.toolVectorStore` | Wraps Supabase for the agent |
| Window Memory | `@n8n/n8n-nodes-langchain.memoryBufferWindow` | Short-term agent memory |
| Chat Model | `@n8n/n8n-nodes-langchain.lmChatOllama` | `llama3.1` generation |
| RAG Agent | `@n8n/n8n-nodes-langchain.agent` | Orchestrates generation + deduplication |
| Append Sheet | `n8n-nodes-base.googleSheets` | Logs ideas to spreadsheet |
| Slack Alert | `n8n-nodes-base.slack` | Posts ideas to channel / alerts on error |
| Sticky Note | `n8n-nodes-base.stickyNote` | Setup instructions on canvas |

## Setup steps

### Step 1 — Install Ollama and pull models

```bash
# Install Ollama — https://ollama.com/download
# Then pull both required models:
ollama pull llama3.1
ollama pull nomic-embed-text

# Verify both are available:
ollama list
```

Expected output includes entries for `llama3.1` and `nomic-embed-text`.

### Step 2 — Confirm Ollama is reachable from n8n

```bash
curl http://localhost:11434/api/tags
```

If n8n runs in Docker and Ollama runs on the host, use `http://host.docker.internal:11434` instead of `localhost`. Update the `baseUrl` field in both the **Chat Model** and **Embeddings** nodes accordingly.

### Step 3 — Supabase vector table

Use a **768-dimension** table (nomic-embed-text output size — different from the cloud variant's 1024):

```sql
create extension if not exists vector;

create table daily_content_ideas_ollama (
  id bigserial primary key,
  content text,
  metadata jsonb,
  embedding vector(768)
);

create index on daily_content_ideas_ollama
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);
```

> ⚠️ Do not reuse the `daily_content_ideas` table from the cloud variant — dimension mismatch (1024 vs 768) will cause insert errors.

### Step 4 — Import and configure in n8n

1. **Import** `AI_ML/daily_content_ideas_ollama.json` via **Import from File**.
2. **Chat Model node** — confirm `baseUrl` matches your Ollama address. Model is pre-set to `llama3.1`.
3. **Embeddings node** — same `baseUrl` check. Model is pre-set to `nomic-embed-text`.
4. **Supabase credential** — attach your Supabase credential. The index name is pre-set to `daily_content_ideas_ollama`.
5. **Google Sheets credential** — attach OAuth2 credential. Replace `SHEET_ID` in the Append Sheet node.
6. **Slack credential** — attach Slack token. Update channel name if needed.
7. **Activate** and test with a POST.

### Step 5 — Test

```bash
curl -X POST http://your-n8n-instance/webhook/daily-content-ideas-ollama \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "home office productivity",
    "audience": "remote workers",
    "count": 3,
    "formats": ["blog post", "short video"]
  }'
```

## Alternative models

`llama3.1` is a solid default but any Ollama-compatible chat model works — just update the `model` field in the Chat Model node:

| Model | Size | Notes |
|---|---|---|
| `llama3.1` | 4.7 GB | Default — good balance of quality and speed |
| `llama3.1:70b` | 40 GB | Higher quality, needs significant RAM |
| `mistral` | 4.1 GB | Fast, good for structured output |
| `qwen2.5` | 4.7 GB | Strong multilingual performance |
| `phi3` | 2.2 GB | Lightweight, good for low-resource setups |

For embeddings, `nomic-embed-text` (768 dims) is the recommended default. `mxbai-embed-large` (1024 dims) is an alternative — if you use it, update the Supabase table to `vector(1024)`.

## Docker networking note

If n8n runs in Docker Compose and Ollama runs on the host:

```yaml
# In your docker-compose.yml n8n service:
extra_hosts:
  - "host.docker.internal:host-gateway"
```

Then set `baseUrl` to `http://host.docker.internal:11434` in the Chat Model and Embeddings nodes.

If Ollama also runs in Docker on the same Compose network, use the container service name as the host.

## Cost

**Zero API costs.** Your only running costs are electricity and hardware for the Ollama host.

## Privacy notes

- All inference runs locally — no content leaves your network.
- Supabase can be self-hosted ([supabase.com/docs/guides/self-hosting](https://supabase.com/docs/guides/self-hosting)) to achieve fully air-gapped operation.
- With self-hosted Supabase, Google Sheets is the only remaining external dependency (replaceable with Airtable, Notion, or a local database node).

## Safety notes

- `ai-generated-output` — review generated ideas before publishing.
- Local model quality varies by hardware and model version — outputs may be less consistent than GPT-4o; adjust your review process accordingly.
