# AI_ML Workflows

- Focus area: **yes** (primary)
- Catalog: [`catalog/workflows.json`](../catalog/workflows.json)
- Docs directory: [`docs/workflows/ai_ml/`](../docs/workflows/ai_ml/)

| Workflow | Status | OpenAI models | Providers | Documentation |
|---|---|---|---|---|
| `translate_form_submissions.json` | `needs-configuration` | GPT-4o, text-embedding-3-small | OpenAI, Google Sheets, Slack, Supabase | [Guide](../docs/workflows/ai_ml/translate_form_submissions.md) |
| `translate_form_submissions_ollama.json` | `ready` (run-tested 2026-10-20) | — (self-hosted) | Ollama only (in-memory vector store) | [Guide](../docs/workflows/ai_ml/translate_form_submissions_ollama.md) |
| `daily_content_ideas.json` | `needs-configuration` | GPT-4o | OpenAI, Cohere, Google Sheets, Slack, Supabase | [Guide](../docs/workflows/ai_ml/daily_content_ideas.md) |
| `daily_content_ideas_ollama.json` | `needs-configuration` | — (self-hosted) | Ollama, Google Sheets, Slack, Supabase | [Guide](../docs/workflows/ai_ml/daily_content_ideas_ollama.md) |
| `translate_form_submissions_local_test.json` | `needs-configuration` | gpt-4o-mini, text-embedding-3-small | OpenAI only (in-memory vector store) | [Local test guide](../docs/workflows/ai_ml/local_test_guide.md) |
| `customer_sentiment_analysis.json` | `needs-configuration` | — | Anthropic, Cohere, Google Sheets, Pinecone, ... | [Guide](../docs/workflows/ai_ml/customer_sentiment_analysis.md) |
| `image_captioning.json` | `needs-configuration` | GPT-4o (vision), text-embedding-3-small | Anthropic, Google Sheets, OpenAI, Slack, ... | [Guide](../docs/workflows/ai_ml/image_captioning.md) |
| `product_description_generator.json` | `needs-configuration` | GPT-4o | Anthropic, Cohere, Google Sheets, Pinecone, ... | [Guide](../docs/workflows/ai_ml/product_description_generator.md) |
| `resume_screening.json` | `needs-configuration` | GPT-4o, text-embedding-3-small | Cohere, Google Sheets, OpenAI, Slack, ... | [Guide](../docs/workflows/ai_ml/resume_screening.md) |
| `summarize_customer_emails.json` | `needs-configuration` | — | Anthropic, Cohere, Google Sheets, Slack, ... | [Guide](../docs/workflows/ai_ml/summarize_customer_emails.md) |
| `ticket_urgency_classification.json` | `needs-configuration` | — | Anthropic, Cohere, Google Sheets, Pinecone, ... | [Guide](../docs/workflows/ai_ml/ticket_urgency_classification.md) |
| `voice_note_transcription.json` | `needs-configuration` | whisper-1, text-embedding-3-small | Cohere, Google Sheets, OpenAI, Slack, ... | [Guide](../docs/workflows/ai_ml/voice_note_transcription.md) |
