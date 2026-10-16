# Monetization Setup Checklist

Use this checklist to go from zero to earning. Target: **$120 in 6 months** (≈ 6 months of ChatGPT Plus).

## Step 1 — Ko-fi (takes ~10 minutes)

- [ ] Go to [ko-fi.com](https://ko-fi.com) and create a free account
- [ ] Set your page name and a short bio (e.g. "I build and maintain free n8n automation workflow templates")
- [ ] Upload a profile picture
- [ ] Set the one-time tip amount to **$5** (default is fine)
- [ ] Enable monthly supporters at **$3/month**
- [ ] Copy your Ko-fi username
- [ ] Edit `.github/FUNDING.yml` — replace `your_kofi_username` with your actual username
- [ ] Edit `SPONSORING.md` — replace the Ko-fi link with your real URL

## Step 2 — Gumroad (takes ~30 minutes)

- [ ] Go to [gumroad.com](https://gumroad.com) and create a free account
- [ ] Create **Product 1**: "n8n AI/ML Workflow Pack — Complete Setup Guide"
  - Copy description from `monetization/gumroad-product-copy.md`
  - Price: $15
  - Upload: a PDF (see Step 3 below), or a ZIP with the PDF
  - Thumbnail: screenshot of the n8n AI_ML workflow folder or a clean cover image
- [ ] Create **Product 2**: "n8n Social Media Automation Pack — Complete Setup Guide"
  - Price: $15
- [ ] Create **Product 3**: "n8n Agriculture & IoT Workflow Pack — Complete Setup Guide"
  - Price: $15
- [ ] Create **Bundle**: all 3 guides
  - Price: $35
- [ ] Copy your Gumroad profile URL
- [ ] Edit `.github/FUNDING.yml` — replace `your-gumroad-profile.gumroad.com` with your real URL
- [ ] Edit `SPONSORING.md` — replace the Gumroad link with your real URL

## Step 3 — Write the PDFs (the actual product)

The guides don't need to be long — buyers want actionable steps, not filler.

### AI/ML guide outline (~10 pages minimum, target 20)

1. Introduction — what you need before starting
2. Credential setup (one section per provider: OpenAI, Anthropic, Cohere, Google Sheets, Slack, Supabase, Pinecone, Weaviate)
3. Importing workflows into n8n
4. Per-workflow: what it does, which nodes need config, sample test payload
5. Troubleshooting table
6. Cost estimates

**Tools to write it:** Notion (export to PDF for free), Google Docs, or Canva.

### Tips for making it feel worth $15

- Include real screenshots from n8n's credential UI
- Include at least one sample JSON payload per workflow
- Include a "this took me X hours to figure out" note — buyers pay to save that time

## Step 4 — Add sponsor button to README

Edit `README.md` to add this block right after the title line:

```
---

**[☕ Support on Ko-fi](https://ko-fi.com/your_kofi_username)** · **[🛒 Premium Setup Guides on Gumroad](https://your-gumroad-profile.gumroad.com)**

---
```

- [ ] Replace both URLs with your real ones
- [ ] Commit and push

## Step 5 — Promote (where buyers actually come from)

- [ ] Post on Reddit: [r/n8n](https://www.reddit.com/r/n8n/), [r/nocode](https://www.reddit.com/r/nocode/), [r/automation](https://www.reddit.com/r/automation/)
  - Title example: "I built 54 free n8n workflow templates with docs — here's the repo"
  - Mention the free templates genuinely; don't lead with the paid guides
- [ ] Post in the [n8n community forum](https://community.n8n.io/)
- [ ] Share on Twitter/X with hashtags: #n8n #nocode #automation #AI
- [ ] Find n8n Discord servers and share (check rules first)

## Revenue math

| Scenario | Sales needed | Time to $120 |
|---|---|---|
| Ko-fi tips only ($5 avg) | 24 tips | Slow — good supplemental |
| Gumroad $15 guides only | 8 guide sales | Realistic in 1–3 months with promotion |
| Mix (2 tips + 6 guide sales) | — | $100–$110, nearly there |
| Bundle sales ($35) | 4 bundles | $140 — done |

**Most realistic path:** 1 Reddit post that gets traction → 5–10 Gumroad sales in the first month.

## Step 6 — After the first sales

- [ ] Ask buyers for feedback via Gumroad's built-in message system
- [ ] Update guides based on feedback (Gumroad lets you push updates to buyers for free)
- [ ] Add a "verified working" badge or note to the GitHub README once you've tested workflows end-to-end
