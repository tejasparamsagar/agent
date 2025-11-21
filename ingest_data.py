"""
Script to ingest HT Code Hub data files into the RAG system.
Run this once to load your data before using the chat widget.
"""
import os
import sys
import requests
from pathlib import Path

# Configuration
API_URL = "http://localhost:5000"
DATASET_NAME = "htcodehub"

# Get AUTH_TOKEN from environment variable
# Make sure this matches the AUTH_TOKEN in your Flask app
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
if not AUTH_TOKEN:
    print("⚠️  AUTH_TOKEN not set in environment variables")
    print("   Set it with: $env:AUTH_TOKEN='your_token' (PowerShell)")
    print("   Or: set AUTH_TOKEN=your_token (CMD)")
    print("   Or: export AUTH_TOKEN=your_token (Mac/Linux)")
    print()
    # Try to read from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        AUTH_TOKEN = os.getenv("AUTH_TOKEN")
        if AUTH_TOKEN:
            print(f"✅ Found AUTH_TOKEN in .env file")
        else:
            print("❌ AUTH_TOKEN not found. Please set it.")
            sys.exit(1)
    except ImportError:
        print("❌ python-dotenv not installed. Install with: pip install python-dotenv")
        sys.exit(1)

def ingest_file(file_path: Path, dataset_name: str):
    """Ingest a single file."""
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"📄 Ingesting: {file_path.name}...")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'text/plain')}
            data = {'dataset_name': dataset_name}
            headers = {'X-API-Key': AUTH_TOKEN}
            
            response = requests.post(
                f"{API_URL}/ingest",
                files=files,
                data=data,
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success! Added {result.get('chunks_added', 0)} chunks")
                return True
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   {response.text}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Main function to ingest all data files."""
    print("=" * 60)
    print("HT Code Hub Data Ingestion Script")
    print("=" * 60)
    print()
    
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ RAG API is not responding at {API_URL}")
            print("   Make sure Flask is running: python app.py")
            return
        data = response.json()
        if not data.get('rag_initialized'):
            print("⚠️  RAG system is not initialized")
            print("   Check Flask console for errors")
            return
        print("✅ RAG API is running and initialized")
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to RAG API at {API_URL}")
        print("   Make sure Flask is running: python app.py")
        return
    
    print()
    
    # Find data files
    data_dir = Path("data")
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir.absolute()}")
        print("   Create 'data' folder and add your .txt files")
        return
    
    txt_files = list(data_dir.glob("*.txt"))
    if not txt_files:
        print(f"❌ No .txt files found in {data_dir.absolute()}")
        print("   Add your data files to the 'data' directory")
        return
    
    print(f"📁 Found {len(txt_files)} files to ingest:")
    for f in txt_files:
        print(f"   - {f.name}")
    print()
    
    # Ingest each file
    success_count = 0
    for file_path in txt_files:
        if ingest_file(file_path, DATASET_NAME):
            success_count += 1
        print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✅ Successfully ingested: {success_count}/{len(txt_files)} files")
    
    if success_count == len(txt_files):
        print()
        print("🎉 All data ingested! Your chat widget should now work.")
        print()
        print("Test it:")
        print(f"  curl -X POST {API_URL}/api/chat \\")
        print('    -H "Content-Type: application/json" \\')
        print('    -d \'{"query":"What programs do you offer?"}\'')
    else:
        print()
        print("⚠️  Some files failed to ingest. Check errors above.")

if __name__ == "__main__":
    main()

