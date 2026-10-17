# Local Test Guide — Translate Form Submissions

Run and validate this workflow entirely on your PC.
**Only external service needed: your OpenAI API key.**

---

## What you need

- Windows PC (you have this)
- Node.js 24 (already installed — confirmed)
- OpenAI API key

That's it. No Docker, no Supabase account, no Google account, no Slack.

---

## Step 1 — Start n8n

Open a terminal (PowerShell or CMD) and run:

```powershell
npx n8n
```

First run downloads n8n (~200 MB). Wait until you see:

```
Editor is now accessible via:
http://localhost:5678
```

Open **http://localhost:5678** in your browser. Create a local account when prompted (email + password, stored only on your PC).

---

## Step 2 — Add your OpenAI credential

1. In n8n, go to **Settings → Credentials → Add credential**
2. Search for `OpenAI`
3. Paste your API key
4. Name it exactly: **`OpenAI`**
5. Click Save

---

## Step 3 — Import the test workflow

1. In n8n, click **+** (new workflow) → **Import from File**
2. Select: `AI_ML/translate_form_submissions_local_test.json`
3. The workflow opens — you'll see 9 nodes

---

## Step 4 — Attach your OpenAI credential

Two nodes need it. Click each and select your credential:

- **Embeddings** node → OpenAI credential
- **Chat Model** node → OpenAI credential

The model is pre-set to `gpt-4o-mini` (cheaper than gpt-4o, fine for testing — costs < $0.001 per run).

---

## Step 5 — Test it

In n8n, click **Test workflow** (top right). This puts the webhook in test mode.

Then in a **second PowerShell window**, send a test request:

```powershell
Invoke-RestMethod -Uri "http://localhost:5678/webhook-test/translate-form-submissions-local" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"message": "Hola, necesito ayuda con mi pedido numero 1234", "target_language": "English"}'
```

---

## Step 6 — Watch it run

Back in n8n you'll see each node light up green as it executes:

```
Webhook Trigger → Text Splitter → Embeddings → Vector Store → Translation Agent → Save to File
```

Click any node to see its input/output data. The Translation Agent output should contain the English translation.

The result also gets written to:
```
C:\Users\Administrator\Desktop\translations_log.json
```

---

## Expected output

The Translation Agent node output should look like:

```json
{
  "output": "Hello, I need help with my order number 1234"
}
```

---

## Try a few more languages

```powershell
# French → English
Invoke-RestMethod -Uri "http://localhost:5678/webhook-test/translate-form-submissions-local" `
  -Method POST -ContentType "application/json" `
  -Body '{"message": "Bonjour, je voudrais retourner mon colis", "target_language": "English"}'

# English → Spanish
Invoke-RestMethod -Uri "http://localhost:5678/webhook-test/translate-form-submissions-local" `
  -Method POST -ContentType "application/json" `
  -Body '{"message": "Please cancel my subscription", "target_language": "Spanish"}'

# Japanese → English
Invoke-RestMethod -Uri "http://localhost:5678/webhook-test/translate-form-submissions-local" `
  -Method POST -ContentType "application/json" `
  -Body '{"message": "注文をキャンセルしたいです", "target_language": "English"}'
```

---

## Once it works

1. Screenshot the successful execution (green nodes + output visible)
2. Note today's date and n8n version (shown in Settings → About)
3. Update the catalog entry:
   - `status`: `ready`
   - `tested_date`: today's date
4. Update the doc header too

The test variant (`_local_test.json`) stays in the repo as a zero-friction onramp for contributors who want to validate without setting up cloud services.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `npx n8n` hangs | Try `npx n8n start` instead |
| Webhook not receiving | Make sure you clicked **Test workflow** before sending the curl |
| OpenAI credential error | Double-check the key has billing enabled at platform.openai.com |
| `writeBinaryFile` error | The Save to File node can be disabled — right-click → Disable. The translation still works. |
