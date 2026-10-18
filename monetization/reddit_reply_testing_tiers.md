Great feedback — all of this is now addressed on `main` (commit 3439092).

**What CI covers:** JSON/schema validation, secret scanning, connection integrity, and doc/catalog coverage. It does NOT execute workflows or mock API responses — I've made that explicit in the README rather than implying more than we test.

**Testing tiers:** Replaced the old status labels with a clear three-tier system:
- Tier 1 — schema-validated (all 56 workflows)
- Tier 2 — import-tested into live n8n (0 currently)
- Tier 3 — run-tested end-to-end (0 currently)

The README now states exactly what each tier means and how it's verified. I won't promote anything to Tier 2+ without documented evidence.

**Known failure cases + minimum n8n version:** Added a troubleshooting table covering common issues (embedding dimension mismatches, auth errors, webhook 404s, placeholder IDs) and documented minimum n8n version as 1.50+.

**Clone URL:** Fixed — it was pointing to a placeholder. The repo is public at https://github.com/aziikumar07-hash/n8n-workflows

I'm currently working on getting the first workflow through Tier 3 validation locally. Thanks for the push toward honesty — it makes the library better for everyone.
