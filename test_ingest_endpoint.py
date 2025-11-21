"""
Test the /ingest endpoint directly to see the actual error.
"""
import requests
import os
from pathlib import Path

# Configuration
API_URL = "http://localhost:5000"
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "htcodehub-2024")

# Test file
test_file = Path("data/htcodehub_about.txt")

if not test_file.exists():
    print(f"[ERROR] Test file not found: {test_file}")
    exit(1)

print("=" * 60)
print("Testing /ingest Endpoint")
print("=" * 60)
print(f"API URL: {API_URL}")
print(f"AUTH_TOKEN: {AUTH_TOKEN[:10]}...")
print(f"Test file: {test_file}")
print()

# Check health first
print("1. Checking API health...")
try:
    response = requests.get(f"{API_URL}/health", timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        health = response.json()
        print(f"   RAG Initialized: {health.get('rag_initialized', False)}")
    else:
        print(f"   [ERROR] Health check failed: {response.text}")
        exit(1)
except Exception as e:
    print(f"   [ERROR] Cannot connect to API: {e}")
    print("   Make sure Flask app is running: python app.py")
    exit(1)

print()
print("2. Testing file ingestion...")

# Prepare file upload
with open(test_file, 'rb') as f:
    files = {'file': (test_file.name, f, 'text/plain')}
    headers = {'X-API-Key': AUTH_TOKEN}
    data = {'dataset_name': 'htcodehub'}
    
    try:
        response = requests.post(
            f"{API_URL}/ingest",
            files=files,
            headers=headers,
            data=data,
            timeout=30
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   [SUCCESS] Ingested {result.get('chunks_added', 0)} chunks")
        else:
            print(f"   [ERROR] Ingestion failed")
            try:
                error_data = response.json()
                print(f"   Error message: {error_data.get('message', 'Unknown error')}")
                print(f"   Error type: {error_data.get('type', 'Unknown')}")
            except:
                pass
                
    except Exception as e:
        print(f"   [ERROR] Request failed: {e}")
        import traceback
        traceback.print_exc()

