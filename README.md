# n8n Free Templates (Community-Maintained)

A community-maintained collection of **55 documented n8n workflow templates** spanning AI/ML, Agriculture, IoT, Social Media, Media, Education, and Creative Content — with CI validation, per-workflow docs, and a machine-readable catalog.

---

**[⭐ Star this repo](../../stargazers)**

---

## Workflows powered by OpenAI

This repository includes **10 workflows that use the OpenAI API** directly via n8n's LangChain integration nodes (`lmChatOpenAi`, `embeddingsOpenAi`, `Whisper`). These are the most actively maintained workflows in the collection.

| Workflow | OpenAI models used | Category | Docs |
|---|---|---|---|
| [Translate Form Submissions](AI_ML/translate_form_submissions.json) | `gpt-4o`, `text-embedding-3-small` | AI_ML | [Guide](docs/workflows/ai_ml/translate_form_submissions.md) |
| [Daily Content Ideas](AI_ML/daily_content_ideas.json) | `gpt-4o` | AI_ML | [Guide](docs/workflows/ai_ml/daily_content_ideas.md) |
| [Image Captioning](AI_ML/image_captioning.json) | `gpt-4o` (vision), `text-embedding-3-small` | AI_ML | [Guide](docs/workflows/ai_ml/image_captioning.md) |
| [Product Description Generator](AI_ML/product_description_generator.json) | `gpt-4o` | AI_ML | [Guide](docs/workflows/ai_ml/product_description_generator.md) |
| [Resume Screening](AI_ML/resume_screening.json) | `gpt-4o`, `text-embedding-3-small` | AI_ML | [Guide](docs/workflows/ai_ml/resume_screening.md) |
| [Voice Note Transcription](AI_ML/voice_note_transcription.json) | `whisper-1`, `text-embedding-3-small` | AI_ML | [Guide](docs/workflows/ai_ml/voice_note_transcription.md) |
| [Video Automation (images only)](Social_Media/Video_Automation__images_only_.json) | `gpt-4o` (vision) | Social_Media | [Guide](docs/workflows/social_media/Video_Automation__images_only_.md) |
| [Alert on Instagram Competitor Story](Social_Media/alert_on_instagram_competitor_story.json) | `gpt-4o` | Social_Media | [Guide](docs/workflows/social_media/alert_on_instagram_competitor_story.md) |
| [YouTube Comment Summarizer](Social_Media/youtube_comment_summarizer.json) | `gpt-4o`, `text-embedding-3-small` | Social_Media | [Guide](docs/workflows/social_media/youtube_comment_summarizer.md) |
| [Breaking News Summarizer](Media/breaking_news_summarizer.json) | `gpt-4o`, `text-embedding-3-small` | Media | [Guide](docs/workflows/media/breaking_news_summarizer.md) |

All ten workflows use OpenAI through n8n's official `@n8n/n8n-nodes-langchain` package and follow OpenAI's credential-hygiene best practices (no hard-coded keys, placeholder-only credential IDs, secret-scanning in CI).

## Attribution and licensing context

This repository started by importing/adapting templates from [`wassupjay/n8n-free-templates`](https://github.com/wassupjay/n8n-free-templates).

- Upstream currently has **no declared GitHub license metadata**.
- Because of that, you must verify redistribution rights before reusing upstream-derived workflow JSON files.
- Attribution notices must be preserved in this repository and downstream copies.
- See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for details.

## Scope and positioning

This project is being improved toward production-oriented quality, but workflows are **not automatically production-ready**.

Initial focus areas:

1. **AI/ML** (`AI_ML/`) — 11 workflows, primary focus
2. **Agriculture** (`Agriculture/`) — 10 workflows, primary focus
3. **Business automation patterns** (cross-category automations in `Social_Media/`, `Media/`, `Education/`, and related folders)

Other categories remain available while documentation and validation coverage are expanded.

## Repository structure

- Workflow JSON files are grouped by category folders at repository root.
- Per-workflow documentation is in `docs/workflows/<category>/`.
- Machine-readable index is in `catalog/workflows.json`.
- Validation tooling is in `scripts/validate_workflows.py`.

## Workflow status labels

- `ready` — validated by maintainers in a documented environment
- `needs-configuration` — imports, but requires credential/config setup
- `experimental` — exploratory/incomplete behavior
- `not-tested` — no maintained import/run evidence
- `deprecated` — retained for reference/migration

Unless explicitly validated, statuses remain conservative.

## Catalog by category

| Category | Workflow count | Ready | Focus | Folder README |
|---|---:|---:|---|---|
| AI_ML | 11 | 0 | Primary | [AI_ML/README.md](AI_ML/README.md) |
| Agriculture | 10 | 0 | Primary | [Agriculture/README.md](Agriculture/README.md) |
| Creative_Content | 1 | 0 | Secondary | [Creative_Content/README.md](Creative_Content/README.md) |
| Education | 2 | 0 | Secondary | [Education/README.md](Education/README.md) |
| IoT | 10 | 0 | Secondary | [IoT/README.md](IoT/README.md) |
| Media | 10 | 0 | Secondary | [Media/README.md](Media/README.md) |
| Social_Media | 11 | 0 | Secondary | [Social_Media/README.md](Social_Media/README.md) |

Global catalog: [`catalog/workflows.json`](catalog/workflows.json)

## Import and configuration

1. Open n8n and import a workflow JSON file.
2. Review node parameters before first execution.
3. Configure credentials in n8n (never hard-code secrets in workflow JSON).
4. Validate third-party endpoints, index names, spreadsheet IDs, and channels.
5. Run with safe sample data first.

## Compatibility and testing policy

- Compatibility is documented as `1.x (verify in your environment)` unless a tested version is recorded.
- Do not mark a workflow as tested without import/run evidence.
- The validator checks structure, node IDs/positions, suspicious secret patterns, JSON schema conformance, and doc/catalog coverage.

Run locally:

```bash
pip install -r scripts/requirements.txt
python scripts/validate_workflows.py
```

## Privacy and safety guidance

Workflows in this repository may send data to third-party services (for example AI models, vector DBs, sheets, messaging, and cloud APIs).

Before use:

- classify data and redact sensitive fields when possible
- verify provider logging, retention, training, and regional settings
- enforce least-privilege credentials and environment-level secret storage
- avoid sending unnecessary PII to external providers

Important safeguards:

- **Resume screening and customer-impacting decisions:** do not rely on AI output as sole decision authority.
- **Agriculture/IoT workflows:** add manual approvals and fail-safe controls before real-world actuation.
- **AI-generated content:** require human review before publication or policy-sensitive actions.

## Governance, contributions, and security

- Contribution guide: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Code of conduct: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- Security policy: [`SECURITY.md`](SECURITY.md)
- Changelog: [`CHANGELOG.md`](CHANGELOG.md)
- Roadmap: [`ROADMAP.md`](ROADMAP.md)
- Documentation overview: [`docs/README.md`](docs/README.md)
- Support the project: [`SPONSORING.md`](SPONSORING.md)

## License scope

See [`LICENSE`](LICENSE). It is intentionally scoped to original repository documentation/scripts/metadata and does **not** claim rights over upstream-derived workflow JSON where licensing is uncertain.
