# OpenAI API Quota Exceeded - Solutions

## Problem
You're getting this error:
```
Error code: 429 - You exceeded your current quota, please check your plan and billing details.
Type: RateLimitError / insufficient_quota
```

This means your OpenAI API key has run out of credits.

## Solutions

### Option 1: Add Credits to OpenAI Account (Recommended)
1. Go to https://platform.openai.com/account/billing
2. Add payment method or add credits
3. Wait a few minutes for the quota to update
4. Try ingesting again

### Option 2: Use a Different API Key
1. Get a new API key from https://platform.openai.com/api-keys
2. Update your `.env` file:
   ```
   OPENAI_API_KEY=sk-proj-your-new-key-here
   ```
3. Restart Flask app
4. Try ingesting again

### Option 3: Check Your Usage
1. Go to https://platform.openai.com/usage
2. Check your current usage and limits
3. See when your quota resets (if on a free tier)

### Option 4: Use a Different Embedding Model (Advanced)
If you want to avoid OpenAI costs, you could switch to a local embedding model, but this requires more setup.

## Quick Check
To verify your API key status:
```powershell
# Test your API key directly
python -c "import openai; import os; from dotenv import load_dotenv; load_dotenv(); openai.api_key = os.getenv('OPENAI_API_KEY'); print('Key valid' if openai.api_key else 'Key missing')"
```

## After Fixing
Once you have credits:
1. Restart Flask app (if needed)
2. Run ingestion again:
   ```powershell
   cd agent
   $env:AUTH_TOKEN="htcodehub-2024"
   python ingest_data.py
   ```

## Note
The RAG system uses OpenAI embeddings to convert your documents into vectors. Each document chunk requires an API call, so ingesting 9 files with multiple chunks each will use some credits. Make sure you have sufficient quota before ingesting.

