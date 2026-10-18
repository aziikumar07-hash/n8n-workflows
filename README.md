# 56 Free n8n Workflow Templates — AI, Agriculture, IoT, Social Media

**Import into n8n → add your API key → run.** No paid tools required. Every workflow ships with a setup guide, sample payloads, and a troubleshooting section.

[![CI](https://github.com/aziikumar07-hash/n8n-workflows/actions/workflows/validate-workflows.yml/badge.svg)](https://github.com/aziikumar07-hash/n8n-workflows/actions/workflows/validate-workflows.yml)
[![n8n](https://img.shields.io/badge/n8n-1.50%2B-orange)](https://n8n.io)
[![Workflows](https://img.shields.io/badge/workflows-56-blue)](catalog/workflows.json)
[![Docs](https://img.shields.io/badge/docs-56%2F56-brightgreen)](docs/README.md)

---

## Quick start (60 seconds)

1. **Download** any workflow JSON from this repo
2. **Open n8n** → click **Import from File** → select the JSON
3. **Click each node** that shows a credential icon → attach your API key
4. **Test workflow** → done

That's it. Every workflow has a **[detailed setup guide](docs/README.md)** with step-by-step instructions, sample test payloads, and cost estimates.

---

## 10 AI Workflows (OpenAI-powered)

These use OpenAI directly through n8n's built-in LangChain nodes. Just add your OpenAI API key.

| Workflow | What it does | Setup guide |
|---|---|---|
| [Translate Form Submissions](AI_ML/translate_form_submissions.json) | Auto-translate inbound form responses | [Guide](docs/workflows/ai_ml/translate_form_submissions.md) |
| [Daily Content Ideas](AI_ML/daily_content_ideas.json) | Generate daily content ideas from trends | [Guide](docs/workflows/ai_ml/daily_content_ideas.md) |
| [Daily Content Ideas (Ollama)](AI_ML/daily_content_ideas_ollama.json) | Same, runs on local Ollama — zero API cost | [Guide](docs/workflows/ai_ml/daily_content_ideas_ollama.md) |
| [Image Captioning](AI_ML/image_captioning.json) | Auto-generate alt text and captions for images | [Guide](docs/workflows/ai_ml/image_captioning.md) |
| [Product Description Generator](AI_ML/product_description_generator.json) | Turn product specs into marketing copy | [Guide](docs/workflows/ai_ml/product_description_generator.md) |
| [Resume Screening](AI_ML/resume_screening.json) | Score and tag resumes against a job description | [Guide](docs/workflows/ai_ml/resume_screening.md) |
| [Voice Note Transcription](AI_ML/voice_note_transcription.json) | Whisper transcription → structured summary | [Guide](docs/workflows/ai_ml/voice_note_transcription.md) |
| [YouTube Comment Summarizer](Social_Media/youtube_comment_summarizer.json) | Summarize video comments into themes | [Guide](docs/workflows/social_media/youtube_comment_summarizer.md) |
| [Breaking News Summarizer](Media/breaking_news_summarizer.json) | RSS → concise news briefings | [Guide](docs/workflows/media/breaking_news_summarizer.md) |
| [Instagram Competitor Alerts](Social_Media/alert_on_instagram_competitor_story.json) | Monitor competitor stories, get notified | [Guide](docs/workflows/social_media/alert_on_instagram_competitor_story.md) |

**Prefer local models?** The [Ollama variant](AI_ML/daily_content_ideas_ollama.json) runs entirely on your machine with zero API costs.

---

## All categories

| Category | Workflows | Best for |
|---|---:|---|
| [AI_ML](AI_ML/README.md) | 12 | Content generation, transcription, screening |
| [Agriculture](Agriculture/README.md) | 10 | Crop monitoring, equipment alerts, yield prediction |
| [IoT](IoT/README.md) | 10 | Sensor data, device logs, predictive maintenance |
| [Social_Media](Social_Media/README.md) | 11 | Cross-posting, comment moderation, reporting |
| [Media](Media/README.md) | 10 | News summarization, podcast notes, PR monitoring |
| [Education](Education/README.md) | 2 | Quiz grading, student engagement |
| [Creative_Content](Creative_Content/README.md) | 1 | YouTube transcript → blog post |

Full catalog with status, providers, and credential requirements: [`catalog/workflows.json`](catalog/workflows.json)

---

## What's included with each workflow

- **Workflow JSON** — ready to import into n8n
- **Setup guide** — step-by-step docs with credential setup, sample payloads, and cost estimates
- **Troubleshooting** — common failure modes and fixes
- **Catalog entry** — machine-readable metadata (providers, credentials, webhook paths)

## Quality assurance

Every workflow passes CI validation on every push:
- Valid n8n JSON structure (schema-validated)
- No hard-coded secrets or API keys (secret-scanning)
- All node connections resolve correctly
- Every workflow has a doc file and catalog entry

**Current testing status:** All 56 workflows are schema-validated. Import/run testing is in progress — see [ROADMAP.md](ROADMAP.md) for the testing plan.

## Requirements

- **n8n** 1.50 or later (self-hosted or cloud)
- **API keys** for whichever services a workflow uses (OpenAI, Google Sheets, Slack, etc.)
- Each setup guide lists the exact credentials needed

## Known issues

| Problem | Fix |
|---|---|
| Node shows "unknown type" on import | Update n8n to 1.50+ |
| Auth error on AI nodes | Re-attach your credential to each AI node |
| Embedding dimension mismatch | Match model to vector store (e.g. `text-embedding-3-small` = 1536, `nomic-embed-text` = 768) |
| Webhook returns 404 | Click "Test workflow" before sending test requests |

## Contributing

Found a bug? Want to add a workflow? See [CONTRIBUTING.md](CONTRIBUTING.md).

**⭐ If these workflows save you time, star the repo** — it helps others find them and tells me to keep maintaining them.

## Attribution

Started by adapting templates from [`wassupjay/n8n-free-templates`](https://github.com/wassupjay/n8n-free-templates). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for licensing details.

## License

See [LICENSE](LICENSE). Documentation and scripts are MIT-licensed. Some workflow JSONs may derive from upstream sources with unclear licensing — verify redistribution rights before reuse.

---

**[Support this project](SPONSORING.md)** · **[Report an issue](https://github.com/aziikumar07-hash/n8n-workflows/issues)** · **[View all docs](docs/README.md)**
