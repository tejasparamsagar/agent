# Quick Setup Guide

## Step 1: Create .env File

Copy `env_template.txt` to `.env` and add your credentials:

```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
AUTH_TOKEN=my-secure-token-123
PERSIST_DIRECTORY=./chroma
UPLOAD_FOLDER=./uploads
DEBUG=False
```

## Step 2: Restart the App

Stop the current Flask app (Ctrl+C) and restart:

```bash
python app.py
```

## Step 3: Verify Health Check

Visit: `http://127.0.0.1:5000/health`

You should see:
```json
{
  "rag_initialized": true,
  "status": "running"
}
```

## Step 4: Test Document Ingestion

### Using cURL:
```bash
curl -X POST http://127.0.0.1:5000/ingest \
  -H "X-API-Key: my-secure-token-123" \
  -F "dataset_name=test-data" \
  -F "file=@sample.txt"
```

### Using Postman/Thunder Client:
- Method: POST
- URL: `http://127.0.0.1:5000/ingest`
- Headers: `X-API-Key: my-secure-token-123`
- Body: form-data
  - `dataset_name`: test-data
  - `file`: [select your PDF/TXT/DOCX file]

## Step 5: Test Query

```bash
curl -X POST http://127.0.0.1:5000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: my-secure-token-123" \
  -d '{
    "question": "What is this document about?",
    "dataset_name": "test-data"
  }'
```

## Troubleshooting

### If `rag_initialized` is still `false`:
1. Check that `.env` file exists in the project root
2. Verify `OPENAI_API_KEY` is set correctly
3. Restart the Flask app after creating `.env`
4. Check the terminal for error messages

### If you get authentication errors:
- Make sure `AUTH_TOKEN` in `.env` matches the token in your request headers

### If document ingestion fails:
- Check file size (max 15MB)
- Verify file type (PDF, TXT, or DOCX)
- Check terminal logs for detailed error messages

