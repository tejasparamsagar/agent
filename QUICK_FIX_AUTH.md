# Quick Fix: Invalid API Key Error

## The Problem

You're getting `401 {"error":"Invalid API key"}` because the AUTH_TOKEN doesn't match.

## Solution: Use the Same Token

### Step 1: Check What Token Flask is Using

Look at your Flask console when you started it. What AUTH_TOKEN did you set?

Or check if you have a `.env` file in `agent/` folder.

### Step 2: Set the Same Token for Ingestion

**In PowerShell** (where you run ingestion):

```powershell
# Use the SAME token as Flask
$env:AUTH_TOKEN="your_token_here"

# Then run ingestion
python ingest_data.py
```

### Step 3: If You Don't Know the Token

**Option A**: Check Flask console - it shows what token it's using

**Option B**: Use the simple script that prompts you:
```bash
python ingest_data_simple.py
```

**Option C**: Set a new token in both places:

**Terminal 1 (Flask)**:
```powershell
$env:AUTH_TOKEN="htcodehub-secure-2024"
python app.py
```

**Terminal 2 (Ingestion)**:
```powershell
$env:AUTH_TOKEN="htcodehub-secure-2024"
python ingest_data.py
```

## Easiest Solution

**Create `.env` file** in `agent/` folder:

```env
OPENAI_API_KEY=your_openai_key
AUTH_TOKEN=htcodehub-secure-2024
PERSIST_DIRECTORY=./chroma
UPLOAD_FOLDER=./uploads
```

Then both Flask and ingestion will use the same token automatically!

## Test After Fix

```bash
# Should work now
python ingest_data.py
```

You should see: `✅ Success! Added X chunks` for each file.

