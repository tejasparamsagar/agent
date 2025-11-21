# Fix PyTorch DLL Issue on Windows

The RAG system is failing to initialize due to a PyTorch DLL loading error on Windows.

## Quick Fix Options

### Option 1: Reinstall PyTorch CPU-only (Recommended)

```bash
pip uninstall torch -y
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Option 2: Install Visual C++ Redistributables

PyTorch requires Visual C++ Redistributables. Download and install:
- [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Option 3: Use Python 3.10 or 3.11

Python 3.13 may have compatibility issues. Consider using Python 3.10 or 3.11:

```bash
# Create new virtual environment with Python 3.11
python3.11 -m venv venv311
venv311\Scripts\activate
pip install -r requirements.txt
```

### Option 4: Temporary Workaround

The app will still run and show the error in `/health` endpoint. You can:
1. Deploy to Render.com (Linux environment, no PyTorch DLL issues)
2. Use Docker container
3. Use WSL (Windows Subsystem for Linux)

## Verify Fix

After applying a fix, restart the Flask app and check:

```bash
python app.py
```

Then visit: `http://127.0.0.1:5000/health`

You should see:
```json
{
  "status": "running",
  "rag_initialized": true
}
```



