# How to Ingest Data into RAG System

## Data Files Created

I've created comprehensive data files based on your live website content:

1. `htcodehub_about.txt` - About HT Code Hub
2. `htcodehub_programs.txt` - All 12 training programs
3. `htcodehub_features.txt` - Features and benefits
4. `htcodehub_statistics.txt` - Statistics and impact numbers
5. `htcodehub_contact.txt` - Contact information
6. `htcodehub_testimonials.txt` - Student testimonials
7. `htcodehub_trainers.txt` - Trainer information
8. `htcodehub_registration.txt` - Registration process
9. `htcodehub_homepage.txt` - Homepage content

All files are in: `agent/data/` directory

## Step-by-Step Ingestion

### Step 1: Start RAG API

```bash
cd agent

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Set environment variables
# Windows PowerShell:
$env:OPENAI_API_KEY="your_openai_key"
$env:AUTH_TOKEN="your_secure_token"
$env:PERSIST_DIRECTORY="./chroma"
$env:UPLOAD_FOLDER="./uploads"

# Start Flask
python app.py
```

**Wait for**: `RAG system initialized successfully`

### Step 2: Ingest Data Files

In a **NEW terminal** (keep Flask running):

```bash
cd agent
venv\Scripts\activate  # Windows

# Install requests if needed
pip install requests

# Run ingestion script
python ingest_data.py
```

The script will:
1. Check if RAG API is running
2. Find all `.txt` files in `data/` directory
3. Upload each file to the RAG system
4. Show progress and results

### Step 3: Verify Ingestion

After ingestion completes, test it:

```bash
# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"What programs do you offer?\"}"
```

You should get a detailed answer about your programs!

## What the Script Does

The `ingest_data.py` script:
- Connects to your RAG API at `http://localhost:5000`
- Finds all `.txt` files in `data/` folder
- Uploads each file using the `/ingest` endpoint
- Uses dataset name: `htcodehub`
- Shows progress for each file
- Reports success/failure

## Expected Output

```
============================================================
HT Code Hub Data Ingestion Script
============================================================

✅ RAG API is running and initialized

📁 Found 9 files to ingest:
   - htcodehub_about.txt
   - htcodehub_programs.txt
   - htcodehub_features.txt
   - htcodehub_statistics.txt
   - htcodehub_contact.txt
   - htcodehub_testimonials.txt
   - htcodehub_trainers.txt
   - htcodehub_registration.txt
   - htcodehub_homepage.txt

📄 Ingesting: htcodehub_about.txt...
   ✅ Success! Added X chunks
...

============================================================
Summary
============================================================
✅ Successfully ingested: 9/9 files

🎉 All data ingested! Your chat widget should now work.
```

## Troubleshooting

### Error: "Cannot connect to RAG API"

**Fix**: Make sure Flask is running on port 5000
```bash
# Check if running
curl http://localhost:5000/health
```

### Error: "401 Unauthorized"

**Fix**: Check `AUTH_TOKEN` matches in:
1. Flask environment variable
2. `ingest_data.py` script (or set it as env var)

### Error: "RAG system not initialized"

**Fix**: 
1. Check Flask console for errors
2. Verify `OPENAI_API_KEY` is set
3. Restart Flask

### Files Not Found

**Fix**: Make sure data files are in `agent/data/` directory:
```bash
cd agent
dir data  # Windows
ls data   # Mac/Linux
```

## After Ingestion

Once data is ingested:
1. ✅ Test chat endpoint works
2. ✅ Update Laravel `.env`: `RAG_API_URL=http://localhost:5000`
3. ✅ Test chat widget on website
4. ✅ Chat widget should now answer questions about your programs!

## Next Steps

1. **Test locally** - Make sure everything works
2. **Deploy to Render** - When ready for production
3. **Update Laravel** - Point to Render URL
4. **Monitor** - Check logs and user feedback

Your RAG system is now ready with comprehensive data about HT Code Hub! 🚀

