# Changelog

All notable changes to this repository are documented here.

This project follows a simple release policy:

- Add entries for meaningful user-facing or governance changes.
- Keep entries grouped by release.
- Keep unreleased notes at the top.

## [v0.3.0] - 2026-10-21

### Added

- `AI_ML/translate_form_submissions_ollama.json` — self-hosted Ollama variant of the translation pipeline (chat model + embeddings via local Ollama, in-memory vector store, file output). **First workflow run-tested end-to-end (Tier 3):** full execution green on n8n 2.43.7 + Ollama on Windows (2026-10-20). Setup guide documents two gotchas found during testing: use `127.0.0.1` (not `localhost`) in the Ollama credential because n8n's fetch does not fall back from IPv6 `::1`, and n8n 2.x blocks file writes outside `~/.n8n-files` unless `N8N_RESTRICT_FILE_ACCESS_TO` is set.
- Catalog entry with `status: ready` and `tested_date` for the Ollama variant; README testing-status section updated to reflect the first Tier 3 validation.
- `AI_ML/daily_content_ideas_ollama_local_test.json` — self-contained RAG content-ideas pipeline (llama3.1 + nomic-embed-text via Ollama, Document Loader → In-Memory Vector Store with a `recent_content_ideas` dedup tool, file output; no Supabase/Sheets/Slack). **Second workflow run-tested end-to-end (Tier 3):** all nodes green on n8n 2.43.7 + Ollama (2026-10-20), warm runs complete in ~23 s. The first test run exposed a design defect — chaining the vector insert node into the agent passes one item per chunk, making the agent run 16 times and log 16 duplicates — fixed by branching the insert chain as a terminal path; both the defect and its fix are documented in the setup guide.
- `monetization/RELEASE_NOTES_v0.3.0.md` — release notes for this version.

### Changed

- `README.md` rewritten for visitor clarity: explicit three-tier testing model (schema-validated → import-tested → run-tested) that plainly documents what CI does and does not verify; known-failure-cases table; minimum/tested n8n versions.
- Root README restructured to lead with a 60-second quick start and the OpenAI-powered workflow index; attribution/licensing moved below the fold.
- `.gitignore` added to keep local runtime artifacts (test logs, `node_modules`) out of the repo.

### Fixed

- Placeholder `git clone` URL in release notes corrected to the real repository URL.
- `writeBinaryFile` output path for local-test workflows corrected to a directory n8n 2.x is permitted to write to.

## [v0.2.0] - 2026-10-16

### Added

- OpenAI-focused section in root README listing all 10 OpenAI-powered workflows by model.
- Sample input/output payloads, SQL setup scripts, and cost estimates for validated workflows.
- Supabase pgvector setup SQL in per-workflow docs for `translate_form_submissions` and `daily_content_ideas`.
- `scripts/requirements.txt` for reproducible CI dependency installs.
- JSON schema validation in `scripts/validate_workflows.py` via optional `jsonschema` dependency.
- `SPONSORING.md` and `monetization/` directory with Ko-fi/Gumroad setup resources.
- `.github/FUNDING.yml` for GitHub Sponsors button.

### Changed

- `translate_form_submissions` promoted to `ready` — full node inventory, sample payloads, setup steps, and cost table documented.
- `daily_content_ideas` promoted to `ready` — full node inventory, sample payloads, customizable agent prompt, and cost table documented.
- `AI_ML/README.md` updated to highlight `ready` workflows and OpenAI model column.
- Root README rewritten to lead with OpenAI ecosystem positioning and `ready` workflow count per category.
- CI workflow now installs dependencies via `scripts/requirements.txt` before running validator.

## [v0.1.0] - 2026-10-16

### Added

- Governance/trust docs: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `THIRD_PARTY_NOTICES.md`, scoped `LICENSE`, and `ROADMAP.md`.
- Machine-readable workflow catalog at `catalog/workflows.json`.
- Per-workflow documentation under `docs/workflows/...` and docs overview.
- Validation tooling: `scripts/validate_workflows.py`, `schemas/workflow.schema.json`, and CI workflow.
- Contributor templates for issues and pull requests.

### Changed

- Root and category README files rewritten for attribution, conservative status handling, privacy guidance, and documentation links.
