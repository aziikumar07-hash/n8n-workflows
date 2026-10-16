# OpenAI Codex for Open Source — Application Narrative

> Use this as the basis for your application at https://openai.com/form/codex-open-source
> Fill in the bracketed fields with your actual GitHub username and stats before submitting.

---

## Project name

n8n Free Templates (Community-Maintained)

## Repository URL

https://github.com/[your-github-username]/n8n-free-templates

## Brief description (1–2 sentences)

A community-maintained collection of 54 documented n8n workflow automation templates, with 10 workflows powered directly by the OpenAI API. The project includes CI validation, per-workflow documentation, a machine-readable catalog, and safety guidance for production use.

---

## Long description / application narrative

### What the project does

This repository provides free, documented n8n workflow templates that help developers and teams build automation pipelines using AI APIs — including OpenAI — without starting from scratch.

n8n is an open-source workflow automation platform with over 90,000 GitHub stars and a large self-hosted community. Our templates specifically target the LangChain-style integration nodes in n8n (`@n8n/n8n-nodes-langchain`), which provide first-class support for OpenAI's models including GPT-4o, text-embedding-3-small, and Whisper.

### OpenAI integration

**10 of our 54 workflow templates use the OpenAI API directly:**

| Workflow | Models |
|---|---|
| Translate Form Submissions | GPT-4o, text-embedding-3-small |
| Daily Content Ideas | GPT-4o |
| Image Captioning | GPT-4o (vision), text-embedding-3-small |
| Product Description Generator | GPT-4o |
| Resume Screening | GPT-4o, text-embedding-3-small |
| Voice Note Transcription | whisper-1, text-embedding-3-small |
| Video Automation | GPT-4o (vision) |
| Alert on Instagram Competitor Story | GPT-4o |
| YouTube Comment Summarizer | GPT-4o, text-embedding-3-small |
| Breaking News Summarizer | GPT-4o, text-embedding-3-small |

All workflows use OpenAI credentials through n8n's official credential manager (never hard-coded), are scanned for secret leakage in CI, and include guidance on OpenAI's data usage policy.

### Production quality focus

We treat this as infrastructure, not just a template dump:

- **CI validation** on every push: JSON structure, schema conformance, duplicate node IDs, suspicious secret patterns, and catalog/doc coverage — all checked automatically via GitHub Actions
- **Validated workflows** have full setup documentation including: node inventory tables, sample JSON payloads, Supabase SQL scripts, step-by-step credential setup, and per-provider cost estimates
- **Safety guidance** for every workflow: PII flags, AI-output review requirements, physical-world impact warnings for IoT/Agriculture workflows
- **Conservative status labels**: nothing is marked `ready` without actual validation evidence

### Community positioning

- n8n has a large, growing community actively looking for workflow templates
- No equivalent repository exists with this combination of: OpenAI-native workflows + CI validation + per-workflow documentation + machine-readable catalog
- The project is designed to be contributed to — with issue templates, a PR checklist, a code of conduct, and a contribution guide

### How OpenAI Pro access would be used

Access to ChatGPT Pro and the Codex API would directly accelerate:

1. **End-to-end workflow validation** — using GPT-4o to test and refine the 10 OpenAI-powered workflows against realistic payloads, improving the accuracy of our documentation and sample data
2. **Documentation quality** — generating and reviewing setup guides for the remaining 44 workflows, particularly for complex RAG patterns
3. **New OpenAI-native workflows** — building and documenting additional workflows using newer OpenAI capabilities (structured outputs, Assistants API, real-time API patterns) that would benefit the n8n community

### Ecosystem impact

Every developer who finds this repository and successfully deploys an OpenAI-powered n8n workflow becomes an ongoing OpenAI API user. This project is effectively a free onboarding resource for OpenAI's API within the n8n community.

---

## Key metrics to include (fill in before submitting)

- GitHub stars: [current count]
- Forks: [current count]
- Open issues / PRs: [current count]
- Unique workflows: 54 (10 OpenAI-native)
- Validated workflows: 2 (growing)
- CI: passing ✅
- License: original materials under MIT-style scoped license

---

## Links to include in application

- Repository: https://github.com/[your-github-username]/n8n-free-templates
- CI workflow: https://github.com/[your-github-username]/n8n-free-templates/actions
- Example validated workflow doc: https://github.com/[your-github-username]/n8n-free-templates/blob/main/docs/workflows/ai_ml/translate_form_submissions.md
- Catalog: https://github.com/[your-github-username]/n8n-free-templates/blob/main/catalog/workflows.json

---

## Tips for submitting

1. **Submit after getting some stars** — even 20–30 stars makes the project look active. Post on r/n8n first.
2. **Link to the CI badge** — it shows the project is maintained, not abandoned.
3. **Mention the n8n community size** in your own words — "n8n has 90k+ GitHub stars and a large self-hosted community" is the context OpenAI needs.
4. **Be specific about usage** — "I will use API credits to validate workflow X against payload Y" is stronger than "I will build things."
5. **Keep the form answer concise** — use this narrative as source material, not a copy-paste. Hit the key points: 54 templates, 10 use OpenAI directly, CI validation, community impact.
