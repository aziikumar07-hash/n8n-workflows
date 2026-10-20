# Roadmap

## Milestone 1 - Trust baseline (complete)

- [x] Attribution and third-party notice policy
- [x] Scoped license for original repository materials
- [x] Governance files and contribution templates
- [x] Workflow catalog + docs coverage baseline
- [x] JSON/structure/coverage validation in CI

## Milestone 2 - Quality hardening (in progress)

- [x] JSON schema validation integrated into CI (`jsonschema` via `scripts/requirements.txt`)
- [x] First two workflows promoted to `ready` with full setup docs, sample payloads, and SQL scripts (`translate_form_submissions`, `daily_content_ideas`)
- [x] First workflow run-tested end-to-end (Tier 3): `translate_form_submissions_ollama` — full pipeline green on n8n 2.43.7 + Ollama (2026-10-20); findings documented in its setup guide (use `127.0.0.1` not `localhost` for Ollama; n8n 2.x requires `N8N_RESTRICT_FILE_ACCESS_TO` for out-of-tree file writes)
- [ ] Validate remaining AI/ML and Social Media priority workflows end-to-end in n8n 1.x
- [ ] Promote additional verified workflows to `ready`
- [ ] Add category-level compatibility notes and known limitations to all category READMEs
- [ ] Add safer default error handling/retry guidance in docs

## Milestone 3 - Community and maintenance

- [ ] Enable GitHub Discussions (manual repository setting)
- [ ] Maintain issue triage labels and response SLA notes
- [ ] Publish tagged releases with changelog updates
- [ ] Collect compatibility reports from contributors/users
