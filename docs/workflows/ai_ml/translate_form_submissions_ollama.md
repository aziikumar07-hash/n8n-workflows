# Translate Form Submissions (Ollama)

**Category:** AI_ML
**Status:** ready — run-tested end-to-end on 2026-10-20 (n8n 2.43.7, Ollama 0.13.x, Windows Server 2025, Tesla T4)

Self-hosted variant of [Translate Form Submissions](translate_form_submissions.md). Same pipeline, zero API costs: all model calls run against a local [Ollama](https://ollama.com) server.

## What it does

```
Webhook Trigger → Translation Agent (toolsAgent)
                    ├─ Ollama Chat Model      (orcarouter/qwen3.8-27b-uncensored)
                    ├─ Window Memory
                    └─ In-Memory Vector Store (Query)
                         └─ Ollama Embeddings (nomic-embed-text)
                                  ↑ populated at start of each run by
                          Vector Store Insert ← Text Splitter ← Webhook body
Convert Agent Output to JSON File → Save to File (translations_log.json)
```

1. Accepts a POST with `message` and `target_language`
2. Embeds the message with `nomic-embed-text` and retrieves similar stored translations (few-shot context)
3. The agent translates via the local chat model
4. Appends the result to `translations_log.json`

## Prerequisites

1. **Ollama** running locally on port 11434
2. Models pulled:
   ```
   ollama pull orcarouter/qwen3.8-27b-uncensored
   ollama pull nomic-embed-text
   ```
   (Any Ollama chat + embedding model pair works — change the model names in the Chat Model and Embeddings nodes.)
3. **One Ollama credential** in n8n (`ollamaApi` type) — Base URL: `http://127.0.0.1:11434`
   - Use `127.0.0.1`, **not** `localhost`: n8n's HTTP dispatcher does not fall back from IPv6 `::1`, and Ollama listens on IPv4 only. With `localhost` every model call fails instantly with `fetch failed` / `ECONNREFUSED ::1:11434`.
4. **n8n must allow writes to the output folder.** The Save to File node writes to the Desktop; n8n 2.x blocks all file writes outside `~/.n8n-files` unless you set:
   ```
   N8N_RESTRICT_FILE_ACCESS_TO=C:\Users\<you>\Desktop
   ```
   (semicolon-separated list; set before starting n8n)

## Setup

1. Import the JSON, attach your `ollamaApi` credential to both the **Chat Model** and **Embeddings** nodes
2. Adjust the **Save to File** `fileName` if you don't want `C:\Users\<you>\Desktop\translations_log.json`
3. Activate the workflow (production webhook)

## Test payload

```bash
curl -X POST "http://localhost:5678/webhook/<WORKFLOW_ID>/webhook%2520trigger/translate-form-submissions-ollama" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, necesito ayuda con mi pedido", "target_language": "English"}'
```

> The production webhook path contains the literal string `webhook trigger` (with a space) between the workflow ID and your custom path. When calling via curl, double-encode the space as `%2520`.

Expected output appended to `translations_log.json`:

```json
{
  "output": "Hello, I need help with my order."
}
```

## Verified run (2026-10-20)

- n8n 2.43.7 on Windows Server 2025, Ollama with `orcarouter/qwen3.8-27b-uncensored` (16.5 GB, Tesla T4 15 GB VRAM) + `nomic-embed-text`
- Full execution `success` in ~60 s: Webhook Trigger → Embeddings → Vector Store Query → Chat Model (~57 s) → Translation Agent → Convert to File → Save to File, all nodes green
- First cold run takes ~3–4 min while the 16 GB model loads into VRAM

## Troubleshooting

| Problem | Fix |
|---|---|
| `fetch failed` / `connect ECONNREFUSED ::1:11434` | Credential Base URL must be `http://127.0.0.1:11434` (IPv6 `::1` is refused) |
| `Node does not have any credentials set` | Attach the Ollama credential to the Chat Model **and** Embeddings nodes |
| `Access to the file is not allowed` | Set `N8N_RESTRICT_FILE_ACCESS_TO` to the output folder before starting n8n |
| Webhook 404 | Workflow must be **activated** (production URL), and the space in `webhook trigger` must be double-encoded (`%2520`) in curl |
| Slow first response | Normal for large models — Ollama loads the model on first call and unloads after ~5 min idle |
