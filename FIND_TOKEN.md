# Find Your AUTH_TOKEN

## From Your Flask Console

Looking at your Flask output, Flask is running but **AUTH_TOKEN is not shown in logs**.

## Default Token

If you didn't set `AUTH_TOKEN` when starting Flask, it's using:
```
default-token-change-in-production
```

This is the default value in `config.py`.

## Solution: Use the Default Token

**In PowerShell** (where you run ingestion):

```powershell
$env:AUTH_TOKEN="default-token-change-in-production"
python ingest_data.py
```

## Better Solution: Set a Custom Token

**Terminal 1 (Flask)** - Stop Flask (Ctrl+C), then:

```powershell
$env:AUTH_TOKEN="htcodehub-2024"
python app.py
```

**Terminal 2 (Ingestion)**:

```powershell
$env:AUTH_TOKEN="htcodehub-2024"
python ingest_data.py
```

## Check What Token Flask is Using

Run this in a new terminal:

```powershell
cd agent
python check_auth_token.py
```

This will show you exactly what token Flask is using.

## Quick Fix Right Now

Since Flask is already running with the default token, just use it:

```powershell
$env:AUTH_TOKEN="default-token-change-in-production"
python ingest_data.py
```

This should work immediately!

