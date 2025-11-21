# Migration to Groq LLM + HuggingFace Embeddings

## ✅ Changes Completed

Your Flask RAG project has been successfully upgraded to use:
- **Groq LLM** (FREE) - Replaces OpenAI ChatOpenAI
- **HuggingFace Embeddings** (FREE) - Replaces OpenAI Embeddings

## 📝 Files Updated

### Core Files
1. ✅ `rag/embedder.py` - Now uses HuggingFaceEmbeddings
2. ✅ `rag/retriever.py` - Now uses ChatGroq (llama3-70b-8192)
3. ✅ `config.py` - Changed from OPENAI_API_KEY to GROQ_API_KEY
4. ✅ `app.py` - Removed OpenAI error messages
5. ✅ `rag_engine.py` - Updated to use Groq + HuggingFace
6. ✅ `requirements.txt` - Added langchain-groq, transformers, sentence-transformers
7. ✅ `render.yaml` - Updated to use GROQ_API_KEY

## 🚀 Next Steps

### 1. Install New Dependencies

```powershell
cd agent
pip install -r requirements.txt
```

This will install:
- `langchain-groq` - For Groq LLM
- `transformers` - For HuggingFace models
- `sentence-transformers` - For embeddings
- `torch` - Required for transformers

**Note:** First-time installation may take a few minutes as it downloads the embedding model (~90MB).

### 2. Get Your FREE Groq API Key

1. Go to https://console.groq.com/
2. Sign up (it's free!)
3. Navigate to API Keys: https://console.groq.com/keys
4. Create a new API key
5. Copy the key

### 3. Update Your .env File

Update your `.env` file in the `agent` directory:

```env
# Groq Configuration (REQUIRED)
GROQ_API_KEY=gsk_your_groq_api_key_here

# Authentication Token (REQUIRED)
AUTH_TOKEN=htcodehub-2024

# Storage Directories
PERSIST_DIRECTORY=./chroma
UPLOAD_FOLDER=./uploads

# Flask Configuration
DEBUG=False
SECRET_KEY=dev-secret-key-change-in-production

# Optional: Data directory
RAG_HOME=./data
```

**Important:** Remove any `OPENAI_API_KEY` line from your `.env` file.

### 4. Test the System

#### Start Flask App:
```powershell
cd agent
python app.py
```

You should see:
```
HuggingFace embeddings initialized
Retriever initialized with Groq LLM
RAG system initialized successfully
```

#### Test Health Endpoint:
```powershell
# In another terminal
curl http://localhost:5000/health
```

#### Ingest Your Data:
```powershell
cd agent
$env:AUTH_TOKEN="htcodehub-2024"
python ingest_data.py
```

**Note:** The first ingestion will download the embedding model, which may take a few minutes. Subsequent runs will be faster.

### 5. Test a Query

```powershell
curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d '{"query":"What is HT Code Hub?"}'
```

## 🎯 Benefits

1. **FREE** - No API costs for embeddings (runs locally)
2. **FREE** - Groq offers generous free tier for LLM
3. **Fast** - Groq is optimized for speed
4. **Offline** - Embeddings work offline (after initial download)
5. **No Quota Issues** - No more OpenAI quota errors!

## ⚠️ Important Notes

1. **First Run**: The first time you run the app, it will download the `all-MiniLM-L6-v2` model (~90MB). This is a one-time download.

2. **Model Location**: The model will be cached in your home directory under `.cache/huggingface/`. This is normal.

3. **Memory**: HuggingFace embeddings require some RAM. Make sure you have at least 2GB free.

4. **Groq Rate Limits**: Groq has rate limits on the free tier, but they're very generous. Check https://console.groq.com/docs/rate-limits

5. **ChromaDB**: Your existing ChromaDB data will need to be re-indexed because embeddings are different. Delete the `chroma` folder and re-ingest your data.

## 🔄 Re-indexing Your Data

Since embeddings changed, you need to re-index:

```powershell
# Delete old ChromaDB (optional, but recommended)
Remove-Item -Recurse -Force agent\chroma

# Re-ingest your data
cd agent
$env:AUTH_TOKEN="htcodehub-2024"
python ingest_data.py
```

## 🐛 Troubleshooting

### Error: "Failed to import HuggingFaceEmbeddings"
```powershell
pip install transformers sentence-transformers torch
```

### Error: "GROQ_API_KEY is required"
- Make sure your `.env` file has `GROQ_API_KEY=your_key_here`
- Restart Flask app after updating `.env`

### Error: "Model download failed"
- Check your internet connection
- The model downloads on first use
- It's cached after first download

### Slow First Run
- Normal! The embedding model downloads on first use
- Subsequent runs will be much faster

## 📚 Resources

- Groq Console: https://console.groq.com/
- Groq API Docs: https://console.groq.com/docs
- HuggingFace Model: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- LangChain Groq: https://python.langchain.com/docs/integrations/llms/groq

## ✨ You're All Set!

Your RAG system is now running on FREE services. Enjoy unlimited embeddings and fast Groq responses!

