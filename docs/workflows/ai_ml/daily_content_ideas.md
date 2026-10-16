# Daily Content Ideas

- **Workflow file:** `AI_ML/daily_content_ideas.json`
- **Status:** `ready`
- **Tested date:** 2026-10-16
- **n8n compatibility:** 1.x
- **Source:** Adapted/imported from `wassupjay/n8n-free-templates` (license status uncertain; verify rights before redistribution)

## Purpose

Triggered by a webhook (schedulable via n8n's Schedule Trigger), this workflow uses **OpenAI GPT-4o** to generate a batch of content ideas for a given topic or brand, stores embeddings via **Cohere** in a **Supabase** vector store to avoid duplicates over time, logs results to **Google Sheets**, and posts the idea list to **Slack**.

Typical use cases: daily editorial calendars, social media content planning, blog topic generation for content teams.

## Required n8n compatibility

- n8n `1.x` — tested on 1.x self-hosted

## Required services and credentials

| Credential | n8n credential type | Used by |
|---|---|---|
| OpenAI API key | `openAiApi` | Chat model (GPT-4o) |
| Cohere API key | `cohereApi` | Embeddings for deduplication |
| Supabase | `supabaseApi` | Vector store (insert + query) |
| Google Sheets OAuth2 | `googleSheetsOAuth2Api` | Log append |
| Slack API | `slackApi` | Posts idea list + error alerts |

## Node inventory

| Node name | Type | Purpose |
|---|---|---|
| Webhook Trigger | `n8n-nodes-base.webhook` | Receives POST at `/daily-content-ideas` |
| Text Splitter | `@n8n/n8n-nodes-langchain.textSplitterCharacterTextSplitter` | Chunks topic context |
| Embeddings | `@n8n/n8n-nodes-langchain.embeddingsCohere` | Cohere embed-english-v3.0 |
| Supabase Insert | `@n8n/n8n-nodes-langchain.vectorStoreSupabase` | Stores embedding in `daily_content_ideas` index |
| Supabase Query | `@n8n/n8n-nodes-langchain.vectorStoreSupabase` | Retrieves recent ideas to avoid duplication |
| Vector Tool | `@n8n/n8n-nodes-langchain.toolVectorStore` | Wraps Supabase for agent |
| Window Memory | `@n8n/n8n-nodes-langchain.memoryBufferWindow` | Short-term agent memory |
| Chat Model | `@n8n/n8n-nodes-langchain.lmChatOpenAi` | GPT-4o idea generation |
| RAG Agent | `@n8n/n8n-nodes-langchain.agent` | Orchestrates generation + deduplication |
| Append Sheet | `n8n-nodes-base.googleSheets` | Logs ideas to spreadsheet |
| Slack Alert | `n8n-nodes-base.slack` | Posts ideas to `#content` (or alerts on error) |
| Sticky Note | `n8n-nodes-base.stickyNote` | Canvas annotation |

## Input and output

### Webhook endpoint

```
POST /webhook/daily-content-ideas
Content-Type: application/json
```

### Sample input payload

```json
{
  "topic": "sustainable packaging for e-commerce",
  "audience": "small business owners",
  "count": 5,
  "formats": ["blog post", "short video", "LinkedIn carousel"]
}
```

### Sample Slack output

```
📝 Daily Content Ideas — sustainable packaging for e-commerce

1. [Blog] "5 Affordable Sustainable Packaging Swaps for Small Online Stores"
2. [Video] Behind-the-scenes: how we switched to compostable mailers in 30 days
3. [Carousel] The real cost of plastic vs. recycled packaging (with numbers)
4. [Blog] Supplier guide: where to source eco-friendly packaging in bulk
5. [Video] Customer unboxing reactions when you go sustainable
```

## Setup steps

1. **Import** `AI_ML/daily_content_ideas.json` into n8n via **Import from File**.
2. **OpenAI credential** — add an `OpenAI` credential with your API key.
3. **Cohere credential** — add a `Cohere` credential with your API key (free trial tier works for development).
4. **Supabase credential** — add Supabase credential. Create the vector table (see SQL below). Cohere `embed-english-v3.0` produces 1024-dimension vectors.
5. **Google Sheets credential** — add OAuth2 credential; create a sheet called `Daily Content Ideas` with a `Log` tab. Replace `SHEET_ID` in the Append Sheet node.
6. **Slack credential** — add Slack API token. Update the channel in the Slack Alert node (default `#alerts`).
7. **Schedule it** — optionally replace the Webhook Trigger with n8n's Schedule Trigger node set to run every morning.
8. **Activate** and test with a POST to the webhook URL.

## Supabase pgvector setup (SQL)

```sql
create extension if not exists vector;

create table daily_content_ideas (
  id bigserial primary key,
  content text,
  metadata jsonb,
  embedding vector(1024)
);

create index on daily_content_ideas
  using ivfflat (embedding vector_cosine_ops)
  with (lists = 100);
```

## Customizing the agent prompt

The RAG Agent's system message defaults to `"You are an assistant for Daily Content Ideas"`. Replace it with something like:

```
You are a content strategist for a sustainable e-commerce brand. 
Generate {count} unique, actionable content ideas for the topic provided.
Check the vector store for recently generated ideas and avoid duplicating them.
Format output as a numbered list with the content format in brackets.
```

## Cost estimate

| Provider | Usage per run | Approx. cost |
|---|---|---|
| OpenAI GPT-4o | ~300 input + ~400 output tokens | ~$0.005 |
| Cohere Embeddings | ~100 tokens | Free tier / < $0.001 |
| Supabase | 1 insert + 1 query | Free tier covers dev volumes |
| Google Sheets | 1 append | Free |

## Privacy notes

- Topic and brand context is sent to OpenAI for generation.
- No PII is expected in this workflow's typical inputs.
- Review OpenAI's [data usage policy](https://openai.com/policies/api-data-usage-policies) if brand information is commercially sensitive.

## Safety notes

- `ai-generated-output` — review generated ideas before publishing.
- AI-generated content should go through editorial review before public posting.
