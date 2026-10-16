# Changelog

All notable changes to this repository are documented here.

This project follows a simple release policy:

- Add entries for meaningful user-facing or governance changes.
- Keep entries grouped by release.
- Keep unreleased notes at the top.

## [Unreleased]

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
