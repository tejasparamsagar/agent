# Fix "Invalid API key" Error

## The Problem

You're getting `401 {"error":"Invalid API key"}` when trying to ingest data.

This means the `AUTH_TOKEN` in the ingestion script doesn't match the `AUTH_TOKEN` in your Flask app.

## Quick Fix

### Option 1: Set AUTH_TOKEN Environment Variable

**In the terminal where Flask is running**, make sure you set:
```powershell
$env:AUTH_TOKEN="your_secure_token_here"
```

**In the terminal where you run ingestion**, set the SAME token:
```powershell
$env:AUTH_TOKEN="your_secure_token_here"
python ingest_data.py
```

### Option 2: Use the Simple Script (Easier)

Use the new script that prompts for the token:

```bash
python ingest_data_simple.py
```

It will ask you to enter the AUTH_TOKEN if not found.

### Option 3: Check What Token Flask is Using

**In Flask console**, you should see what AUTH_TOKEN is being used. Or check:

1. What you set when starting Flask:
   ```powershell
   $env:AUTH_TOKEN="your_token"
   ```

2. Or check if there's a `.env` file in `agent/` folder

### Option 4: Use the Same Token Everywhere

**Step 1**: Choose a token (e.g., `my-secure-token-123`)

**Step 2**: Set it when starting Flask:
```powershell
$env:AUTH_TOKEN="my-secure-token-123"
python app.py
```

**Step 3**: Set it when running ingestion:
```powershell
$env:AUTH_TOKEN="my-secure-token-123"
python ingest_data.py
```

## Recommended: Create .env File

Create `agent/.env` file:

```env
OPENAI_API_KEY=your_openai_key
AUTH_TOKEN=my-secure-token-123
PERSIST_DIRECTORY=./chroma
UPLOAD_FOLDER=./uploads
```

Then both Flask and ingestion script will use the same token automatically.

## Test the Token

After setting the token, test it:

```bash
curl -X POST http://localhost:5000/ingest \
  -H "X-API-Key: your_token_here" \
  -F "dataset_name=test" \
  -F "file=@data/htcodehub_about.txt"
```

If it works, the token is correct!

## Quick Solution

**Easiest way** - Use the same token in both terminals:

```powershell
# Terminal 1 (Flask)
$env:AUTH_TOKEN="htcodehub-2024"
python app.py

# Terminal 2 (Ingestion)
$env:AUTH_TOKEN="htcodehub-2024"
python ingest_data.py
```

Make sure both use the **exact same token**!

