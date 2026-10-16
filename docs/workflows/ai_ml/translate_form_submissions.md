# Translate Form Submissions

- **Workflow file:** `AI_ML/translate_form_submissions.json`
- **Status:** `ready`
- **Tested date:** 2026-10-16
- **n8n compatibility:** 1.x
- **Source:** Adapted/imported from `wassupjay/n8n-free-templates` (license status uncertain; verify rights before redistribution)

## Purpose

Accepts a form submission payload via webhook, uses **OpenAI GPT-4o** to translate the text content into a target language, stores a semantic embedding in Supabase via `text-embedding-3-small`, and appends the result to a Google Sheets log. Slack receives an error alert if the agent fails.

Typical use cases: multilingual contact forms, international support ticket intake, global survey responses.

## Required n8n compatibility

- n8n `1.x` — tested on 1.x self-hosted

## Required services and credentials

| Credential | n8n credential type | Used by |
|---|---|---|
| OpenAI API key | `openAiApi` | Chat model (GPT-4o) + Embeddings (text-embedding-3-small) |
| Supabase | `supabaseApi` | Vector store (insert + query) |
| Google Sheets OAuth2 | `googleSheetsOAuth2Api` | Log append |
| Slack API | `slackApi` | Error alert |

## Node inventory

| Node name | Type | Purpose |
|---|---|---|
| Webhook Trigger | `n8n-nodes-base.webhook` | Receives POST at `/translate-form-submissions` |
| Text Splitter | `@n8n/n8n-nodes-langchain.textSplitterCharacterTextSplitter` | Chunks input (400 chars, 40 overlap) |
| Embeddings | `@n8n/n8n-nodes-langchain.embeddingsOpenAi` | `text-embedding-3-small` |
| Supabase Insert | `@n8n/n8n-nodes-langchain.vectorStoreSupabase` | Stores embedding in `translate_form_submissions` index |
| Supabase Query | `@n8n/n8n-nodes-langchain.vectorStoreSupabase` | Retrieves relevant context |
| Vector Tool | `@n8n/n8n-nodes-langchain.toolVectorStore` | Wraps Supabase for agent |
| Window Memory | `@n8n/n8n-nodes-langchain.memoryBufferWindow` | Short-term agent memory |
| Chat Model | `@n8n/n8n-nodes-langchain.lmChatOpenAi` | GPT-4o translation |
| RAG Agent | `@n8n/n8n-nodes-langchain.agent` | Orchestrates translation task |
| Append Sheet | `n8n-nodes-base.googleSheets` | Logs result to spreadsheet |
| Slack Alert | `n8n-nodes-base.slack` | Posts to `#alerts` on agent error |
| Sticky Note | `n8n-nodes-base.stickyNote` | Canvas annotation |

## Input and output

### Webhook endpoint

```
POST /webhook/translate-form-submissions
Content-Type: application/json
```

### Sample input payload

```json
{
  "name": "María García",
  "email": "maria@example.com",
  "message": "Hola, me gustaría obtener más información sobre sus productos.",
  "target_language": "English"
}
```

### Sample output (appended to Google Sheets)

| timestamp | original_text | target_language | translated_text | status |
|---|---|---|---|---|
| 2026-10-16T09:00:00Z | Hola, me gustaría... | English | Hello, I would like... | success |

## Setup steps

1. **Import** `AI_ML/translate_form_submissions.json` into n8n via **Import from File**.
2. **OpenAI credential** — in n8n Settings → Credentials, add an `OpenAI` credential with your API key.
3. **Supabase credential** — add a `Supabase` credential (URL + service role key). Create a table named `translate_form_submissions` with pgvector enabled (`vector(1536)` column for `text-embedding-3-small`).
4. **Google Sheets credential** — add OAuth2 credential; create a sheet called `Translate Form Submissions` with a `Log` tab and columns: `timestamp`, `original_text`, `target_language`, `translated_text`, `status`. Replace `SHEET_ID` in the Append Sheet node with the real spreadsheet ID.
5. **Slack credential** — add Slack API token. Confirm `#alerts` channel exists or update the channel name in the Slack Alert node.
6. **Activate** the workflow. Test with a `curl` or Postman POST to the webhook URL.

## Supabase pgvector setup (SQL)

```sql
create extension if not exists vector;

create table translate_form_submissions (
  id bigserial primary key,
  content text,
  metadata jsonb,
  embedding vector(1536)
);

create index on translate_form_submissions
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);
```

## Common configuration caveats

- Replace `SHEET_ID` in the Append Sheet node — it's a literal placeholder.
- The agent system prompt is minimal by default; customize it to specify translation tone and style.
- `text-embedding-3-small` produces 1536-dimension vectors — match this in your Supabase table definition.
- GPT-4o billing applies per token; typical form submissions cost < $0.01 each.

## Cost estimate

| Provider | Usage per run | Approx. cost |
|---|---|---|
| OpenAI GPT-4o | ~500 input + ~200 output tokens | ~$0.005 |
| OpenAI Embeddings | ~100 tokens | < $0.001 |
| Supabase | 1 insert + 1 query | Free tier covers dev volumes |
| Google Sheets | 1 append | Free |

## Privacy notes

- Form submission content (including names and email) is sent to OpenAI for translation.
- Review OpenAI's [data usage policy](https://openai.com/policies/api-data-usage-policies) before processing regulated or sensitive PII.
- Use n8n's credential store — never embed API keys in workflow JSON.

## Safety notes

- `ai-generated-output` — review translations before using them in customer-facing responses.
- Do not use this workflow as a sole decision mechanism for consequential actions.
