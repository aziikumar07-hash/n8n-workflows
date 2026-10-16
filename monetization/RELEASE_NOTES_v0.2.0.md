# Release v0.2.0 — OpenAI Ecosystem Focus + First Validated Workflows

## What's new

### ✅ First `ready`-status workflows

Two workflows are now fully validated with complete setup documentation, sample payloads, SQL scripts, and cost tables:

- **[Translate Form Submissions](AI_ML/translate_form_submissions.json)** — GPT-4o + text-embedding-3-small + Supabase pgvector  
  Translates multilingual webhook form payloads and logs results to Google Sheets.

- **[Daily Content Ideas](AI_ML/daily_content_ideas.json)** — GPT-4o + Cohere embeddings + Supabase deduplication  
  Generates and deduplicates daily content ideas, posts to Slack.

### 📋 OpenAI workflow index

The root README now has a dedicated section listing all 10 OpenAI-powered workflows with their specific models (`gpt-4o`, `text-embedding-3-small`, `whisper-1`).

### 🔧 Stronger CI

- JSON schema validation added to `scripts/validate_workflows.py` via optional `jsonschema` dependency
- `scripts/requirements.txt` makes CI dependencies reproducible
- CI installs dependencies before running validator

### 📖 Richer docs for validated workflows

Validated workflow docs now include:
- Full node inventory table
- Sample input JSON payloads
- Sample output format
- Step-by-step credential setup
- Supabase pgvector SQL
- Per-provider cost estimates

## Install / use

```bash
# Clone and validate
git clone https://github.com/your-org/n8n-free-templates
cd n8n-free-templates
pip install -r scripts/requirements.txt
python scripts/validate_workflows.py
```

Import any `.json` file into n8n via **Settings → Import from File**.

## What's next (v0.3.0)

- Validate remaining AI/ML workflows
- Add category READMEs with compatibility notes
- Add error handling and retry guidance to workflow docs
