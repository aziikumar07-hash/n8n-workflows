# v0.3.0 — First Run-Tested Workflows (Tier 3) + Zero-Dependency Ollama Variants

This release moves the collection from *schema-validated only* to *genuinely run-tested*, and adds two workflows that need **no paid services at all**.

## Highlights

### ✅ First two workflows run-tested end-to-end (Tier 3)

Both were executed on a live n8n 2.43.7 instance with real model calls. Testing surfaced real bugs — which is exactly why we now test before labeling.

| Workflow | What it does | Stack |
|---|---|---|
| [Translate Form Submissions (Ollama)](AI_ML/translate_form_submissions_ollama.json) | Webhook-driven translation with RAG context | n8n 2.43.7 + local Ollama |
| [Daily Content Ideas (Ollama, local test)](AI_ML/daily_content_ideas_ollama_local_test.json) | RAG content-idea generation with dedup tool | n8n 2.43.7 + Ollama `llama3.1` + `nomic-embed-text` |

Both are `status: ready` in the catalog with a recorded `tested_date` of 2026-10-20.

### 🐛 Real defects found and fixed

Run-testing was not a formality. The Daily Content Ideas test exposed a **design defect**: chaining the vector-store insert node directly into the agent passes one item per chunk, causing the agent to run 16 times and log 16 duplicates. Fixed by branching the insert chain as a terminal path. Both the defect and the fix are documented in the workflow's setup guide.

### 🖥️ Zero-dependency local variants

The new Ollama workflows run entirely on your own machine — no OpenAI key, no Supabase, no Google Sheets, no Slack. They use n8n's built-in in-memory vector store and write output to a local JSON file.

### 📚 Two documented n8n 2.x gotchas

Discovered during testing and now written into the setup guides:

1. **Use `127.0.0.1`, not `localhost`** in the Ollama credential — n8n's fetch does not fall back from IPv6 `::1`, so the connection is refused.
2. **n8n 2.x blocks file writes outside `~/.n8n-files`** unless `N8N_RESTRICT_FILE_ACCESS_TO` is set.

### 📊 Honest testing tiers in the README

The root README now separates **schema-validated**, **import-tested**, and **run-tested**, and states plainly what CI does and does not check. No workflow is labeled `ready` without execution evidence.

## Repository stats

- **58 workflow JSON files**
- **2 run-tested (Tier 3)**, both Ollama-based
- Validator: **0 errors, 0 warnings**
- CI green on every push

## Install / use

```bash
git clone https://github.com/aziikumar07-hash/n8n-workflows.git
pip install -r scripts/requirements.txt
python scripts/validate_workflows.py
```

Import any `.json` file into n8n via **Import from File**.

## What's next (v0.4.0)

- Validate additional AI/ML and Social Media workflows end-to-end
- Add category-level compatibility notes to every category README
- Add error-handling and retry guidance to workflow docs
